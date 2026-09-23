import pendulum

from airflow.sdk import dag, task

@dag(
    dag_id="data_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2026, 9, 20, tz="UTC"),
    catchup=False,
)
def data_pipeline():
        
        @task
        def start_pipeline():
          print("Data pipeline started")

        start_pipeline()