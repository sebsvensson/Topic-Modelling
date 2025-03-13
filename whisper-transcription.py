import whisper
import os

model = whisper.load_model("large", device="cpu")

audio_path = r"MY_FOLDER"

def format_timestamp(seconds):
    ms = int((seconds % 1) * 1000)
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

for filename in os.listdir(audio_path):

    file_path = os.path.join(audio_path, filename)

    if  os.path.isfile(file_path) and filename.endswith(("wav")):

        print(f"Transcribing: {file_path}")

        result = model.transcribe(file_path)

        srt_file = os.path.splitext(file_path)[0] + "_transcription.srt"

        with open(srt_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                print(f"Segment {i+1}: {segment['text'].strip()}")
                # SRT index
                f.write(f"{i+1}\n")
                # Timestamps
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                f.write(f"{start} --> {end}\n")
                # Text
                f.write(f"{segment['text'].strip()}\n\n")

        print(f"SRT file save at: {srt_file}")

print("All audio files have been transcribed")