from flask import Flask, request
from Summarizer.summarizer import summarize
from other_functions.mathocr import *

app = Flask(__name__)


@app.route("/summary", methods=["GET"])
def get_summary():
    text = request.args["text"]
    return summarize(text)

@app.route("/summary", methods=["GET"])
def do_math():
    path = request.args.get("path")
    imgstr = request.args.get("imgstr")

    if path:
        return eq_from_img(path)

    return eq_from_str(imgstr)

app.run(threaded=True)
