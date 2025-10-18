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

def ingest_bronze_to_silver() -> None:

    BRONZE_PATH = f"{DATALAKE_PATH}/bronze/transaction_data"
    SILVER_PATH = f"{DATALAKE_PATH}/silver/transaction_data"

    df_bronze = DeltaTable.forPath(spark, BRONZE_PATH)

    try:
        df_silver = DeltaTable.forPath(spark, SILVER_PATH)
        df_silver.toDF().limit(1)

        MAIOR_DATA_SILVER = (
            df_silver
            .toDF()
            .agg(
                F.max('transaction_date')
            )
            .collect()[0][0]
        )

        df_bronze = df_bronze.toDF().filter(f"transaction_date > '{MAIOR_DATA_SILVER}'")
        
        (
            df_silver.alias('old_data')
            .merge(
                df_bronze.alias('new_data'),
                "old_data.transaction_id = new_data.transaction_id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )

    
    except Exception as e:
        if 'DELTA_MISSING_DELTA_TABLE' in str(e):
            (
                df_bronze
                .toDF()
                .write
                .format('delta')
                .option('mergeSchema', 'true')
                .mode('overwrite')
                .save(SILVER_PATH)
            )
        else:
            raise e