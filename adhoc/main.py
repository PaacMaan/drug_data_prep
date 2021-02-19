import json
import os
from operator import itemgetter

# setting environment and const variables
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
DATA_PATH = AIRFLOW_HOME + '/dags/data/output'

def adhoc_feature(drug_mentions_file):
	"""

	"""
	
	# read the json data on which we'll do the computation 
	with open(f'{DATA_PATH}/'+drug_mentions_file) as f:
		drug_mentions = json.load(f)
	
	counts = {}

	# loop through our dicts in the list
	for obj in drug_mentions:
	    # look in each journal mention
	    for mention in obj['mentioned_in']:
	        # if we haven't seen this journal before
	        if mention['journal'] not in counts:
	            counts[mention['journal']] = set()

	        counts[mention['journal']].add(obj['drug'])

	# this would have all our verbose info as we want it
	unique_drug_counts = [
	    {
	        "journal": journal,
	        "unique_drug_mentions": len(drugs)
	    }
	    for journal, drugs in counts.items()
	]

	# journal_with_max_drugs_mentions = max(counts.items(), key=lambda x: len(x[1]))
	journal_with_max_drugs_mentions = max(unique_drug_counts, key=itemgetter("unique_drug_mentions"))
	return journal_with_max_drugs_mentions


if __name__ == '__main__':
	target_file = "drug_mentions.json"
	journal_with_max_drugs_mentions = adhoc_feature("drug_mentions.json")
	print("journal with maximum different drugs mentions is {} with {} mentions".format(journal_with_max_drugs_mentions["journal"], journal_with_max_drugs_mentions["unique_drug_mentions"]))