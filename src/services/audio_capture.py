import sounddevice as sd
import soundfile as sf
import numpy as np

import threading
from datetime import datetime
from pathlib import Path

from models.meeting import Meeting
from services.logger import logger


# Current meeting object
current_meeting = None


# Audio storage
recording = []

# Thread lock for audio data safety
recording_lock = threading.Lock()


# Stream variables
stream = None

samplerate = None
device_id = None
channels = None


# Create temp folder
Path("temp").mkdir(
    exist_ok=True
)



def get_best_microphone():
    """
    Detect best available microphone.
    """

    devices = sd.query_devices()

    selected = None


    print("\nAvailable Microphones:")


    for index, device in enumerate(devices):

        if device["max_input_channels"] > 0:

            print(
                index,
                "-",
                device["name"]
            )

            if selected is None:
                selected = index



    if selected is None:

        raise Exception(
            "No microphone found."
        )



    device_info = sd.query_devices(
        selected
    )


    max_channels = device_info["max_input_channels"]


    selected_channels = min(
        max_channels,
        2
    )


    possible_rates = [
        int(device_info["default_samplerate"]),
        48000,
        44100,
        32000,
        16000
    ]


    working_rate = None


    for rate in possible_rates:

        try:

            sd.check_input_settings(
                device=selected,
                channels=selected_channels,
                samplerate=rate,
                dtype="int16"
            )

            working_rate = rate

            break


        except Exception:

            continue



    if working_rate is None:

        raise Exception(
            "No supported sample rate found."
        )



    return {

        "id": selected,

        "name": device_info["name"],

        "channels": selected_channels,

        "samplerate": working_rate

    }





def audio_callback(indata, frames, time, status):
    """
    Receives audio chunks from microphone.
    """


    if status:

        print(
            "Audio status:",
            status
        )



    with recording_lock:

        recording.append(
            indata.copy()
        )







def start_meeting(name):
    """
    Start microphone recording.
    """


    global current_meeting
    global stream
    global samplerate
    global device_id
    global channels



    with recording_lock:

        recording.clear()



    current_meeting = Meeting(
        name=name,
        start_time=datetime.now()
    )



    mic = get_best_microphone()



    device_id = mic["id"]

    samplerate = mic["samplerate"]

    channels = mic["channels"]



    print("\n==============================")
    print("Microphone Selected")
    print("==============================")
    print("Name:", mic["name"])
    print("Device:", device_id)
    print("Channels:", channels)
    print("Sample Rate:", samplerate)
    print("==============================\n")




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
            "Recording Started"
        )


        logger.info(
            f"Recording started: {mic['name']}"
        )



    except Exception as error:


        logger.error(
            f"Recording start failed: {error}"
        )


        raise Exception(
            "Could not start microphone recording."
        )



    return current_meeting







def stop_meeting():
    """
    Stop recording and save WAV file.
    """


    global current_meeting
    global stream



    if current_meeting is None:

        raise Exception(
            "No active meeting."
        )




    if stream is not None:


        # Stop accepting new audio

        stream.stop()

        stream.close()

        stream = None




    # Small safety delay
    # allows final callback data to arrive

    sd.sleep(200)




    with recording_lock:

        if len(recording) == 0:

            raise Exception(
                "No audio recorded."
            )


        audio_data = np.concatenate(
            recording,
            axis=0
        )



        recording.clear()



    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    file_path = (
        f"temp/meeting_{timestamp}.wav"
    )



    sf.write(
        file_path,
        audio_data,
        samplerate
    )



    duration = (
        len(audio_data)
        /
        samplerate
    )



    current_meeting.end_time = datetime.now()



    # Keep compatibility with your existing code
    current_meeting.audio_file = file_path



    print(
        "\nAudio Saved:",
        file_path
    )


    print(
        "Duration:",
        round(duration, 2),
        "seconds"
    )



    logger.info(
        f"Meeting stopped. Audio saved: {file_path}"
    )



    return current_meeting