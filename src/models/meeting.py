from dataclasses import dataclass
from datetime import datetime

@dataclass
class Meeting:
    name: str
    start_time: datetime
    end_time: datetime | None = None
    transcript: str = ""
    summary: str = ""