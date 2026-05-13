import assemblyai as aai
from config.settings import ASSEMBLYAI_API_KEY

if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY

class TranscriptionClient:
    def transcribe(self, audio_file_path: str):
        if not ASSEMBLYAI_API_KEY:
            raise ValueError("ASSEMBLYAI_API_KEY is not set.")
            
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"],
            language_detection=True,
            speaker_labels=True,
            auto_chapters=False,
            summarization=False
        )
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")
            
        return transcript
