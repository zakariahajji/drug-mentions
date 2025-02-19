import pandas as pd
import json
from pathlib import Path
from typing import List
from datetime import datetime
from drug_mentions.models.schema import Drug, Publication

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
    
    def load_drugs(self) -> List[Drug]:
        file_path = self.data_dir / "drugs.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Drugs file not found: {file_path}")
            
        try:
            df = pd.read_csv(file_path)
            return [Drug(**row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            raise Exception(f"Error loading drugs from {file_path}: {str(e)}")
    
    def load_pubmed(self) -> List[Publication]:
        publications = []
        
        # Load CSV
        csv_path = self.data_dir / "pubmed.csv"
        if csv_path.exists():
            try:
                df_csv = pd.read_csv(csv_path)
                df_csv['date'] = pd.to_datetime(df_csv['date'])
                publications.extend([Publication(**row.to_dict()) for _, row in df_csv.iterrows()])
            except Exception as e:
                raise Exception(f"Error loading pubmed CSV from {csv_path}: {str(e)}")
        
        # Load JSON
        json_path = self.data_dir / "pubmed.json"
        if json_path.exists():
            try:
                with open(json_path) as f:
                    data = json.load(f)
                for item in data:
                    item['date'] = datetime.strptime(item['date'], '%d/%m/%Y')
                publications.extend([Publication(**item) for item in data])
            except Exception as e:
                raise Exception(f"Error loading pubmed JSON from {json_path}: {str(e)}")
        
        return publications
    
    def load_clinical_trials(self) -> List[Publication]:
        file_path = self.data_dir / "clinical_trials.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Clinical trials file not found: {file_path}")
            
        try:
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'])
            return [Publication(**row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            raise Exception(f"Error loading clinical trials from {file_path}: {str(e)}")