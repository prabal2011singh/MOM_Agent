def parse_transcript(transcript):
    structured_data = []
    if getattr(transcript, 'utterances', None):
        for utterance in transcript.utterances:
            structured_data.append({
                "speaker": f"Speaker {utterance.speaker}",
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end
            })
    return structured_data
