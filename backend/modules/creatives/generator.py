import requests
import urllib.parse
from backend.core.config import HF_TOKEN

def huggingface_generate(prompt: str):
    try:
        url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        r = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=60)
        if r.status_code == 200:
            with open("/tmp/creative.png", "wb") as f:
                f.write(r.content)
            return "/tmp/creative.png"
        return None
    except Exception:
        return None

def pollinations_generate(prompt: str):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
    r = requests.get(url, timeout=30)
    with open("/tmp/creative.png", "wb") as f:
        f.write(r.content)
    return "/tmp/creative.png"

def generate_creative(prompt: str) -> str:
    img = huggingface_generate(prompt)
    if img:
        return img
    return pollinations_generate(prompt)
