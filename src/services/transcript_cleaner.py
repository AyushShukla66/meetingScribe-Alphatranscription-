from openai import OpenAI
from config.settings import OPENAI_API_KEY



client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)



def clean_transcript(raw_transcript):


    response = client.chat.completions.create(

        model="gpt-4o-mini",


        messages=[


            {


                "role":"system",


                "content":"""

You are a Hinglish transcript cleaner.

Your job is ONLY to clean the transcript.

Rules:

- Keep Hinglish exactly as spoken.
- Do NOT translate into English.
- Do NOT convert Hindi words into English.
- Do NOT summarize.
- Do NOT change sentence meaning.
- Do NOT make it formal.
- Keep English technical words unchanged.
- Remove unnecessary filler words like:
  umm, hmm, acha, matlab (only if they do not add meaning).

Maintain Roman Hindi style.

Example:

Input:

humko is tool ke baare mein discuss karna hai ki humko isko organization mein deploy karna hai ya nahi.

Output:

humko is tool ke baare mein discuss karna hai ki humko isko organization mein deploy karna hai ya nahi.


Another example:

Input:

aaj hum API integration discuss karenge aur fir deployment ka flow dekhenge.

Output:

aaj hum API integration discuss karenge aur fir deployment ka flow dekhenge.


Return only cleaned Hinglish transcript.

"""


            },


            {


                "role":"user",

                "content": raw_transcript

            }

        ]

    )


    return (
        response
        .choices[0]
        .message
        .content
    )