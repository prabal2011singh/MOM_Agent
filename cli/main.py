import typer
import json
import os
from pathlib import Path
import glob
import sys

# Ensure local imports work regardless of where the script is called from
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recorder.recorder import AudioRecorder
from transcription.assemblyai_client import TranscriptionClient
from transcription.transcript_parser import parse_transcript
from summarizer.gemini_client import GeminiClient
from summarizer.mom_generator import generate_markdown

app = typer.Typer(help="AI-Powered Microsoft Teams Meeting Assistant (MVP)")

BASE_DIR = Path.cwd()
RECORDER = AudioRecorder(BASE_DIR)
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

@app.command()
def start():
    """Start recording system audio."""
    success, msg = RECORDER.start()
    if success:
        typer.echo(f"Starting recording... Saving to {msg}")
    else:
        typer.echo(msg)

@app.command()
def stop():
    """Stop the current recording."""
    success, msg = RECORDER.stop()
    if success:
        typer.echo(f"Recording stopped successfully. Audio saved to: {msg}")
    else:
        typer.echo(msg)

@app.command()
def process(file: str):
    """Process an audio file or 'latest' (Upload -> Transcribe -> Generate MOM)."""
    if file == "latest":
        recordings = glob.glob(str(BASE_DIR / "recordings" / "*.wav"))
        if not recordings:
            typer.echo("No recordings found.")
            raise typer.Exit()
        target_file = max(recordings, key=os.path.getctime)
    else:
        target_file = file

    if not os.path.exists(target_file):
        typer.echo(f"Error: File not found: {target_file}")
        raise typer.Exit()

    typer.echo(f"Processing audio file: {target_file}")
    
    file_stem = Path(target_file).stem
    transcript_json_path = OUTPUTS_DIR / f"{file_stem}_transcript.json"
    mom_json_path = OUTPUTS_DIR / f"{file_stem}_mom.json"
    mom_md_path = OUTPUTS_DIR / f"{file_stem}_mom.md"

    # Step 1: Upload & Transcription via AssemblyAI
    typer.echo("Step 1/3: Uploading & transcribing with AssemblyAI...")
    try:
        transcriber = TranscriptionClient()
        transcript = transcriber.transcribe(target_file)
    except Exception as e:
        typer.echo(f"Transcription failed: {e}")
        raise typer.Exit()

    # Step 2: Parse Transcript
    structured_transcript = parse_transcript(transcript)
    with open(transcript_json_path, "w") as f:
        json.dump(structured_transcript, f, indent=2)
    typer.echo(f"Transcript saved to {transcript_json_path}")

    # Step 3: Gemini MOM Generation
    typer.echo("Step 2/3: Generating MOM with Gemini...")
    try:
        gemini = GeminiClient()
        mom_json = gemini.generate_mom(structured_transcript)
    except Exception as e:
        typer.echo(f"MOM generation failed: {e}")
        raise typer.Exit()

    # Step 4: Save Outputs
    typer.echo("Step 3/3: Saving outputs...")
    with open(mom_json_path, "w") as f:
        json.dump(mom_json, f, indent=2)
        
    mom_md = generate_markdown(mom_json)
    with open(mom_md_path, "w") as f:
        f.write(mom_md)
        
    typer.echo(f"MOM generation complete! Saved to {mom_json_path} and {mom_md_path}")

if __name__ == "__main__":
    app()
