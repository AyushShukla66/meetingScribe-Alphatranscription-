import re

from pathlib import Path

from docx import Document
from openai import OpenAI

from config.settings import OPENAI_API_KEY
from services.transcription import transcribe_audio


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)


def generate_report(meeting):
    """
    Generate meeting report from recorded audio.
    """


    # Create reports folder
    Path("reports").mkdir(
        exist_ok=True
    )


    print(
        "Generating transcript..."
    )


    # Get exact transcript directly from audio

    transcript = transcribe_audio(
        "temp/meeting.wav"
    )


    print(
        "======== ORIGINAL TRANSCRIPT ========"
    )

    print(transcript)


    # Save raw transcript for checking
    # This does not modify the transcript

    with open(
        "temp/raw_transcript.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            transcript
        )


    print(
        "Raw transcript saved:"
    )

    print(
        "temp/raw_transcript.txt"
    )


    print(
        "====================================="
    )


    print(
        "Generating meeting summary..."
    )


    # Generate English meeting summary

    report_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a professional corporate meeting report generator.

Create a structured meeting report from the transcript.

Generate only:

1. Meeting Topic
2. Key Discussion Points
3. Decisions Made
4. Action Items


Rules:

- Write the report in professional English.
- Do not include the transcript.
- Do not modify the transcript.
- Do not rewrite spoken words.
- Only summarize the meeting content.
- Do not add information that was not discussed.
- Keep technical terms unchanged.
- Keep API names unchanged.
- Keep software names unchanged.
- Keep company names unchanged.
- Keep product names unchanged.
"""
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )


    meeting_report = (
        report_response
        .choices[0]
        .message
        .content
    )


    # Create DOCX file

    doc = Document()


    doc.add_heading(
        "Finodaya Capital",
        level=1
    )


    doc.add_heading(
        "Meeting Report",
        level=2
    )


    doc.add_paragraph(
        f"Meeting Name: {meeting.name}"
    )


    doc.add_paragraph(
        f"Start Time: {meeting.start_time}"
    )


    doc.add_paragraph(
        f"End Time: {meeting.end_time}"
    )


    # AI Generated Summary

    doc.add_heading(
        "Summary",
        level=2
    )


    doc.add_paragraph(
        meeting_report
    )


    # Original Voice Transcript

    doc.add_heading(
        "Original Voice Transcript",
        level=2
    )


    doc.add_paragraph(
        transcript
    )


    # Safe filename for Windows

    safe_name = re.sub(
        r'[\\/:*?"<>|]',
        "-",
        meeting.name
    )


    filename = (
        f"reports/{safe_name}.docx"
    )


    doc.save(
        filename
    )


    print(
        "DOCX FILE CREATED:",
        Path(filename).absolute()
    )


    return filename