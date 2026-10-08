import os

from flask import Flask, render_template, request
import requests
from google import genai

app = Flask(__name__)

# Local Ollama
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = "gemma4:e2b"

# Public hosted AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.8-flash"

gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def translate_with_ollama(text, language):
    prompt = f"""
Translate the following text into {language}.
Give only the translation. Do not explain anything.

Text:
{text}
"""

    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result.get("response", "").strip()


def translate_with_gemini(text, language):
    prompt = f"""
Translate the following text into {language}.
Give only the translation. Do not explain anything.

Text:
{text}
"""

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text.strip()


@app.route("/", methods=["GET", "POST"])
def home():
    translation = ""
    error = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        language = request.form.get("language", "").strip()

        if not text:
            error = "Please enter some text."

        elif not language:
            error = "Please select a target language."

        else:
            try:
                # Use Gemini when deployed with an API key.
                if GEMINI_API_KEY:
                    translation = translate_with_gemini(
                        text,
                        language
                    )

                # Otherwise use local Ollama.
                else:
                    translation = translate_with_ollama(
                        text,
                        language
                    )

            except Exception as e:
                error = f"Translation error: {e}"

    return render_template(
        "index.html",
        translation=translation,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )