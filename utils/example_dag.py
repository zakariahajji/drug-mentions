"""
Exemple de DAG Airflow orchestrant 3 tâches :
- load_data : Chargement via DataLoader
- transform_data : Transformation via DataTransformer
- write_data : Écriture via DataWriter
"""

from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from drug_mentions.pipeline.loader import DataLoader
from drug_mentions.pipeline.transformer import DataTransformer
from drug_mentions.pipeline.writer import DataWriter

def load_data(**kwargs):
    """Load the data from the input directory."""
    input_dir = Path('/path/to/your/input')  
    loader = DataLoader(str(input_dir))
    drugs = loader.load_drugs()
    pubs = loader.load_pubmed() + loader.load_clinical_trials()
    return {'drugs': [d.dict() for d in drugs], 'pubs': [p.dict() for p in pubs]}

def transform_data(**kwargs):
    """Transform the loaded data to find drug mentions."""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='load_data')
    from drug_mentions.models.schema import Drug, Publication
    drugs = [Drug.parse_obj(d) for d in data['drugs']]
    pubs = [Publication.parse_obj(p) for p in data['pubs']]
    transformer = DataTransformer()
    return transformer.find_drug_mentions(drugs, pubs)

def write_data(**kwargs):
    """Write the transformed data to a JSON file Ou BigQuery."""
    ti = kwargs['ti']
    mentions = ti.xcom_pull(task_ids='transform_data')
    output_dir = Path('/path/to/your/output') 
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'drug_mentions.json'
    DataWriter().write_json(mentions, output_file)
    return str(output_file)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'drug_mentions_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
    )
    write_task = PythonOperator(
        task_id='write_data',
        python_callable=write_data,
        provide_context=True,
    )

    load_task >> transform_task >> write_task

