from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from decouple import config
from scripts.odk_data_download import get_submissions
from scripts.s3_data_upload import upload_to_s3


def download_odk_media():
    get_submissions()

def upload_media_to_s3():
    upload_to_s3('audio')

default_args = {
    'owner': 'Lydia',
    'start_date': datetime(2021, 5, 7),
    'email': config('ODK_EMAIL'),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=20)
}

data_transfer_dag = DAG(
    dag_id='prepare_data',
    default_args=default_args,
    schedule_interval='@daily'
)

download_odk_media_task = PythonOperator(
    task_id='download_odk_media',
    python_callable=download_odk_media,
    dag=data_transfer_dag
)

upload_media_to_s3_task = PythonOperator(
    task_id='upload_media_to_s3',
    python_callable=upload_media_to_s3,
    dag=data_transfer_dag
)
