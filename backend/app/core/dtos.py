from dataclasses import dataclass
from datetime import datetime

@dataclass
class DocumentDetail:
    filename: str
    size: int
    type: str
    upload_date: datetime