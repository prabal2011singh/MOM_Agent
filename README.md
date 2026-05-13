# AI-Powered Microsoft Teams Meeting Assistant (MVP)

A lightweight, reliable, and production-style MVP that records your Microsoft Teams meetings locally and generates a structured Minutes of Meeting (MOM) document using Cloud AI APIs.

This project is built for **macOS (Apple Silicon / Intel)** and bypasses heavy local machine learning setups by using a **Hybrid Architecture**:
- **Local:** Audio recording via FFmpeg and BlackHole.
- **Cloud:** Transcription & Speaker Diarization via AssemblyAI, and MOM Generation via Google Gemini.

---

## 🏗 Architecture Overview

```text
            Microsoft Teams Meeting
                       ↓
              Local Audio Recording (BlackHole + FFmpeg)
                       ↓
         Upload Audio to AssemblyAI API
                       ↓
        Speaker-aware Transcript Generation
                       ↓
             Structured Transcript JSON
                       ↓
              Gemini MOM Generation
                       ↓
           Markdown / JSON MOM Output
```

---

## ⚙️ Prerequisites & Setup

### 1. System Dependencies (macOS)
You need **FFmpeg** to record audio and **BlackHole** to route system audio. Install both using Homebrew:

```bash
brew install ffmpeg
brew install blackhole-2ch
```

*Note: In Microsoft Teams, ensure your Output/Speaker device is set to "BlackHole 2ch" or a Multi-Output Device that includes BlackHole so the assistant can "hear" the meeting.*

### 2. Python Environment Setup
It is highly recommended to use a virtual environment.

```bash
cd meeting-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. API Keys (.env)
Create a `.env` file in the root of the project and add your API keys:

```ini
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🚀 How to Use the CLI

The entire workflow is orchestrated through a simple Command Line Interface (CLI). 

### Step 1: Record a Meeting
When you join your Microsoft Teams meeting, start the recording:
```bash
python3 cli/main.py start
```
*The assistant runs in the background and records system audio into the `recordings/` folder.*

### Step 2: Stop the Recording
Once the meeting is over, stop the recording process:
```bash
python3 cli/main.py stop
```
*This safely stops FFmpeg and saves your `.wav` file.*

### Step 3: Process the Audio & Generate MOM
To automatically upload the audio, transcribe the speakers, and generate the final MOM markdown document, simply run:
```bash
python3 cli/main.py process latest
```

Alternatively, if you want to process a specific old recording, pass the file path:
```bash
python3 cli/main.py process recordings/meeting_20260511_234945.wav
```

---

## 📂 Project Outputs

Once the processing is complete, you will find the generated files inside the `outputs/` directory:
- `meeting_TIMESTAMP_transcript.json` - The raw speaker-separated transcript.
- `meeting_TIMESTAMP_mom.json` - The structured JSON metadata of the meeting.
- `meeting_TIMESTAMP_mom.md` - The **final human-readable Minutes of Meeting** containing:
  - Meeting Summary
  - Key Discussion Points
  - Decisions
  - Action Items (with Owners and Deadlines)
  - Risks / Blockers

*(Note: System audio recording via BlackHole still needs to happen on your host machine, as Docker for Mac cannot easily capture local macOS system audio hardware.)*
