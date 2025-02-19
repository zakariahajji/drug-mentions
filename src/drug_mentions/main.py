from pathlib import Path

from drug_mentions.pipeline.loader import DataLoader
from drug_mentions.pipeline.transformer import DataTransformer
from drug_mentions.pipeline.writer import DataWriter


def main():
    print("Drug Mention Finder")
    # Set up paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "input"
    output_dir = base_dir / "data" / "output"
    output_file = output_dir / "drug_mentions.json"

    try:
        # Init loader
        loader = DataLoader(data_dir)

        # Load data
        print("Loading drugs...")
        drugs = loader.load_drugs()
        print(f"Loaded {len(drugs)} drugs")

        print("Loading publications...")
        pubmed_pubs = loader.load_pubmed()
        clinical_trials = loader.load_clinical_trials()
        all_publications = pubmed_pubs + clinical_trials
        print(f"Loaded {len(all_publications)} publications")

        # Transform data
        print("Finding drug mentions...")
        transformer = DataTransformer()
        mentions = transformer.find_drug_mentions(drugs, all_publications)
        print(f"Found mentions for {len(mentions)} drugs")

        # Write results
        print("Writing results...")
        writer = DataWriter()
        writer.write_json(mentions, output_file)
        print(f"Results written to {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
