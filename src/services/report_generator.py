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


    # Create reports folder
    Path("reports").mkdir(exist_ok=True)



    print(
        "Generating transcript..."
    )


    # Get exact Hinglish transcript
    transcript = transcribe_audio(
        "temp/meeting.wav"
    )


    print(
        "======== TRANSCRIPT ========"
    )

    print(transcript)

    print(
        "============================"
    )



    print(
        "Generating meeting summary..."
    )


    # Generate meeting report
    report_response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role": "system",

                "content": """

                You are a professional meeting report generator.

                Create a structured meeting report from the transcript.

                Generate only:

                1. Meeting Topic
                2. Key Points
                3. Action Items

                Rules:
                - Write the report in English.
                - Do not include the transcript in the summary.
                - Do not change technical terms.
                - Keep API, software names, company names unchanged.

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



    # Create Word document

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



    # AI Generated Report

    doc.add_heading(
        "Summary",
        level=2
    )


    doc.add_paragraph(
        meeting_report
    )



    # Original Transcript

    doc.add_heading(
        "Original Meeting Transcript",
        level=2
    )


    doc.add_paragraph(
        transcript
    )



    # Save DOCX

    filename = (
        f"reports/{meeting.name}.docx"
    )



    doc.save(filename)



    print(
        "DOCX FILE CREATED:",
        Path(filename).absolute()
    )



    return filename