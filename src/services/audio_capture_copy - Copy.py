import sounddevice as sd
import soundfile as sf
from datetime import datetime
from pathlib import Path

from models.meeting import Meeting
from services.logger import logger

current_meeting = None
recording = None
samplerate = 44100
sd.default.device = 12

Path("temp").mkdir(exist_ok=True)


def start_meeting(name):

    global current_meeting
    global recording

    current_meeting = Meeting(
        name=name,
        start_time=datetime.now()
    )

    recording = sd.rec(
        int(300 * samplerate),
        samplerate=samplerate,
        channels=2,
        dtype="int16",
        device=(12, 3)
    )

    logger.info(f"Meeting Started : {name}")

    return current_meeting


def stop_meeting():

    global current_meeting
    global recording

    sd.stop()

    sf.write(
        "temp/meeting.wav",
        recording,
        samplerate
    )

    current_meeting.end_time = datetime.now()

    logger.info("Meeting Stopped")

    return current_meeting