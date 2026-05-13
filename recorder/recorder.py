import subprocess
import os
import signal
import json
from pathlib import Path
from datetime import datetime

class AudioRecorder:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.recordings_dir = self.base_dir / "recordings"
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        self.pid_file = self.base_dir / "ffmpeg.pid"

    def start(self):
        if self.pid_file.exists():
            return False, "Recording is already in progress."

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.recordings_dir / f"meeting_{timestamp}.wav"

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "avfoundation",
            "-i", ":BlackHole 2ch",
            "-ar", "16000",
            "-ac", "1",
            str(output_file)
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )

        with open(self.pid_file, "w") as f:
            json.dump({
                "pid": process.pid,
                "file": str(output_file)
            }, f)

        return True, str(output_file)

    def stop(self):
        if not self.pid_file.exists():
            return False, "No recording is currently in progress."

        with open(self.pid_file, "r") as f:
            data = json.load(f)

        pid = data.get("pid")
        output_file = data.get("file")

        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass

        self.pid_file.unlink(missing_ok=True)
        return True, output_file
