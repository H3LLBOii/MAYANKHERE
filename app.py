import os

from flask import Flask, render_template, request, redirect, url_for
from bot_controller import get_tokens, get_convos, get_messages, get_settings,                            update_tokens, update_convos, update_messages, update_settings, start_bot, stop_bot, is_running

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html",
                           tokens=get_tokens(),
                           convos=get_convos(),
                           messages=get_messages(),
                           settings=get_settings(),
                           running=is_running())

@app.route("/update_tokens", methods=["POST"])
def update_tokens_route():
    tokens = request.form["tokens"]
    update_tokens(tokens)
    return redirect(url_for('index'))

@app.route("/update_convos", methods=["POST"])
def update_convos_route():
    convos = request.form["convos"]
    update_convos(convos)
    return redirect(url_for('index'))

@app.route("/update_messages", methods=["POST"])
def update_messages_route():
    messages = request.form["messages"]
    update_messages(messages)
    return redirect(url_for('index'))

@app.route("/update_settings", methods=["POST"])
def update_settings_route():
    haters = request.form["haters"]
    speed = request.form["speed"]
    update_settings(haters, speed)
    return redirect(url_for('index'))

@app.route("/start", methods=["POST"])
def start():
    start_bot()
    return redirect(url_for('index'))

@app.route("/stop", methods=["POST"])
def stop():
    stop_bot()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
