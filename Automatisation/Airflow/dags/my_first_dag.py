from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import datetime
import time

my_dag = DAG(
    dag_id='automatisationComplete',
    description='Lance tous les process du projet',
    tags=['datascientest', 'projet'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2),
    }
)

# definition of the function to execute
def lunchScrapping():
    # raise TypeError('This will not work')
    print(datetime.datetime.now())
    print('Hello from Airflow')

def lunchIngestion():
    print('Hello from Airflow again')


my_lunchScrapping = PythonOperator(
    task_id='lunchScrapping',
    python_callable=lunchScrapping,
    dag=my_dag
)

my_lunchIngestion = PythonOperator(
    task_id='lunchIngestion',
    python_callable=lunchIngestion,
    dag=my_dag
)

my_lunchScrapping >> my_lunchIngestion