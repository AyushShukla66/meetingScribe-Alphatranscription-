import os
import time

from openai import OpenAI

from config.settings import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)


def transcribe_audio(audio_file):
    """
    Generate raw verbatim Roman Hindi + English transcript from audio.
    """

    if not os.path.exists(audio_file):
        raise FileNotFoundError(audio_file)


    print(
        "Uploading audio for transcription..."
    )


    for attempt in range(3):

        try:

            with open(audio_file, "rb") as file:

                result = client.audio.transcriptions.create(
                    model="gpt-4o-transcribe",
                    file=file,
                    prompt="""
You are a RAW VERBATIM speech-to-text transcription engine.

Your ONLY job:

Convert the speaker's voice into text exactly as spoken.

The final transcript must look like a chat message created from the person's voice.


The speaker can speak:

- Hindi
- English
- Hinglish (Hindi + English mix)


==================================================

MOST IMPORTANT RULE:

The final output MUST ALWAYS be:

Roman Hindi + English mix.

NEVER return Hindi Devanagari script.

Example:

Wrong:

"तू जाने ना, तू जाने ना"


Correct:

"Tu jaane na, tu jaane na"


==================================================


STRICT VERBATIM RULES:

- Write every spoken word.
- Do not remove any word.
- Do not add any word.
- Keep repeated words.
- Keep repeated sentences.
- Keep self corrections.
- Keep mistakes.
- Keep pronunciation mistakes.
- Keep grammar mistakes.
- Keep filler words.
- Keep slang.
- Keep incomplete sentences.


If speaker says:

"sorry sorry sorry"

Output:

"sorry sorry sorry"


If speaker repeats a line:

"Jay Jay Siyaram, Jay Jay Siyaram"

Do NOT reduce it to:

"Jay Siyaram"


Keep every repetition.


==================================================


DO NOT:

- Do not summarize.
- Do not explain.
- Do not rewrite.
- Do not correct grammar.
- Do not improve sentences.
- Do not make professional sentences.
- Do not guess missing words.
- Do not replace unclear words.
- Do not remove repeated words.
- Do not translate.


==================================================


LANGUAGE RULES:


Hindi:

- If Hindi is spoken in Devanagari script, convert it into Roman Hindi.
- Change ONLY the script.
- Do NOT change the words.
- Do NOT translate Hindi into English.


English:

- Keep English words exactly as spoken.
- Do not translate English words.
- Keep technical words unchanged.


Hinglish:

- Maintain natural Hindi + English mixing.
- Keep the same order of words.


Keep unchanged:

- Software names.
- API names.
- Company names.
- Product names.
- Technical terms.


==================================================


EXAMPLES:


Speaker:

"जय सियाराम, जय सियाराम, मैं अभी टेस्ट कर रहा हूँ"


Transcript:

"Jay Siyaram, Jay Siyaram, main abhi test kar raha hoon"



--------------------------------------------------


Speaker:

"तू जाने ना, तू जाने ना, मिलके भी हम ना मिले तुम से ना जाने क्यों"


Transcript:

"Tu jaane na, tu jaane na, milke bhi hum na mile tum se na jaane kyun"



--------------------------------------------------


Speaker:

"ऐसा जैसा मैं बोलता जाऊँ, वैसा वैसा उसको transcript करते जाओ, यानी कि मेरी voice को chats में लिख दो"


Transcript:

"Jaisa jaisa main bolta jaaun, waisa waisa usko transcript karte jao, yani ki meri voice ko chats mein likh do"



--------------------------------------------------


Speaker:

"I want to tell that कि मुझे ये chats इसी formation में चाहिए"


Transcript:

"I want to tell that ki mujhe ye chats isi formation mein chahiye"



--------------------------------------------------


Speaker:

"i dont know wha to do i don knwo what to do aab age kya karu"


Transcript:

"i dont know wha to do i don knwo what to do aab age kya karu"



--------------------------------------------------


Speaker:

"i wnat to do theis code for tensing so ham iska use apni cpanmy me kar skate"


Transcript:

"i wnat to do theis code for tensing so ham iska use apni cpanmy me kar skate"



==================================================


FINAL RULE:

Return ONLY the transcript.

No explanation.
No summary.
No formatting.
"""
                )


            print(
                "Transcription completed"
            )


            return result.text


        except Exception as e:

            print(
                "Transcription failed attempt:",
                attempt + 1
            )

            print(e)

            time.sleep(5)


    raise Exception(
        "Transcription failed after retries."
    )