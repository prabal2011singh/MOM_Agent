from google import genai
import json
from config.settings import GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
    def generate_mom(self, transcript_data):
        prompt = f"""
You are an AI meeting assistant. Please generate a structured Minutes of Meeting (MOM) from the following transcript.
The transcript includes speaker labels.

Transcript:
{json.dumps(transcript_data, indent=2)}

Please provide the output in JSON format with the following keys:
- "summary": A brief meeting summary.
- "discussion_points": A list of key discussion points.
- "decisions": A list of decisions made.
- "action_items": A list of objects, each containing "task", "owner" (if identifiable), "priority", and "deadline" (if mentioned).
- "blockers": A list of risks or blockers.

Ensure the response is valid JSON only. Do not include markdown code block formatting like ```json in the output.
"""
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        return json.loads(text)
