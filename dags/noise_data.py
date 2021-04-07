from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator


def download_csv():
    print("Download csv")

def download_media():
    print("Download media")

default_args = {
    'owner': 'Lydia',
    'start_date': datetime(2021, 3, 1),
    'retry_delay': timedelta(minutes=20)
}

data_prep_dag = DAG(
    dag_id='prepare_data',
    default_args=default_args,
    schedule_interval='@daily'
)

download_csv_task = PythonOperator(
    task_id='download_csv_task',
    python_callable=download_csv,
    dag=data_prep_dag
)

download_media_task = PythonOperator(
    task_id='download_media_task',
    python_callable=download_csv,
    dag=data_prep_dag
)

