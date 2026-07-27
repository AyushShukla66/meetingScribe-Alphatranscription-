from openai import OpenAI

from config.settings import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)


def generate_executive_brief(transcript):
    """
    Generate executive meeting brief from transcript.
    This function only creates summary.
    It does not modify the original transcript.
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an Executive Assistant.

Your task is ONLY to create an executive meeting brief.

The input transcript is an original voice transcript.

IMPORTANT:

- Never rewrite the transcript.
- Never clean the transcript.
- Never correct words.
- Never translate the transcript.
- Never change the meaning of spoken sentences.
- Use the transcript only as information for creating a summary.

Generate only these sections:

1. Executive Summary
2. Decisions
3. Action Items
4. Risks
5. Director Attention


Rules:

- Write the output in professional English.
- Use only information discussed in the meeting.
- Do not invent information.
- Do not add assumptions.
- Do not include the full transcript.
- Keep technical terms unchanged.
- Keep API names unchanged.
- Keep software names unchanged.
- Keep company names unchanged.
- Keep product names unchanged.
- Keep important numbers, dates, and names unchanged.
"""
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )


    executive_brief = (
        response
        .choices[0]
        .message
        .content
    )


    return executive_brief