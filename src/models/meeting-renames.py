from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SpeakerSegment:

    speaker: str

    start: float

    end: float

    text: str



@dataclass
class Meeting:

    name: str

    start_time: datetime

    end_time: datetime | None = None

    transcript: str = ""

    summary: str = ""

    speaker_segments: list[SpeakerSegment] = field(
        default_factory=list
    )