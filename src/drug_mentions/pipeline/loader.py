import re
import pandas as pd
import json
from pathlib import Path
from typing import List
from datetime import datetime
from drug_mentions.models.schema import Drug, Publication

def parse_date(date_str: str) -> datetime:
    """Try multiple date formats and return a datetime object."""
    date_str = date_str.strip()
    formats = [
        '%Y-%m-%d',    
        '%d/%m/%Y',    
        '%d %B %Y',    
        '%d %b %Y',    
        '%B %d, %Y',   
        '%b %d, %Y'  
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    try:
        from dateutil import parser
        return parser.parse(date_str)
    except Exception:
        raise ValueError(f"Unknown date format: {date_str}")

def load_csv_with_date(file_path: Path, date_column: str = "date") -> pd.DataFrame:
    """Load a CSV and convert the specified date column using parse_date."""
    df = pd.read_csv(file_path)
    df[date_column] = df[date_column].apply(parse_date)
    return df

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
        
        # try to looad pubmed CSV 
        csv_path = self.data_dir / "pubmed.csv"
        if csv_path.exists():
            try:
                df_csv = load_csv_with_date(csv_path, date_column="date")
                publications.extend(
                    [Publication(**row.to_dict()) for _, row in df_csv.iterrows()]
                )
            except Exception as e:
                raise Exception(f"Error loading pubmed CSV from {csv_path}: {str(e)}")
        
        # Load pubmed Json
        json_path = self.data_dir / "pubmed.json"
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8-sig") as f:
                    content = f.read().strip()
                if not content:
                    raise ValueError("pubmed.json is empty")
                # remove trailing commas from arrays ( json problem )
                content = re.sub(r',\s*\]', ']', content)
                try:
                    # try parsing the whole file as a json array.
                    data = json.loads(content)
                except json.JSONDecodeError:
                    # Fallback: treat file as NDJSON (one json object per line)
                    data = []
                    lines = content.splitlines()
                    for i, line in enumerate(lines, start=1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data.append(json.loads(line))
                        except json.JSONDecodeError as nd_e:
                            raise Exception(
                                f"Error parsing JSON on line {i} of {json_path}: {nd_e}"
                            ) from nd_e
                # Parse dates for each item
                for item in data:
                    item['date'] = parse_date(item['date'])
                publications.extend([Publication(**item) for item in data])
            except Exception as e:
                raise Exception(f"Error loading pubmed JSON from {json_path}: {str(e)}")
        
        return publications
    
    def load_clinical_trials(self) -> List[Publication]:
        file_path = self.data_dir / "clinical_trials.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Clinical trials file not found: {file_path}")
        try:
            df = load_csv_with_date(file_path, date_column="date")
            return [Publication(**row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            raise Exception(f"Error loading clinical trials from {file_path}: {str(e)}")
