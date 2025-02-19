import streamlit as st
import pandas as pd
import json
import tempfile
from pathlib import Path

# Import your pipeline components (adjust the import paths as needed)
from drug_mentions.pipeline.loader import DataLoader
from drug_mentions.pipeline.transformer import DataTransformer
from drug_mentions.pipeline.writer import DataWriter

from utils.d3_viewer import d3_viewer

st.set_page_config(layout="wide")
st.title("Drug mentions finder with data viz!")

col_left, col_right = st.columns([1, 1])

def save_uploaded_file(uploaded_file, save_path: Path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getvalue())

with col_left:
    st.header("Upload CSV Files")
    clinical_file = st.file_uploader("Clinical Trials CSV", type=["csv"])
    drugs_file = st.file_uploader("Drugs CSV", type=["csv"])
    pubmed_file = st.file_uploader("PubMed CSV", type=["csv"])
    process_button = st.button("Process")

with col_right:
    st.header("Visualization")

if process_button:
    if clinical_file is None or drugs_file is None or pubmed_file is None:
        st.warning("Please upload all three CSV files before processing.")
    else:
        # Create a temporary directory for the pipeline input/output
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmp_dir = Path(tmpdirname)
            input_dir = tmp_dir / "input"
            output_dir = tmp_dir / "output"
            input_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded files in the "input" folder with expected filenames
            save_uploaded_file(clinical_file, input_dir / "clinical_trials.csv")
            save_uploaded_file(drugs_file, input_dir / "drugs.csv")
            save_uploaded_file(pubmed_file, input_dir / "pubmed.csv")
            # Note: If you also use pubmed.json, add similar logic here.

            # Run the pipeline:
            # 1. Load data using DataLoader
            loader = DataLoader(str(input_dir))
            drugs_list = loader.load_drugs()
            pubmed_publications = loader.load_pubmed()
            clinical_publications = loader.load_clinical_trials()
            all_publications = pubmed_publications + clinical_publications

            # 2. Transform data to generate mentions mapping
            transformer = DataTransformer()
            mentions_dict = transformer.find_drug_mentions(drugs_list, all_publications)

            # 3. Write output JSON using DataWriter
            output_file = output_dir / "drug_mentions.json"
            writer = DataWriter()
            writer.write_json(mentions_dict, output_file)

            # Read the output JSON back as a dictionary
            with open(output_file, "r") as f:
                results_dict = json.load(f)

            # Visualize using the vis-network viewer
            d3_viewer(results_dict, height=800)

            st.subheader("Raw JSON")
            st.json(results_dict)
