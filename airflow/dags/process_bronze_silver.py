from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from airflow.providers.apache.spark.operators.spark_submit import (SparkSubmitOperator)

with DAG(
    dag_id="bronze-to-silver",
    start_date=datetime(2015, 9, 18),
    catchup=False,
    schedule ="@daily"
) as dag:

    create_bronze_parquet = SparkSubmitOperator(
        task_id= "create_bronze_files",
        conn_id= "spark_default",
        application= "/jobs/01_process_bronze_to_silver.py"
    )

    create_silver_parquet = SparkSubmitOperator(
        task_id= "create_silver_files",
        conn_id= "spark_default",
        application= "/jobs/02_load_silver_to_postgres.py"
    )

    create_bronze_parquet >> create_silver_parquet