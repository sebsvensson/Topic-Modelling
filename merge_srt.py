import srt
import os
import json

srt_folder = r"MY_FOLDER"

json_folder = os.path.join(os.path.dirname(srt_folder), "_json")

os.makedirs(json_folder, exist_ok=True)

def segments_overlap(start1, end1, start2, end2, min_overlap=0.5):
                    """ Check if two segments overlap significantly """
                    overlap = max(0, min(end1, end2) - max(start1, start2))
                    duration1 = end1 - start1
                    duration2 = end2 - start2
                    return overlap >= min_overlap * min(duration1, duration2)

for filename in os.listdir(srt_folder):
    if filename.endswith("_transcription.srt"):

        base_name = filename.replace("_transcription.srt", "")
        transcription_file = os.path.join(srt_folder, filename)
        diarization_file = os.path.join(srt_folder, base_name + "_diarization.srt")
        json_file_path = os.path.join(json_folder, base_name + ".json")
        if not os.path.exists(diarization_file):
            print(f"Skipping {filename}, no diarization file found.")
            continue

        # Load transcription segments
        with open(transcription_file, "r", encoding="utf-8") as f:
            transcription_segments = list(srt.parse(f.read()))

        # Load diarization segments
        with open(diarization_file, "r", encoding="utf-8") as f:
            diarization_segments = list(srt.parse(f.read()))

        updated_segments = []

        # Assign speakers to transcription segments
        for trans_segment in transcription_segments:
            trans_start = trans_segment.start.total_seconds()
            trans_end = trans_segment.end.total_seconds()

            best_speaker = "Unknown"
            max_overlap = 0

            for diarization_segment in diarization_segments:
                diarization_start = diarization_segment.start.total_seconds()
                diarization_end = diarization_segment.end.total_seconds()

                if segments_overlap(trans_start, trans_end, diarization_start, diarization_end):
                    overlap_duration = min(trans_end, diarization_end) - max(trans_start, diarization_start)
                    if overlap_duration > max_overlap:
                        max_overlap = overlap_duration
                        best_speaker = diarization_segment.content

            
            if best_speaker != "Unknown" or trans_segment.content.strip():
                trans_segment.content = f"{best_speaker}: {trans_segment.content}"
                updated_segments.append({
                    "index": trans_segment.index,
                    "start": trans_start,
                    "end": trans_end,
                    "speaker": best_speaker,
                    "text": trans_segment.content
                })

        # Save final SRT with speakers
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(updated_segments, f, indent=4, ensure_ascii=False)

        print(f"Final transcription saved: {json_file_path}")

print("All files merged.")