import sounddevice as sd
import soundfile as sf

from datetime import datetime
from pathlib import Path
import numpy as np

from models.meeting import Meeting
from services.logger import logger


current_meeting = None
recording = []
stream = None
samplerate = None
device_id = None
channels = None

Path("temp").mkdir(exist_ok=True)


def get_best_microphone():

    devices = sd.query_devices()

    selected = None

    for i, dev in enumerate(devices):

        if dev["max_input_channels"] > 0:
            selected = i
            break

    if selected is None:
        raise Exception("No microphone found.")

    device = sd.query_devices(selected)

    info = {
        "id": selected,
        "name": device["name"],
        "channels": min(device["max_input_channels"], 2),
        "samplerate": int(device["default_samplerate"]),
    }

    print("\n==============================")
    print("Microphone Selected")
    print("==============================")
    print("Name:", info["name"])
    print("Device ID:", info["id"])
    print("Channels:", info["channels"])
    print("SampleRate:", info["samplerate"])
    print("==============================\n")

    return info



def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    recording.append(indata.copy())



def start_meeting(name):

    global current_meeting
    global stream
    global samplerate
    global device_id
    global channels
    global recording


    recording = []


    current_meeting = Meeting(
        name=name,
        start_time=datetime.now()
    )


    mic = get_best_microphone()

    device_id = mic["id"]
    samplerate = mic["samplerate"]
    channels = mic["channels"]


    try:

        stream = sd.InputStream(
            device=device_id,
            samplerate=samplerate,
            channels=channels,
            dtype="int16",
            callback=audio_callback
        )

        stream.start()

        print("Recording Started Successfully")
        print("Using:", mic["name"])

        logger.info(
            f"Recording started using {mic['name']}"
        )


    except Exception as e:

        print("Microphone error:")
        print(e)

        raise Exception(
            "Could not open microphone."
        )


    return current_meeting




def stop_meeting():

    global current_meeting
    global stream
    global recording


    if stream:

        stream.stop()
        stream.close()


    if len(recording) > 0:

        audio_data = np.concatenate(
            recording,
            axis=0
        )


        sf.write(
            "temp/meeting.wav",
            audio_data,
            samplerate
        )


        current_meeting.audio_file = "temp/meeting.wav"


    current_meeting.end_time = datetime.now()


    logger.info(
        "Meeting Stopped"
    )


    return current_meeting