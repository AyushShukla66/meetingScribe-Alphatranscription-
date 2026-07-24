Based on our earlier discussion, use this **preferred installation setup** for MeetingScribe.

## Target Environment

Windows 11 Pro physical machine
Do not use Hyper-V VM for audio capture

---

# MeetingScribe Installation Steps

## 1. Install Python

Download:

[Python Downloads](https://www.python.org/downloads/?utm_source=chatgpt.com)

During installation:

☑ Add Python to PATH
☑ Install pip

Verify:

```powershell
python --version
pip --version
```

---

# 2. Create Project Folder

```powershell
mkdir C:\MeetingScribe
cd C:\MeetingScribe
```

Create:

```powershell
mkdir src,data,reports,logs,temp,assets,docs
```

---

# 3. Install Packages

```powershell
pip install streamlit
pip install openai
pip install python-docx
pip install soundcard
pip install soundfile
pip install numpy
pip install python-dotenv
```

---

# 4. Install FFmpeg

Download:

[FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/?utm_source=chatgpt.com)

Extract:

```
C:\ffmpeg
```

Verify:

```
C:\ffmpeg\bin\ffmpeg.exe
```

---

# 5. Create Environment File

Create:

```
C:\MeetingScribe\.env
```

Add:

```
OPENAI_API_KEY=your_key_here
```

---

# 6. Create Folder Structure

Final structure:

```
C:\MeetingScribe

│ .env
│
├── src
│   │ app.py
│   │ test_ai.py
│
│   ├──config
│   │   settings.py
│
│   ├──models
│   │   meeting.py
│
│   ├──services
│       ai_engine.py
│       audio_capture.py
│       logger.py
│       report_generator.py
│
├──data
├──reports
├──logs
├──temp
├──assets
└──docs
```

---

# 7. Run Application

From PowerShell:

```powershell
cd C:\MeetingScribe
python -m streamlit run src\app.py
```

---

# 8. First Test Flow

1. Open MeetingScribe
2. Enter Meeting Name
3. Start Meeting
4. Speak
5. Stop Meeting
6. Generate Executive Brief

Expected:

```
C:\MeetingScribe\reports\MeetingName.docx
```

---

# 9. Production Add-ons Later

Phase 2:

* Zoho Meeting integration
* Windows taskbar mini app
* Auto meeting detection
* Whisper transcription
* Executive dashboard
* Action tracking

Current status:
✅ AI engine done
✅ Report generation done
⏳ Audio capture pending on physical machine

Next step after installation on laptop:

**Test microphone capture.**

Extra usable 
Based on your previous work, your MeetingScribe is already working for:

✅ Microphone recording
✅ Hindi + English mixed transcription
✅ DOCX transcript generation

Now for **joining online meetings and generating transcripts**, do not change your working code immediately. Build it in phases.

I suggest this installation path:

---

# Phase 1: Capture Online Meeting Audio (Recommended First)

Goal:

```
Google Meet / Teams / Zoom
          |
          ↓
     Computer Audio
          +
     Your Microphone
          |
          ↓
   MeetingScribe
          |
          ↓
 Whisper Transcript
          |
          ↓
 DOCX File
```

---

## Step 1: Install Virtual Audio Cable

Install:

**VB-Audio Virtual Cable**

Download from:

[https://vb-audio.com/Cable/](https://vb-audio.com/Cable/)

Install:

```
VBCABLE_Setup_x64.exe
```

Restart your PC after installation.

---

## Step 2: Check New Audio Device

Open PowerShell:

```powershell
python
```

Then:

```python
import sounddevice as sd
print(sd.query_devices())
```

You should see something like:

```
CABLE Input
CABLE Output
Microphone
Speakers
```

---

## Step 3: Configure Meeting App Audio

For Google Meet / Teams / Zoom:

Go to:

```
Settings
   ↓
Audio
   ↓
Speaker
```

Change speaker to:

```
CABLE Input
```

Keep microphone as:

```
Your normal microphone
```

Example:

```
Speaker:
CABLE Input

Microphone:
Conexant HD Audio Microphone
```

Now:

Other people voice → goes into CABLE
Your voice → microphone

---

# Phase 2: Modify MeetingScribe Recording

Currently:

```
audio_capture.py
```

records only:

```
Microphone
```

We will add:

```
system_audio_capture.py
```

New structure:

```
src
 |
 ├── services
 │
 │    ├── audio_capture.py
 │    |
 │    ├── system_audio_capture.py   (new)
 │    |
 │    ├── transcription.py
 │    |
 │    └── report_generator.py
```

---

# Phase 3: Install Required Python Packages

Run:

```powershell
pip install sounddevice soundfile numpy
```

You already have most of these.

---

# Phase 4: Test Meeting Audio

Before coding, test:

Open YouTube:

Play any video.

Run:

```python
import sounddevice as sd

print(sd.query_devices())
```

Find:

```
CABLE Output
```

That is the meeting audio source.

---

# Phase 5: Add Speaker Identification (Later)

After audio capture works, add:

```
WhisperX
+
Pyannote
```

Then output becomes:

```
Speaker 1:
Hello everyone, आज हम meeting start करते हैं.

Speaker 2:
Yes, I have checked the report.

Speaker 1:
Okay, let's proceed.
```

---

# Your final architecture will become:

```
MeetingScribe

        Google Meet
             |
             |
       Virtual Cable
             |
             |
   +----------------+
   |                |
System Audio     Microphone
   |                |
   +----------------+
             |
             ↓
       Audio Recorder
             |
             ↓
        Whisper AI
             |
             ↓
       Raw Transcript
             |
             ↓
          DOCX
```

---

## Important

Do not remove your current working code.

Make a backup:

Copy:

```
C:\MeetingScribe\MeetingScribe
```

to:

```
C:\MeetingScribe\MeetingScribe_backup_working
```

Your current version is your stable checkpoint.

---

Next step after installing VB-Audio:

Send me the output of:

```powershell
python -c "import sounddevice as sd; print(sd.query_devices())"
```

Then I will tell you exactly which device ID to use in your `audio_capture.py`.


Error Troubleshooting In Scripting 

I understand. You want the **complete step-by-step history from the beginning** — the same way we solved the errors in MeetingScribe — including **what error happened, why it happened, and what we changed to fix it**.

Here is the complete troubleshooting path:

---

# MeetingScribe Complete Setup & Error Resolution Steps

## 1. Initial Error: FFmpeg Not Found

### Error:

```
FileNotFoundError: [WinError 2]
The system cannot find the file specified
```

and:

```
ffmpeg : The term 'ffmpeg' is not recognized
```

### Reason:

Your code used:

```python
pydub
```

to convert WAV → MP3.

`pydub` requires FFmpeg, but Windows could not find it.

---

## Solution:

Install FFmpeg:

```powershell
winget install Gyan.FFmpeg
```

Verify:

```powershell
winget list ffmpeg
```

Output:

```
FFmpeg Gyan.FFmpeg 8.1.2
```

Find location:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter ffmpeg.exe
```

You found:

```
C:\Users\finoadmin\AppData\Local\Microsoft\WinGet\Packages\
Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\
ffmpeg-8.1.2-full_build\bin\ffmpeg.exe
```

Added this in:

```
transcription.py
```

Code:

```python
AudioSegment.converter = r"YOUR_FFMPEG_PATH\ffmpeg.exe"
```

---

# 2. FFmpeg Encoding Error

### Error:

```
pydub.exceptions.CouldntEncodeError

ffmpeg returned error code:255
```

### Reason:

FFmpeg was installed, but your recording was creating very large files:

Example:

```
Original size: 4844.97 MB
Audio length: 405 minutes
```

Your code was recording:

```python
frames=int(8 * 60 * 60 * samplerate)
```

Meaning:

8 hours reserved.

It recorded:

* silence
* background noise
* empty time

---

# 3. Problem: Huge Audio Files

You said:

> I don't want it to generate chunks. I only want clear audio. When someone speaks, only that time should record.

The old method:

```
Record everything
        ↓
Save huge WAV
        ↓
Split chunks
        ↓
Transcribe
```

was changed.

New method:

```
Start recording
        ↓
Collect audio live
        ↓
Stop recording
        ↓
Save only actual meeting audio
        ↓
Transcribe
```

---

# 4. Updated audio_capture.py

Changed from:

```python
sd.rec()
```

to:

```python
sd.InputStream()
```

Reason:

`sd.rec()` reserves memory for the complete recording.

`InputStream()` records continuously in small pieces.

---

New flow:

```
Microphone
     |
     ↓
audio_callback()
     |
     ↓
recording list
     |
     ↓
stop_meeting()
     |
     ↓
meeting.wav
```

---

# 5. Microphone Error

### Error:

```
Exception: Could not open any microphone
```

### Reason:

Your microphone device selection was not stable.

Old code selected:

```
USB / Bluetooth / default
```

but Windows changed device IDs.

---

Solution:

Changed microphone detection:

```python
sd.query_devices()
```

and selected:

```
max_input_channels > 0
```

Now it detects:

Example:

```
Name:
Microsoft Sound Mapper - Input

Channels:
2

SampleRate:
44100
```

---

# 6. OpenAI Client Error

### Error:

```
NameError:
name 'client' is not defined
```

File:

```
ai_engine.py
```

Reason:

You used:

```python
client.chat.completions.create()
```

but never created:

```python
client = OpenAI()
```

---

Solution:

Added:

```python
from openai import OpenAI
from config.settings import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY
)
```

---

# 7. Transcript Generated in Wrong Language

### Problem:

Output:

```
䭐Ѓ 晦峸劭醥...
```

or:

Chinese-like characters.

---

Reason:

DOCX was opened incorrectly OR Whisper was not forced correctly.

---

Solution:

Changed transcription:

Before:

```python
model="whisper-1"
```

After:

```python
result = client.audio.transcriptions.create(
    model="whisper-1",
    file=file,
    language="en"
)
```

---

# 8. Wrong AI Summary Format

Old output:

```
Executive Summary

Decisions

Action Items
```

You wanted:

```
Whatever person speaks,
write exactly the same words.
```

Example:

Speaker says:

```
दिल जलों का दिल जला के क्या मिलेगा मेहरमा
I want to check the mic properly
मैंको स्क्रिप्टिंग भी टेस्ट करनी है
```

Transcript should be:

```
दिल जलों का दिल जला के क्या मिलेगा मेहरमा

I want to check the mic properly

मैंको स्क्रिप्टिंग भी टेस्ट करनी है
```

No rewriting.
No summary.
No translation.

---

# 9. Report File Generation

Your final flow became:

```
audio_capture.py

        ↓

temp/meeting.wav

        ↓

transcription.py

        ↓

Whisper

        ↓

report_generator.py

        ↓

Meeting_Name.docx
```

---

# 10. Current Working Status

Now your system can:

✅ Record microphone
✅ Stop recording
✅ Convert audio
✅ Send to Whisper
✅ Keep Hindi + English mixed words
✅ Generate transcript
✅ Create DOCX report

---

# Next Development Stage

Your next requirement:

> "Join Google Meet / Teams / Zoom and automatically create meeting transcript"

That requires adding:

```
System audio capture
+
Microphone capture
+
Speaker identification
```

It is the next phase after your current working version.

---

Keep this as your **MeetingScribe troubleshooting document**. It describes the exact journey from the first FFmpeg problem to your current working transcript system.
