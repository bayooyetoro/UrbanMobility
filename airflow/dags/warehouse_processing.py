from airflow import DAG
from airflow.providers.common.sql.operators.sql import (SQLExecuteQueryOperator)
from datetime import datetime

with DAG(
    dag_id="warehouse_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    create_dim_date = SQLExecuteQueryOperator(
        task_id= "create_dim_date",
        conn_id= "postgres_default",
        sql= "sql/create_dim_date.sql"
    )

    create_dim_station = SQLExecuteQueryOperator(
        task_id= "create_dim_station",
        conn_id= "postgres_default",
        sql= "sql/create_dim_station.sql"
    )

    load_fact = SQLExecuteQueryOperator(
        task_id="load_fact_bike_trips",
        conn_id="postgres_default",
        sql="sql/load_fact_bike_trips.sql"
    )

    create_dim_date >> create_dim_station >> load_fact