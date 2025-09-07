import sys
import os
sys.path.append('/home/bantu/dataProjects/titanic_pipeline')

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def extract_wrapper():
    os.chdir('/home/bantu/dataProjects/titanic_pipeline')
    from extraction.extract import extract_data
    return extract_data()

def transform_wrapper():
    os.chdir('/home/bantu/dataProjects/titanic_pipeline')
    from transformation.transform import transform_data
    return transform_data()

def load_wrapper():
    os.chdir('/home/bantu/dataProjects/titanic_pipeline')
    from loading.load import load_data
    return load_data()

# Define DAG
default_args = {"owner": "bantu", "start_date": datetime(2025, 9, 5)}
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
