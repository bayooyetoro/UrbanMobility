from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

SILVER_PATH = "/data/silver/bikes/*.parquet"

POSTGRES_URL = (
    f"jdbc:postgresql://postgres:5432/{os.getenv('POSTGRES_DB')}"
)

POSTGRES_PROPERTIES = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver"
}

spark = (
    SparkSession.builder
    .appName("load-bikes-postgres")
    .getOrCreate()
)

df = spark.read.parquet(SILVER_PATH)

(
    df.write
    .format("jdbc")
    .option("url", POSTGRES_URL)
    .option("dbtable", "silver.bike_trips")
    .option("user", POSTGRES_PROPERTIES["user"])
    .option("password", POSTGRES_PROPERTIES["password"])
    .option("driver", POSTGRES_PROPERTIES["driver"])
    .mode("append")
    .save()
)

spark.stop()