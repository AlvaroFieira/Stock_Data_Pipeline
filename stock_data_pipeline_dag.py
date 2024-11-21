from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/home/ubuntu/airflow/dags/src')
from fetch_stock_data import fetch_stock_data
from transform_stock_data import transform_stock_data

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# Define the DAG
with DAG(
    "stock_data_pipeline",
    default_args=default_args,
    description="ETL pipeline for stock price data",
    schedule_interval="0 * * * *",  # Run every hour
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    fetch_data = PythonOperator(
        task_id="fetch_stock_data",
        python_callable=fetch_stock_data,
        op_kwargs={"symbol": "AAPL"}
    )
    
    transform_data = PythonOperator(
        task_id="transform_stock_data",
        python_callable=transform_stock_data
    )
    
    # Define task dependencies
    fetch_data >> transform_data
