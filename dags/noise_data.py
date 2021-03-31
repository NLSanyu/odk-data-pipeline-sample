from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

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