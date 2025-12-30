from pathlib import Path
import re

from flask import Flask, redirect, render_template, request, session, url_for

regex_match = r'\[(.+?)\]'

BASE_DIR = Path(__file__).resolve().parent
MADLIBS_DIR = BASE_DIR / "madlibs"

app = Flask(__name__)
app.secret_key = "madlib-dev-secret"


def list_madlib_files():
    if not MADLIBS_DIR.exists():
        return []
    return sorted([p.name for p in MADLIBS_DIR.glob("*.txt")])


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()
    except FileNotFoundError:
        return None


def extract_prompts(input_string):
    return re.findall(regex_match, input_string)


def replace_prompts_with_answers(input_string, answers):
    prompts = re.findall(regex_match, input_string)
    for i, prompt in enumerate(prompts):
        input_string = re.sub(r"\[" + re.escape(prompt) + r"\]", answers[i], input_string, 1)
    return input_string


@app.get("/")
def index():
    files = list_madlib_files()
    return render_template("index.html", files=files)


@app.post("/start")
def start():
    files = set(list_madlib_files())
    filename = request.form.get("filename", "")
    if filename not in files:
        return redirect(url_for("index"))
    session["filename"] = filename
    session["answers"] = []
    session["index"] = 0
    return redirect(url_for("prompt"))


@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    filename = session.get("filename")
    if not filename:
        return redirect(url_for("index"))

    file_path = MADLIBS_DIR / filename
    input_string = read_file(file_path)
    if input_string is None:
        return redirect(url_for("index"))

    prompts = extract_prompts(input_string)

    if request.method == "POST":
        answers = []
        for i in range(len(prompts)):
            answer = request.form.get(f"answer_{i}", "").strip()
            answers.append(answer)
        session["answers"] = answers
        return redirect(url_for("result"))

    return render_template(
        "prompt.html",
        prompts=prompts,
        filename=filename,
    )


@app.get("/result")
def result():
    filename = session.get("filename")
    if not filename:
        return redirect(url_for("index"))

    file_path = MADLIBS_DIR / filename
    input_string = read_file(file_path)
    if input_string is None:
        return redirect(url_for("index"))

    prompts = extract_prompts(input_string)
    answers = session.get("answers", [])
    if len(answers) < len(prompts):
        return redirect(url_for("prompt"))

    completed = replace_prompts_with_answers(input_string, answers)
    return render_template("result.html", completed=completed, filename=filename)


@app.post("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
