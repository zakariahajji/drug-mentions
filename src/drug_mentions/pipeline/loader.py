import re
import pandas as pd
import json
from pathlib import Path
from typing import List
from datetime import datetime
from drug_mentions.models.schema import Drug, Publication

def parse_date(date_str: str) -> datetime:
    """
    try multiple date formats and return a datetime object.
    Raises ValueError if the date cannot be parsed.
    """
    if not isinstance(date_str, str):
        raise ValueError(f"Expected string date, got {type(date_str)}: {date_str}")
        
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
    """
    Load a CSV and convert the specified date column using parse_date.
    Handles encoding issues and ensures proper date parsing.
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
        
    if date_column not in df.columns:
        raise ValueError(f"Date column '{date_column}' not found in {file_path}")
        
    df[date_column] = df[date_column].apply(parse_date)
    return df

class DataLoader:
    def __init__(self, data_dir: str):
        """Initialize the DataLoader with the data directory path."""
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load_drugs(self) -> List[Drug]:
        """
        Load drugs data from CSV file.
        Returns a list of Drug objects.
        """
        file_path = self.data_dir / "drugs.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Drugs file not found: {file_path}")
            
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            return [Drug(**row.to_dict()) for _, row in df.iterrows()]
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin1')
            return [Drug(**row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            raise Exception(f"Error loading drugs from {file_path}: {str(e)}")

    def load_pubmed(self) -> List[Publication]:
        """
        Load PubMed publications from both CSV and JSON files.
        Returns a list of Publication objects with source='pubmed'.
        """
        publications = []
        
        # Load pumed csv
        csv_path = self.data_dir / "pubmed.csv"
        if csv_path.exists():
            try:
                df_csv = load_csv_with_date(csv_path, date_column="date")
                df_csv['source'] = 'pubmed'  # add source information
                publications.extend(
                    [Publication(**row.to_dict()) for _, row in df_csv.iterrows()]
                )
            except Exception as e:
                raise Exception(f"Error loading pubmed CSV from {csv_path}: {str(e)}")
        
        # Load PubMed JSON
        json_path = self.data_dir / "pubmed.json"
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8-sig") as f:
                    content = f.read().strip()
                    
                if not content:
                    raise ValueError("pubmed.json is empty")
                    
                # Clean JSON content (remove trailing commas)
                content = re.sub(r',\s*\]', ']', content)
                
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
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
                
                for item in data:
                    item['date'] = parse_date(item['date'])
                    item['source'] = 'pubmed'  # Add source information
                publications.extend([Publication(**item) for item in data])
                
            except Exception as e:
                raise Exception(f"Error loading pubmed JSON from {json_path}: {str(e)}")
        
        if not publications:
            raise ValueError("No PubMed publications found in either CSV or JSON format")
            
        return publications

    def load_clinical_trials(self) -> List[Publication]:
        """
        Load clinical trials data from CSV file.
        Returns a list of Publication objects with source='clinical_trial'.
        """
        file_path = self.data_dir / "clinical_trials.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Clinical trials file not found: {file_path}")
            
        try:
            df = load_csv_with_date(file_path, date_column="date")
            df['source'] = 'clinical_trial'  
            return [Publication(**row.to_dict()) for _, row in df.iterrows()]
        except Exception as e:
            raise Exception(f"Error loading clinical trials from {file_path}: {str(e)}")