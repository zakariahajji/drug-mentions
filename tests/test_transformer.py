import pytest
from datetime import datetime
from drug_mentions.models.schema import Drug, Publication
from drug_mentions.pipeline.transformer import DataTransformer

def create_publication(id: str, title: str, date_str: str, journal: str) -> Publication:
    """
    Create a Publication instance from given parameters.
    The date is parsed using a fixed format ("%d/%m/%Y") for testing.
    """
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    data = {
        "id": id,
        "title": title,
        "date": date_obj,
        "journal": journal,
    }
    return Publication.parse_obj(data)

def test_find_drug_mentions_default_source():
    """
    Test that when a publication doesn't have an explicit 'source',
    it is treated as coming from pubmed.
    """
    drugs = [
        Drug(atccode="D1", drug="Aspirin"),
        Drug(atccode="D2", drug="Ibuprofen")
    ]
    
    publications = [
        create_publication("P1", "Study on Aspirin efficacy", "01/01/2020", "Journal A"),
        # Publication that mentions "ibuprofen" (default source: pubmed)
        create_publication("P2", "Ibuprofen reduces inflammation", "02/01/2020", "Journal B"),
        # Publication that does not mention any of the drugs
        create_publication("P3", "A study on Paracetamol", "03/01/2020", "Journal C")
    ]
    
    transformer = DataTransformer()
    result = transformer.find_drug_mentions(drugs, publications)
    
    # Check that both drugs have mentions
    assert "Aspirin" in result
    assert "Ibuprofen" in result

    aspirin_mentions = result["Aspirin"]
    assert len(aspirin_mentions["pubmed_mentions"]) == 1
    assert aspirin_mentions["pubmed_mentions"][0]["id"] == "P1"
    assert aspirin_mentions["pubmed_mentions"][0]["date"] == "01/01/2020"
    assert "Journal A" in aspirin_mentions["journals"]
    
    ibuprofen_mentions = result["Ibuprofen"]
    assert len(ibuprofen_mentions["pubmed_mentions"]) == 1
    assert ibuprofen_mentions["pubmed_mentions"][0]["id"] == "P2"
    assert ibuprofen_mentions["pubmed_mentions"][0]["date"] == "02/01/2020"
    assert "Journal B" in ibuprofen_mentions["journals"]
