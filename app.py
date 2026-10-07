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

    if request.method == "POST":
        text = request.form["text"]
        language = request.form["language"]

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

        response = requests.post(OLLAMA_URL, json=data)
        result = response.json()

        translation = result["response"]

    return render_template(
        "index.html",
        translation=translation
    )


if __name__ == "__main__":
    app.run(debug=True)