"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import json
from helper import *

# setting environment and const variables
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
DATA_PATH = AIRFLOW_HOME + '/dags/data'

args = {
    'owner': 'airflow'
}

# instanciate a DAG object
dag = DAG(
    dag_id='data_pipeline',
    start_date=days_ago(2),
    default_args=args
)


def get_mentions_from_pubmed():
    """Check the existence of a drug on a publication's title in PubMed dataset"""

    # read the drugs as a dataframe from csv file
    drugs = pd.read_csv(f'{DATA_PATH}/drugs.csv')
    # read the pubmed as a dataframe from csv file
    pubmed = pd.read_csv(f'{DATA_PATH}/pubmed.csv')

    # build a list of unique drugs
    drug_list = list(drugs["drug"].unique())

    # call the get_drug_mentions function from helper to get the mentions of drugs in pubmed
    drug_mentions_in_pubmed = get_drug_mentions(pubmed, drug_list, column_name="title")
    

    # save results as json
    with open(f'{DATA_PATH}/output/drug_mentions_in_pubmed.json', 'w', encoding='utf-8') as f:
        json.dump(drug_mentions_in_pubmed, f, ensure_ascii=False, indent=4)


def get_mentions_from_ct():
    """Check the existence of a drug on a publication's title in Clinical Trials dataset"""

    # read the drugs as a dataframe from csv file
    drugs = pd.read_csv(f'{DATA_PATH}/drugs.csv')
    # read the clinical_trials as a dataframe from csv file
    clinical_trials = pd.read_csv(f'{DATA_PATH}/clinical_trials.csv')
    
    # build a list of unique drugs
    drug_list = list(drugs["drug"].unique())

    # call the get_drug_mentions function from helper to get the mentions of drugs in clinical trials
    drug_mentions_in_ct = get_drug_mentions(clinical_trials, drug_list, column_name="scientific_title")

    # save as json
    with open(f'{DATA_PATH}/output/drug_mentions_in_ct.json', 'w', encoding='utf-8') as f:
        json.dump(drug_mentions_in_ct, f, ensure_ascii=False, indent=4)


def combine_data():
    """Combine both drug mentions coming from PubMed and Clinical_trials by drug name and their atccode"""

    # read the drug mentions in pubmed 
    with open(f'{DATA_PATH}/output/drug_mentions_in_pubmed.json') as f:
        mentions_in_pubmed = json.load(f)

    # read the drug mentions in clinical trial
    with open(f'{DATA_PATH}/output/drug_mentions_in_ct.json') as f:
        mentions_in_ct = json.load(f)

    # combine both json files on the "mentioned_in" attribute by drug and atccode
    for obj in mentions_in_ct:
        for obj2 in mentions_in_pubmed:
            if obj['drug'] == obj2['drug'] and obj['atccode'] == obj2['atccode']:
                obj2['mentioned_in'].extend(obj['mentioned_in'])
                break

    # save the json's combination result as json file
    with open(f'{DATA_PATH}/output/drug_mentions.json', 'w', encoding='utf-8') as f:
        json.dump(mentions_in_pubmed, f, ensure_ascii=False, indent=4)
    


# Defining Python's operators calling the built-in functions above

get_mentions_from_pubmed = PythonOperator(
    task_id='get_mentions_from_pubmed',
    python_callable=get_mentions_from_pubmed,
    dag=dag
)

get_mentions_from_ct = PythonOperator(
    task_id='get_mentions_from_ct',
    python_callable=get_mentions_from_ct,
    dag=dag
)

combine_and_save_data = PythonOperator(
    task_id='combine_and_save_data',
    python_callable=combine_data,
    dag=dag
)

# setting up the DAG's pipeline
[get_mentions_from_pubmed, get_mentions_from_ct] >> combine_and_save_data


if __name__ == "__main__":
    dag.cli()