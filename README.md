# Drug Data Processing

## Informations
This repository process 3 datasets which are `drugs.csv`, `pubmed.csv` and `clinical_trials.csv` in order to build a pipeline that will generate a json containing each drug within its correspending mentions in different journals and publications coming from different sources.

## Data structure
The resulted output is stored in a folder under `dags > data > output`, where we store data resulted by each step from the pipeline.
Resulted files are :
- `drug_mentions_in_ct.json` : contains drug mentions on clinical trials
- `drug_mentions_in_pubmed.json` : contains drug mentions on PubMed
- `drug_mentions.json` : combine them both by drug and atccode

## Approach
The approach consist on extracting all drug names in a list coming from the `drugs.csv` file, then we fetch these names on the publication's titles either on `pubmed.csv` or `clinical_trials.csc`, wehenever there is a match, we create a new object wehere we save the `journal`, `title` and `date` for each drug.

This leads us to a result similar to this one below :
```
{
        "drug": "EPINEPHRINE",
        "atccode": "A01AD",
        "mentioned_in": [
            {
                "title": "The High Cost of Epinephrine Autoinjectors and Possible Alternatives.",
                "date": "01/02/2020",
                "journal": "The journal of allergy and clinical immunology. In practice"
            },
            {
                "title": "Time to epinephrine treatment is associated with the risk of mortality in children who achieve sustained ROSC after traumatic out-of-hospital cardiac arrest.",
                "date": "01/03/2020",
                "journal": "The journal of allergy and clinical immunology. In practice"
            }
        ]
    }
```

Once this step is done for both data sources, the next step consist on merging the found mentions. With that said, we need to merge both json outputs coming from `pubmed.csv` and `clinical_trial.csv` by their common keys which are the `drug` and its correspending `atccode`. 
The benefit in this scenario is that in case a drug has more than one unique `atccode`, it still working either.

 

## Output :
The data pipeline output are the three files saved in the `dags > data > output` directory, we are more concerned about the final data schema which looks like :

### JSON sample :
```
{
        ...
        {
        "drug": "DIPHENHYDRAMINE",
        "atccode": "A04AD",
        "mentioned_in": [
            {
                "title": "A 44-year-old man with erythema of the face diphenhydramine, neck, and chest, weakness, and palpitations",
                "date": "01/01/2019",
                "journal": "Journal of emergency nursing"
            },
            {
                "title": "An evaluation of benadryl, pyribenzamine, and other so-called diphenhydramine antihistaminic drugs in the treatment of allergy.",
                "date": "01/01/2019",
                "journal": "Journal of emergency nursing"
            },
            {
                "scientific_title": "Use of Diphenhydramine as an Adjunctive Sedative for Colonoscopy in Patients Chronically on Opioids",
                "date": "1 January 2020",
                "journal": "Journal of emergency nursing"
            },
            {
                "scientific_title": "Phase 2 Study IV QUZYTTIR™ (Cetirizine Hydrochloride Injection) vs V Diphenhydramine",
                "date": "1 January 2020",
                "journal": "Journal of emergency nursing"
            },
            {
                "scientific_title": "Feasibility of a Randomized Controlled Clinical Trial Comparing the Use of Cetirizine to Replace Diphenhydramine in the Prevention of Reactions Related to Paclitaxel",
                "date": "1 January 2020",
                "journal": "Journal of emergency nursing"
            }
        ],
        ...
    }
```


## Installations
1. First of all, build the docker image using `docker-compose` with the following command : 

`$ docker-compose up`

2. Once the docker images built, you can go to  new browser window tab type the following adresse :
    `http://localhost:8080/`

3. Then Airflow UI will show up, in order to run the DAG all you need to do is to activate the pipeline and trigger the dag to be run from the UI byclicking on `Trigger DAG`. 

![dag_pipeline](https://github.com/PaacMaan/drug_data_prep/blob/main/pipeline_dag.png?raw=true)


## Adhoc feature
The last requested question about the ad-hoc feature could be run by executing the python file under `adhoc` repository in the `main.py` file.
 `$ docker exec CONTAINER_ID python adhoc/main.py `
 
 ### Output : 
 >>> `journal with maximum different drugs mentions is Journal of emergency nursing with 2 mentions`



