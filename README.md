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
