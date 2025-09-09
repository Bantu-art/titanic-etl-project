import sys
import os

# PROJECT_ROOT replaced by setup script
PROJECT_ROOT = "{{PROJECT_ROOT}}"
sys.path.insert(0, PROJECT_ROOT)

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def extract_wrapper():
    from extraction.extract import extract_data
    return extract_data()

def transform_wrapper():
    from transformation.transform import transform_data
    return transform_data()

def load_wrapper():
    from loading.load import load_data
    return load_data()

# Define DAG
default_args = {"owner": "data_engineer", "start_date": datetime(2024, 1, 1)}
with DAG("titanic_pipeline",
         default_args=default_args,
         schedule="@daily",
         catchup=False) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_wrapper
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_wrapper
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_wrapper
    )

    # Define order
    extract_task >> transform_task >> load_task