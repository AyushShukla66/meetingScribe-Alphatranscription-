from pyannote.audio import Pipeline
from config.settings import HUGGINGFACE_TOKEN


def detect_speakers(audio_file):
    """
    Detect speakers from audio file.
    Returns speaker timestamps.
    """


    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=HUGGINGFACE_TOKEN
    )


    diarization = pipeline(audio_file)


    speakers = []


    for turn, _, speaker in diarization.itertracks(
        yield_label=True
    ):

        speakers.append(
            {
                "speaker": speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2)
            }
        )


    return speakers