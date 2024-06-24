import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_spast": False,
    "start_date": pendulum.datetime(2023, 1, 9),
    "email": [""],
}

def training(**kwargs):
    from src.pipeline import training_pipeline
    training_pipeline()

bash_success="echo 'Training Pipeline is completed successfully'"

with DAG(dag_id="training_dag",default_args=default_args,description="Sensor Training Pipeline",
schedule_interval="@weekly",catchup=False,tags=["loan_default"]) as dag:   
    
    training_pipeline=PythonOperator(task_id="training_pipeline",python_callable=training)
    success=BashOperator(task_id="success",bash_command=bash_success)
    training_pipeline>>success