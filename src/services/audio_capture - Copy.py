import sounddevice as sd
import soundfile as sf
import numpy as np

from datetime import datetime
from pathlib import Path

from models.meeting import Meeting
from services.logger import logger


current_meeting = None

recording = []

stream = None

samplerate = None
device_id = None
channels = None


# Create temp directory if it does not exist
Path("temp").mkdir(
    exist_ok=True
)


def get_best_microphone():
    """
    Detect and return the first available microphone device.
    """

    devices = sd.query_devices()

    selected = None

    print("\nAvailable Microphones:")

    for i, dev in enumerate(devices):

        if dev["max_input_channels"] > 0:

            print(
                i,
                "-",
                dev["name"]
            )

            if selected is None:
                selected = i


    if selected is None:
        raise Exception(
            "No microphone found."
        )


    device = sd.query_devices(
        selected
    )


    info = {
        "id": selected,
        "name": device["name"],
        "channels": min(
            device["max_input_channels"],
            2
        ),
        "samplerate": int(
            device["default_samplerate"]
        ),
    }


    print("\n==============================")
    print("Microphone Selected")
    print("==============================")
    print(
        "Name:",
        info["name"]
    )
    print(
        "Device ID:",
        info["id"]
    )
    print(
        "Channels:",
        info["channels"]
    )
    print(
        "SampleRate:",
        info["samplerate"]
    )
    print("==============================\n")


    return info



def audio_callback(indata, frames, time, status):
    """
    Receive audio data chunks.
    """

    if status:
        print(status)


    recording.append(
        indata.copy()
    )



def start_meeting(name):
    """
    Start meeting audio recording.
    """

    global current_meeting
    global stream
    global samplerate
    global device_id
    global channels


    # Clear previous audio data
    recording.clear()


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


        print(
            "Recording Started Successfully"
        )

        print(
            "Using:",
            mic["name"]
        )


        logger.info(
            f"Recording started using {mic['name']}"
        )


    except Exception as e:

        print(
            "Microphone error:"
        )

        print(e)


        raise Exception(
            "Could not open microphone."
        )


    return current_meeting



def stop_meeting():
    """
    Stop recording and save audio file.
    """

    global current_meeting
    global stream


    if current_meeting is None:

        raise Exception(
            "No active meeting found."
        )


    if stream:

        stream.stop()

        stream.close()

        stream = None



    if len(recording) == 0:

        raise Exception(
            "No audio recorded."
        )



    audio_data = np.concatenate(
        recording,
        axis=0
    )


    file_path = (
        "temp/meeting.wav"
    )


    sf.write(
        file_path,
        audio_data,
        samplerate
    )


    current_meeting.audio_file = file_path


    duration = (
        len(audio_data)
        /
        samplerate
    )


    print(
        "Audio saved:",
        file_path
    )

    print(
        "Audio duration:",
        round(duration, 2),
        "seconds"
    )


    current_meeting.end_time = datetime.now()


    logger.info(
        "Meeting Stopped"
    )


    # Clear old recording data
    recording.clear()


    return current_meeting