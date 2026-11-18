from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(dag_id="warehouse_build", start_date=datetime(2025, 1, 1), catchup=False,) as dag:

    create_dim_station = SQLExecuteQueryOperator(
        task_id="create_dim_station",
        conn_id="postgres_default",
        sql="sql/create_dim_station.sql"
    )

    load_dim_station = SQLExecuteQueryOperator(
        task_id="load_dim_station",
        conn_id="postgres_default",
        sql="sql/load_dim_station.sql"
    )

    create_dim_station >> load_dim_station