import sounddevice as sd
import soundfile as sf
import numpy as np

from datetime import datetime
from pathlib import Path

from models.meeting import Meeting
from services.logger import logger


current_meeting = None
recording = None

samplerate = 44100
DEVICE_ID = 1   # Microphone (AB13X USB Audio), MME

Path("temp").mkdir(exist_ok=True)


def start_meeting(name):

    global current_meeting
    global recording

    print("CHECK DEVICE:")
    print(sd.query_devices(DEVICE_ID))

    current_meeting = Meeting(
        name=name,
        start_time=datetime.now()
    )

    try:

        recording = sd.rec(
            frames=int(300 * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="int16",
            device=DEVICE_ID,
            blocking=False
        )

        print("RECORDING STARTED")

    except Exception as e:
        print("AUDIO ERROR:")
        print(e)
        raise e


    logger.info(f"Meeting Started : {name}")

    return current_meeting



def stop_meeting():

    global current_meeting
    global recording

    sd.stop()

    if recording is not None:

        sf.write(
            "temp/meeting.wav",
            recording,
            samplerate
        )


    current_meeting.end_time = datetime.now()

    logger.info("Meeting Stopped")

    return current_meeting