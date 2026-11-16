from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
import os


BRONZE_PATH = "/data/bronze/bikes"
SOURCE_PATH = "/data/source_data/bikes/*.csv"

spark = (
    SparkSession.builder
    .master("spark://spark-master:7077")
    .appName("bike-bronze-ingestion")
    .getOrCreate()
)

_options = {"header":"true", "inferSchema":"true", "mode":"PERMISSIVE", "columnNameOfCorruptRecored":"_corrupt_record"}
df = spark.read.options(**_options).csv(SOURCE_PATH)

bronze_df = (
    df.withColumn("source_file", F.input_file_name())
      .withColumn("ingestion_timestamp", F.current_timestamp())
      .withColumn("load_date", F.current_date())
      .withColumn("_partition_date", F.to_date(F.col("Start Date")))
)

bronze_df.write.mode("append").parquet(BRONZE_PATH)

spark.stop()