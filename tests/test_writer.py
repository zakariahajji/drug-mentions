import json
from pathlib import Path
import pytest
from drug_mentions.pipeline.writer import DataWriter

def test_write_json(tmp_path: Path):
    # Sample data to write
    data = {
        "drug1": {
            "pubmed_mentions": [
                {"id": "P1", "title": "Test Title", "date": "01/01/2020", "journal": "Journal A"}
            ],
            "clinical_trials_mentions": [],
            "journals": ["Journal A"]
        },
        "drug2": {
            "pubmed_mentions": [],
            "clinical_trials_mentions": [
                {"id": "P2", "title": "Test Title 2", "date": "02/01/2020", "journal": "Journal B"}
            ],
            "journals": ["Journal B"]
        }
    }
    
    # Define output path within the temporary directory
    output_path = tmp_path / "output" / "mentions.json"
    
    # Write data using the DataWriter
    DataWriter.write_json(data, output_path)
    
    # Verify that the file exists
    assert output_path.exists(), "Output JSON file was not created."
    
    # Load the JSON file and compare with the original data
    with open(output_path, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == data, "Written JSON data does not match expected data."
