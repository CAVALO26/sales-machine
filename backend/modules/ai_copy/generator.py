import json
import re
import anthropic
from backend.core.config import CLAUDE_API_KEY

def generate_copy(structure: dict) -> dict:
    prompt = f"""You receive a marketing page structure in JSON.
Create an improved version keeping the same intent.
Return ONLY a JSON object with these exact fields:
- headline (string)
- subheadline (string)
- bullets (array of at least 5 strings)
- cta (string)
- story (string, 2-3 sentences)
- faq (array of 3 objects with q and a fields)

Input structure:
{json.dumps(structure, ensure_ascii=False)}

Return only valid JSON. No markdown, no explanation."""

    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    content = message.content[0].text

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
        return structure
