import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import os
import pyspark.sql.functions as F

DATALAKE_PATH = ' '

import os
from pyspark.sql import SparkSession
from delta import *

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

builder = SparkSession.builder.appName("TesteDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("SparkSession criada com sucesso!")
print("Versão do Spark:", spark.version)


def ingest_source_to_bronze(data_processamento:str) -> None:

    SOURCE_PATH = f'{DATALAKE_PATH}/source/transaction_system/transaction_data_{data_processamento.replace('-', '_')}.csv'
    BRONZE_PATH = f"{DATALAKE_PATH}/bronze/transaction_data"

    df_source = (
        spark
        .read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("ignoreLeadingWhiteSpace", "true")
        .option("ignoreTrailingWhiteSpace", "true")
        .csv(SOURCE_PATH)
    )

    if "_c0" in df_source.columns:
        df_source = df_source.drop("_c0")

    try:
        df_bronze = DeltaTable.forPath(spark, BRONZE_PATH)
        df_bronze.toDF().limit(1)

        df_bronze.delete(f"transaction_date = '{data_processamento}'")

        (
            df_source
            .write
            .format('delta')
            .mode('append')
            .option('mergeSchema', 'true')
            .save(BRONZE_PATH)
        )

    except Exception as e:
        if 'DELTA_MISSING_DELTA_TABLE' in str(e):
            (
                df_source
                .write
                .format('delta')
                .option('mergeSchema', 'true')
                .mode('overwrite')
                .save(BRONZE_PATH)
            )
        else:
            raise e

    return BRONZE_PATH

