from pyannote.audio import Pipeline
import os

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="MY_TOKEN")

audio_path = r"MY_FOLDER"

def round_timestamp(timestamp):
    return round(timestamp)

def format_timestamp(seconds):
    seconds = round(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02}:{mins:02}:{secs:02}"

for filename in os.listdir(audio_path):
    if filename.endswith(".wav"):
        file_path = os.path.join(audio_path, filename)
        print(f"Diarizing: {file_path}")

        diarization_result = pipeline(file_path)
        srt_file = os.path.splitext(file_path)[0] + "_diarization.srt"

        with open(srt_file, "w", encoding="utf-8") as f:
            for i, (turn, _, speaker) in enumerate(diarization_result.itertracks(yield_label=True)):
                f.write(f"{i+1}\n")
                f.write(f"{format_timestamp(round(turn.start))} --> {format_timestamp(round(turn.end))}\n")
                f.write(f"{speaker}\n\n")

        print(f"Diarization saved: {srt_file}")

print("All files diarized.")