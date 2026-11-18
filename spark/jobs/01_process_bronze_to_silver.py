from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BRONZE_FILES = "/data/bronze/*.csv"
SILVER_PATH = "/data/silver"
QUARANTINE_PATH = "/data/quarantine"

spark = SparkSession.builder.master("spark://spark-master:7077").appName("process-bronze-files").getOrCreate()


_options = {"header":"true", "inferSchema":"true", "mode":"DROPMALFORMED"}
df = spark.read.options(**_options).csv(BRONZE_FILES)

bronze_df = (
    df.withColumn("_ingestion_timestamp", F.current_timestamp())
      .withColumn("_load_date", F.current_date())
      .withColumn("_file_name", F.input_file_name())
)

# DATA QUALTIY REQUIREMENTS
invalid_df = (
    bronze_df.withColumn(
        "rejection_reason",
        F.when(F.col("Rental Id").isNull(), F.lit("missing_rental_id"))
        .when(F.col("Duration") <= 0, F.lit("invalid_duration"))
        .when(F.col("Start Date").isNull(), F.lit("missing_start_date"))
        .when(F.col("End Date").isNull(), F.lit("missing_end_date"))
        .when(F.col("StartStation Name").isNull(), F.lit("missing_start_station"))
        .when(F.col("EndStation Name").isNull(), F.lit("missing_end_station"))
    )
    .filter(F.col("rejection_reason").isNotNull())
)


# PROCESS VALID RECORDS TO SILVER
valid_df = (
    bronze_df.withColumnsRenamed({
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
    .filter(F.col("Rental Id").isNotNull())
    .filter(F.col("Duration") > 0)
    .filter(F.col("Start Date").isNotNull())
    .filter(F.col("End Date").isNotNull())
    .filter(F.col("StartStation Name").isNotNull())
    .filter(F.col("EndStation Name").isNotNull())
    .select(
        "rental_id",
        "bike_id",
        F.to_timestamp(F.col("start_date"), 'dd/MM/yyyy HH:mm').alias("start_date"),
        F.to_timestamp(F.col("end_date"), 'dd/MM/yyyy HH:mm').alias("end_date"),
        F.col("duration").cast("int").alias("duration"),
        "start_station_id",
        "start_station_name",
        "end_station_id",
        "end_station_name",
        "_ingestion_timestamp",
        "_load_date",
        "_file_name"
    ).dropDuplicates(["rental_id"])
)


valid_df.write.mode("overwrite").parquet(SILVER_PATH)
invalid_df.write.mode("overwrite").parquet(QUARANTINE_PATH)

spark.stop()