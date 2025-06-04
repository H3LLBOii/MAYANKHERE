import os
import threading
import time
import requests

lock = threading.Lock()
running = False
bot_thread = None

def read_file(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def write_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content.strip())

def get_tokens():
    return read_file("tokennum.txt")

def get_convos():
    return read_file("convos.txt")

def get_messages():
    return read_file("NP.txt")

def get_settings():
    return {
        "haters": read_file("hatersname.txt"),
        "speed": read_file("time.txt")
    }

def update_tokens(tokens):
    write_file("tokennum.txt", tokens)

def update_convos(convos):
    write_file("convos.txt", convos)

def update_messages(messages):
    write_file("NP.txt", messages)

def update_settings(haters, speed):
    write_file("hatersname.txt", haters)
    write_file("time.txt", speed)

def send_messages(convo_id, messages, tokens, haters, delay):
    token_list = tokens.splitlines()
    msg_list = messages.splitlines()
    max_tokens = len(token_list)

    headers = {"User-Agent": "Mozilla/5.0"}

    for index, message in enumerate(msg_list):
        if not running:
            break
        token = token_list[index % max_tokens].strip()
        url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
        payload = {"access_token": token, "message": f"{haters} {message}"}
        try:
            requests.post(url, json=payload, headers=headers)
            print(f"[✓] Sent to {convo_id} using token {index % max_tokens + 1}")
        except Exception as e:
            print(f"[x] Failed: {e}")
        time.sleep(int(delay))

def bot_main():
    global running
    convos = get_convos().splitlines()
    tokens = get_tokens()
    messages = get_messages()
    settings = get_settings()
    haters = settings["haters"]
    delay = settings["speed"]

    for convo_id in convos:
        if not running:
            break
        send_messages(convo_id.strip(), messages, tokens, haters, delay)

def start_bot():
    global running, bot_thread
    if not running:
        running = True
        bot_thread = threading.Thread(target=bot_main)
        bot_thread.start()

def stop_bot():
    global running
    running = False

def is_running():
    return running
