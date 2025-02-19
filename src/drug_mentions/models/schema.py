from typing import Any
from pydantic import BaseModel, root_validator, validator
from datetime import datetime

class Drug(BaseModel):
    atccode: str
    drug: str

class Publication(BaseModel):
    id: str
    title: str
    date: datetime
    journal: str

    @root_validator(pre=True)
    def use_scientific_title_if_title_missing(cls, values: dict) -> dict:
        if "title" not in values and "scientific_title" in values:
            values["title"] = values["scientific_title"]
        return values

    @validator("date", pre=True)
    def parse_date_field(cls, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        formats = [
            "%Y-%m-%d",    # different date formats
            "%d/%m/%Y",   
            "%d %B %Y",    
            "%d %b %Y",   
            "%B %d, %Y",   
            "%b %d, %Y"   
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                continue
        # Fall back to dateutil if available
        try:
            from dateutil import parser
            return parser.parse(value)
        except Exception as e:
            raise ValueError(f"Invalid date format: {value}") from e

class DrugMention(BaseModel):
    drug: str
    mentions: dict 
