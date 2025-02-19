import json
from pathlib import Path
from typing import Dict, Any

class DataWriter:
    @staticmethod
    def write_json(data: Dict[str, Any], output_path: Path) -> None:
        """
        Write data to a JSON file.
        
        Args:
            data: Dictionary containing the drug mentions data
            output_path: Path where the JSON file will be written
        """
        # Create output directory 
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            raise Exception(f"Error writing to {output_path}: {str(e)}")