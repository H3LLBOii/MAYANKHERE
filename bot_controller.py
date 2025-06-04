import os
import threading
import requests
import time

def send_messages_loop():
    while True:
        try:
            with open("NP.txt", "r") as f:
                message = f.read().strip()
            with open("tokennum.txt", "r") as f:
                tokens = [t.strip() for t in f.readlines()]
            with open("convos.txt", "r") as f:
                convos = [c.strip() for c in f.readlines()]
            with open("hatersname.txt", "r") as f:
                hater = f.read().strip()
            with open("time.txt", "r") as f:
                delay = int(f.read().strip())
        except Exception as e:
            print(f"[!] Error reading files: {e}")
            return

        for convo_id in convos:
            for idx, token in enumerate(tokens):
                try:
                    response = requests.post(
                        f"https://graph.facebook.com/v17.0/t_{convo_id}/",
                        json={
                            "access_token": token,
                            "message": f"{hater} {message}"
                        },
                        headers={
                            "User-Agent": "Mozilla/5.0",
                            "referer": "www.google.com"
                        }
                    )
                    if response.ok:
                        print(f"[✓] Sent to {convo_id} using token {idx+1}")
                    else:
                        print(f"[x] Failed to send to {convo_id} with token {idx+1}: {response.text}")
                except Exception as e:
                    print(f"[!] Error: {e}")
                time.sleep(delay)
