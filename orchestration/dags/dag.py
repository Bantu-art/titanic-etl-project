import sys
import os
from pathlib import Path

# Find project root - works for different installation paths
dag_dir = Path(__file__).parent
project_name = "titanic-etl-project"

# Look for project in common locations
for parent in [dag_dir.parent, dag_dir.parent.parent, dag_dir.parent.parent.parent]:
    project_path = parent / project_name
    if project_path.exists():
        sys.path.append(str(project_path))
        break
else:
    # Fallback - assume standard structure
    home_dir = Path.home()
    project_path = home_dir / "dataProjects" / project_name
    if project_path.exists():
        sys.path.append(str(project_path))

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
