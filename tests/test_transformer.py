from datetime import datetime

import pytest

from drug_mentions.models.schema import Drug, Publication
from drug_mentions.pipeline.transformer import DataTransformer


def create_publication(
    id: str, title: str, date: str, journal: str, source: str = "pubmed"
):
    """Helper function to create a Publication instance for testing."""
    data = {
        "id": id,
        "title": title,
        "date": date,
        "journal": journal,
        "source": source,
    }
    return Publication.parse_obj(data)


def test_publication_root_validator():
    """Test that Publication uses 'scientific_title' when 'title' is missing."""
    data = {
        "id": "123",
        "scientific_title": "A Study on X",
        "date": "1 January 2020",
        "journal": "Test Journal",
        "source": "pubmed",  # Add default source
    }
    pub = Publication(**data)
    assert pub.title == "A Study on X"


def test_find_drug_mentions_default_source():
    """
    Test that when a publication doesn't have an explicit 'source',
    it is treated as coming from pubmed.
    """
    drugs = [Drug(atccode="D1", drug="Aspirin"), Drug(atccode="D2", drug="Ibuprofen")]

    publications = [
        create_publication(
            "P1", "Study on Aspirin efficacy", "01/01/2020", "Journal A"
        ),
        create_publication(
            "P2", "Ibuprofen reduces inflammation", "02/01/2020", "Journal B"
        ),
        create_publication("P3", "A study on Paracetamol", "03/01/2020", "Journal C"),
    ]

    transformer = DataTransformer()
    result = transformer.find_drug_mentions(drugs, publications)

    # Check that both drugs have mentions
    assert "Aspirin" in result
    assert "Ibuprofen" in result

    # Check mentions structure
    aspirin_mentions = result["Aspirin"]["mentions"]
    ibuprofen_mentions = result["Ibuprofen"]["mentions"]

    # Verify pubmed mentions
    assert len(aspirin_mentions["pubmed"]) == 1
    assert len(ibuprofen_mentions["pubmed"]) == 1

    # Verify details of mentions
    assert aspirin_mentions["pubmed"][0]["title"] == "Study on Aspirin efficacy"
    assert ibuprofen_mentions["pubmed"][0]["title"] == "Ibuprofen reduces inflammation"

    # Verify journals are captured
    assert "Journal A" in [j["name"] for j in aspirin_mentions["journals"]]
    assert "Journal B" in [j["name"] for j in ibuprofen_mentions["journals"]]
