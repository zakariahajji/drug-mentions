import pytest
from pathlib import Path
from drug_mentions.pipeline.loader import DataLoader, parse_date
from drug_mentions.models.schema import Publication

# Fixture to create a temporary data directory structure
@pytest.fixture
def temp_data_dir(tmp_path: Path) -> Path:
    data_input = tmp_path / "data" / "input"
    data_input.mkdir(parents=True, exist_ok=True)
    return data_input

def test_publication_root_validator():
    """
    Test that Publication uses 'scientific_title' when 'title' is missing.
    """
    data = {
        "id": "123",
        "scientific_title": "A Study on X",
        "date": "1 January 2020",
        "journal": "Test Journal"
    }
    pub = Publication(**data)
    assert pub.title == "A Study on X"

def test_load_clinical_trials(temp_data_dir: Path):
    """
    Create a sample clinical_trials.csv file and test that DataLoader loads it correctly,
    converting 'scientific_title' into the required 'title' field.
    """
    # Create sample CSV data; note that clinical trials use 'scientific_title'
    sample_csv = (
        "id,scientific_title,date,journal\n"
        "NCT01967433,\"Use of Diphenhydramine as an Adjunctive Sedative\",\"1 January 2020\",\"Journal of emergency nursing\"\n"
        "NCT04189588,\"Phase 2 Study of Something\",\"25/05/2020\",\"Journal of emergency nursing\"\n"
    )
    csv_path = temp_data_dir / "clinical_trials.csv"
    csv_path.write_text(sample_csv, encoding="utf-8")
    
    # Initialize DataLoader with the temporary input directory
    loader = DataLoader(str(temp_data_dir))
    
    # Load clinical trials data
    publications = loader.load_clinical_trials()
    assert len(publications) == 2
    for pub in publications:
        # The root validator should have provided a title (from 'scientific_title')
        assert pub.title.strip() != ""
        # Also check that the date was parsed correctly (as datetime)
        assert isinstance(pub.date, type(parse_date("1 January 2020")))
