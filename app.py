from flask import Flask, render_template, request, redirect
import threading
import requests
import time

app = Flask(__name__)

# Global settings
settings = {
    "tokens": [],
    "convos": [],
    "message": "",
    "hater": "",
    "speed": 5,
    "running": False
}

# Loop function

def send_messages_loop():
    while settings["running"]:
        for convo_id in settings["convos"]:
            for token in settings["tokens"]:
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                payload = {
                    "access_token": token,
                    "message": settings["hater"] + " " + settings["message"]
                }
                try:
                    response = requests.post(url, json=payload)
                    if response.ok:
                        print(f"[✓] Sent to {convo_id} with token {token[:5]}...")
                    else:
                        print(f"[x] Failed to send to {convo_id}: {response.text}")
                except Exception as e:
                    print(f"[!] Error sending to {convo_id}: {e}")
                time.sleep(settings["speed"])
        time.sleep(1)  # short delay between loops

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        settings["tokens"] = [t.strip() for t in request.form['tokens'].split(',') if t.strip()]
        settings["convos"] = [c.strip() for c in request.form['convos'].split(',') if c.strip()]
        settings["message"] = request.form['message'].strip()
        settings["hater"] = request.form['hater'].strip()
        settings["speed"] = int(request.form['speed'])
        settings["running"] = True
        threading.Thread(target=send_messages_loop, daemon=True).start()
        return redirect('/')

    return render_template('dashboard.html')

@app.route("/ping")
def ping():
    return "Alive", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
