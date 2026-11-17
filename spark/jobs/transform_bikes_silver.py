from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, lit, to_timestamp

BRONZE_PATH = "/data/bronze/bikes"
SILVER_PATH = "/data/silver/bikes"
QUARANTINE_PATH = "/data/quarantine/bikes"

spark = (
    SparkSession.builder
    .master("spark://spark-master:7077")
    .appName("bike-bronze-ingestion")
    .getOrCreate()
)

df = spark.read.parquet(f"{BRONZE_PATH}/*.parquet")

# DATA QUALTIY REQUIREMENTS 
invalid_df = (
    df.withColumn(
        "rejection_reason",
        when(col("Rental Id").isNull(), lit("missing_rental_id"))
        .when(col("Duration") <= 0, lit("invalid_duration"))
        .when(col("Start Date").isNull(), lit("missing_start_date"))
        .when(col("End Date").isNull(), lit("missing_end_date"))
        .when(col("StartStation Name").isNull(), lit("missing_start_station"))
        .when(col("EndStation Name").isNull(), lit("missing_end_station"))
    )
    .filter(col("rejection_reason").isNotNull())
)

valid_df = (
    df.withColumnsRenamed({
        "Rental Id": "rental_id",
        "Duration": "duration",
        "Start Date": "start_date",
        "End Date": "end_date",
        "EndStation Id": "end_station_id",
        "StartStation Id": "start_station_id",
        "StartStation Name": "start_station_name",
        "EndStation Name": "end_station_name",
        "EndStation Id": "end_station_id",
        "Bike Id": "bike_id"
    })
    .filter(col("Rental Id").isNotNull())
    .filter(col("Duration") > 0)
    .filter(col("Start Date").isNotNull())
    .filter(col("End Date").isNotNull())
    .filter(col("StartStation Name").isNotNull())
    .filter(col("EndStation Name").isNotNull())
    .select(
        "rental_id",
        "bike_id",
        to_timestamp(col("start_date"), 'dd/MM/yyyy HH:mm').alias("start_date"),
        to_timestamp(col("end_date"), 'dd/MM/yyyy HH:mm').alias("end_date"),
        col("duration").cast("int").alias("duration"),
        "start_station_id",
        "start_station_name",
        "end_station_id",
        "end_station_name",
        "ingestion_timestamp",
        "load_date"
    )
)

valid_df = valid_df.dropDuplicates(["rental_id"])
valid_df.write.mode("overwrite").parquet(SILVER_PATH)
invalid_df.write.mode("overwrite").parquet(QUARANTINE_PATH)