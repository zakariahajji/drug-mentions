from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Drug(BaseModel):
    atccode: str
    drug: str

class Publication(BaseModel):
    id: str
    title: str
    date: datetime
    journal: str

class DrugMention(BaseModel):
    drug: str
    mentions: dict