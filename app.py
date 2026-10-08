import os

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL = "gemma4:e2b"


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
            prompt = f"""
Translate the following text into {language}.
Give only the translation. Do not explain anything.

Text:
{text}
"""

            data = {
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }

            try:
                response = requests.post(
                    OLLAMA_URL,
                    json=data,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()
                translation = result.get("response", "").strip()

                if not translation:
                    error = "The AI returned an empty response."

            except requests.exceptions.RequestException as e:
                error = f"AI connection error: {e}"

            except Exception as e:
                error = f"Unexpected error: {e}"

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