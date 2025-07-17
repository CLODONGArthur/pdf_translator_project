import os
import requests
from dotenv import load_dotenv

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def translate_text(text, source_lang, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_lang.upper(),
        "target_lang": target_lang.upper()
    }
    response = requests.post(url, data=data)
    return response.json()["translations"][0]["text"]