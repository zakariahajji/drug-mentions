# For Servier : drug mention finder
 
Check it live on [Streamlit](https://drug-mentions-ktihvqxgbuay9lcvcystm3.streamlit.app/
)

Pre-requisits : 

- Python 3.11 (or compatible) installed
- Poetry installed (for dependency management)



This project processes drug mentions from three CSV files (clinical trials, drugs, PubMed) and outputs a JSON structure with all mentions. It also provides a Streamlit UI for uploading the CSVs and visualizing the resulting data in an interactive graph




## Installation
Clone the repo:

```
git clone git@github.com:zakariahajji/drug-mentions.git

cd drug-mentions
```

## Install dependencies with Poetry:

```
poetry install
```


## Directory structure:
```

    ├── README.md
    ├── app.py
    ├── pyproject.toml
    ├── src/
    │   ├── __init__.py
    │   ├── data/
    │   │   ├── input/
    │   │   │   ├── clinical_trials.csv
    │   │   │   ├── drugs.csv
    │   │   │   ├── pubmed.csv
    │   │   │   └── pubmed.json
    │   │   └── output/
    │   │       └── drug_mentions.json
    │   └── drug_mentions/
    │       ├── __init__.py
    │       ├── main.py
    │       ├── models/
    │       │   ├── __init__.py
    │       │   └── schema.py
    │       └── pipeline/
    │           ├── __init__.py
    │           ├── loader.py
    │           ├── transformer.py
    │           └── writer.py
    ├── tests/
    │   ├── test_loader.py
    │   ├── test_transformer.py
    │   └── test_writer.py
    └── utils/
        └── d3_viewer.py
```



You can run the main pipeline by running : 


```
➜  drug-mentions git:(main) ✗ poetry run drug-mentions       

Drug Mention Finder
Loading drugs...
Loaded 7 drugs
Loading publications...
Loaded 21 publications
Finding drug mentions...
Found mentions for 7 drugs
Writing results...
Results written to /Users/zakaria/Development/solution/drug-mentions/src/data/output/drug_mentions.json
```



You can run tests y running : 

```
drug-mentions git:(main) poetry run pytest              

==================================================================================================== test session starts =====================================================================================================
platform darwin -- Python 3.11.5, pytest-7.4.4, pluggy-1.5.0
rootdir: /Users/zakaria/Development/solution/drug-mentions
collected 5 items                                                                                                                                                                                                            

tests/test_loader.py ..                                                                                                                                                                                                [ 40%]
tests/test_transformer.py ..                                                                                                                                                                                           [ 80%]
tests/test_writer.py .                                                                                                                                                                                                 [100%]

===================================================================================================== 5 passed in 0.30s ======================================================================================================

```



You can run the ad-hoc script by running : 

```
drug-mentions-py3.11➜  drug-mentions git:(main) ✗ poetry run python utils/ad_hoc.py

Le journal qui mentionne le plus de médicaments différents est The journal of maternal-fetal & neonatal medicine avec 2 médicaments différents : ATROPINE,BETAMETHASONE
```


## Commentaires 

Le code est organisé de manière modulaire en séparant clairement les étapes clés du pipeline (Loader, transformation et Writer). Cela permet de réutiliser certaines étapes dans d'autres pipelines de données. De plus, la structure a été conçue pour être facilement intégrée dans un orchestrateur(comme un DAG Airflow), On peut ainsi personaliser chaque module pour faire le job selon le service orchestré.
Personalisations possibles selon le context : 

    ( Loader et transformer > Partitionner et distribuer le calcul (Spark : aws:EMR/gcp:DataProc) , ou DBT/BigQuery

    (Writer : Ca dépend des use-cases, OLTP/NoSQL > Applicatif OU BI et Dashboards : Datawarehouse ( Bigquery...))

    