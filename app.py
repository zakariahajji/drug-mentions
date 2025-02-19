import streamlit as st
import pandas as pd
from io import StringIO
from utils.vis_network_viewer import vis_network_viewer
import json

st.set_page_config(layout="wide")
st.title("Drug Mentions Finder with Modern Network Visualization")

col_left, col_right = st.columns([1, 1])

def parse_csv(file):
    if file is not None:
        return pd.read_csv(StringIO(file.getvalue().decode("utf-8")))
    return None

with col_left:
    st.header("Upload CSV Files")
    clinical_file = st.file_uploader("Clinical Trials CSV", type=["csv"])
    drugs_file = st.file_uploader("Drugs CSV", type=["csv"])
    pubmed_file = st.file_uploader("PubMed CSV", type=["csv"])
    process_button = st.button("Process")

with col_right:
    st.header("Visualization")

if process_button:
    clinical_df = parse_csv(clinical_file)
    drugs_df = parse_csv(drugs_file)
    pubmed_df = parse_csv(pubmed_file)

    if clinical_df is None or drugs_df is None or pubmed_df is None:
        st.warning("Please upload all three CSV files before processing.")
    else:
        # Here you would normally call your pipeline to process the data.
        # For demonstration, we use a fake output dictionary.
        results_dict = {
            "DIPHENHYDRAMINE": {
                "mentions": {
                    "pubmed": [
                        {"id": "1", "title": "A sample title", "date": "2019-01-01", "source": "pubmed"}
                    ],
                    "clinical_trials": [],
                    "journals": [
                        {"name": "Journal of emergency nursing", "date": "2019-01-01"}
                    ]
                }
            },
            "TETRACYCLINE": {
                "mentions": {
                    "pubmed": [
                        {"id": "2", "title": "Another sample title", "date": "2020-01-01", "source": "pubmed"}
                    ],
                    "clinical_trials": [],
                    "journals": [
                        {"name": "Journal of food protection", "date": "2020-01-01"}
                    ]
                }
            }
        }
        
        # Visualize using the vis-network helper.
        vis_network_viewer(results_dict, height=800)
        
        st.subheader("Raw JSON")
        st.json(results_dict)
