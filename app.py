import os
from flask import Flask, render_template, request, redirect
import threading
from bot_controller import send_messages_loop

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        tokens = request.form['tokens'].strip().splitlines()
        convos = request.form['convos'].strip().splitlines()
        message = request.form['message']
        hater = request.form['hater']
        speed = int(request.form['speed'])

        # Save data to files
        with open("tokennum.txt", "w") as f:
            f.write("\n".join(tokens))
        with open("convos.txt", "w") as f:
            f.write("\n".join(convos))
        with open("NP.txt", "w") as f:
            f.write(message)
        with open("hatersname.txt", "w") as f:
            f.write(hater)
        with open("time.txt", "w") as f:
            f.write(str(speed))

        threading.Thread(target=send_messages_loop, daemon=True).start()
        return redirect('/')

    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
