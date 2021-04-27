from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


def download_odk_csv():
    print("Download csv")

def download_odk_media():
    print("Download media")

def upload_media_to_s3():
    print("Upload media")

default_args = {
    'owner': 'Lydia',
    'start_date': datetime(2021, 3, 1),
    'retry_delay': timedelta(minutes=20)
}

data_transfer_dag = DAG(
    dag_id='prepare_data',
    default_args=default_args,
    schedule_interval='@daily'
)

download_odk_csv_task = PythonOperator(
    task_id='download_csv_task',
    python_callable=download_odk_csv,
    dag=data_transfer_dag
)

download_odk_media_task = PythonOperator(
    task_id='download_odk_media_task',
    python_callable=download_odk_media,
    dag=data_transfer_dag
)

upload_media_to_s3_task = PythonOperator(
    task_id='upload_media_to_s3_task',
    python_callable=upload_media_to_s3,
    dag=data_transfer_dag
)

