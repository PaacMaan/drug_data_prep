import pandas as pd
import os

# setting environment and const variables
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
DATA_PATH = AIRFLOW_HOME + '/dags/data'


def get_atccode_by_drug_name(drug):
	"""
	Return the atccode by drug name

	Parameters:
    drug (string) : the drug name

    Returns:
    atccode (string) : the atccode attached to that drug
	"""
	drugs = pd.read_csv(f'{DATA_PATH}/drugs.csv')
	return drugs.loc[drugs['drug'] == drug, 'atccode'].item()


def get_drug_mentions(df, drug_list, column_name="title"):
	"""
	Return the atccode by drug name

	Parameters:
    df (DataFrame) : the dataframe containing titles and journals data
    drug_list (List) : extracted list of drugs
    column_name (string) : the column where to fetch for drug mentions in the dataframe

    Returns:
    drug_mentions (list) : a list of drug mentions depending on the given dataframe if it's PubMed or Clinical trial
	"""

	# initialize a list to hold the resulted json objects
	drug_mentions = []
	
	for drug in drug_list:
	    mentioned_in = []
	    # iterate over the dataframe and check if a drug name exist on a publications's title
	    for index, row in df.iterrows():
	        mention_obj = {}
	        if row[column_name].lower().find(drug.lower()) > 0:
	            mention_obj[column_name] = row[column_name]
	            mention_obj["date"] = row["date"]
	            mention_obj["journal"] = row["journal"]

	            mentioned_in.append(mention_obj)

        # filter the empty lists where there is no mention
	    if len(mentioned_in) != 0:
	        drug_mentions.append({"drug":drug, "atccode": get_atccode_by_drug_name(drug), "mentioned_in":mentioned_in})

	return drug_mentions