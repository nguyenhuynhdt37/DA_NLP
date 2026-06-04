import os

from flask import Flask, render_template, request

from data import CATEGORY_NAMES, SAMPLE_POSTS, TRAINING_DATA
from text_processing import (
    analyze_text,
    classify_text,
    evaluate_training_data,
    extract_category_feature_words,
    extract_feature_words,
    get_training_summary,
)


HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8001"))

app = Flask(__name__)


def get_sample_text(sample_index):
    if sample_index is None:
        return None
    if 0 <= sample_index < len(SAMPLE_POSTS):
        return SAMPLE_POSTS[sample_index]
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    selected_index = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
    else:
        selected_index = request.args.get("sample", type=int)
        sample_text = get_sample_text(selected_index)
        if sample_text is not None:
            text = sample_text
        else:
            selected_index = None

    has_text = bool(text.strip())
    analysis = analyze_text(text) if has_text else None
    classification = classify_text(text) if has_text else None

    return render_template(
        "index.html",
        text_value=text,
        samples=SAMPLE_POSTS,
        selected_index=selected_index,
        analysis=analysis,
        classification=classification,
        feature_words=extract_feature_words(),
        category_feature_words=extract_category_feature_words(),
        evaluation=evaluate_training_data(),
        training_summary=get_training_summary(),
        training_data=TRAINING_DATA,
        category_names=CATEGORY_NAMES,
    )


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host=HOST, port=PORT, debug=debug)
