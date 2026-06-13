import anthropic
import base64
import json
import re
import os
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

def analyze_screenshot(image_path):
    img = Image.open(image_path)
    img = img.resize((1280, 720))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    image_data = base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": """You are an expert security analyst. Analyze this screenshot carefully and respond ONLY with raw JSON, no markdown:
{
  "threat_level": "HIGH" or "MEDIUM" or "LOW",
  "threat_type": "exposed_credentials" or "phishing" or "sensitive_data" or "malware" or "social_engineering" or "none",
  "confidence": number between 0 and 100,
  "description": "one sentence description of what you see",
  "reason": "one sentence explaining why this is a threat",
  "action": "one sentence on what the user should do"
}"""
                    }
                ],
            }
        ],
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'```$', '', raw).strip()

    try:
        result = json.loads(raw)
    except:
        result = {
            "threat_level": "LOW",
            "threat_type": "none",
            "confidence": 0,
            "description": raw,
            "reason": "Could not parse response",
            "action": "none"
        }

    print(f"Threat Level  : {result['threat_level']}")
    print(f"Threat Type   : {result['threat_type']}")
    print(f"Confidence    : {result.get('confidence', 'N/A')}%")
    print(f"Description   : {result['description']}")
    print(f"Reason        : {result.get('reason', 'N/A')}")
    print(f"Action        : {result['action']}")
    return result

if __name__ == "__main__":
    from capture import take_screenshot
    image_path = take_screenshot()
    analyze_screenshot(image_path)
