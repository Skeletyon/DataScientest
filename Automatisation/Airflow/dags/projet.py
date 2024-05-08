from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
import datetime
import subprocess
import time

folder_scrapping = '../../projet/scrapping/'
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

# my_lunchScrapping = BashOperator(
#     task_id='lunchScrapping',
#     bash_command='python /opt/projet/scrapping/scrappingDetails.py',
#     dag=my_dag
# )

my_lunchIngestion = BashOperator(
    task_id='lunchIngestion',
    bash_command='python /opt/projet/elastic/chargement.py',
    dag=my_dag
)

# my_lunchScrapping >> my_lunchIngestion
my_lunchIngestion