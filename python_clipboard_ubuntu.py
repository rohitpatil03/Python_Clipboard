import time
import subprocess
import requests
import json
import keyboard

URL = "https://zppishnnovduq3jt5cbo2f7vuu0vrfsv.lambda-url.ap-south-1.on.aws"
PREV_DATA = ""
URL_DATA = ""

def get_clipboard():
    return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8').strip()

def set_clipboard(text):
    subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def fetch_clipboard():
    response = requests.get(f"{URL}/getText")
    if response.ok:
        return response.json().get('body', '')
    return None

def update_global_clipboard(data):
    response = requests.post(f"{URL}/setText", json={'text': data})
    if response.ok:
        return True
    return False

def on_press(event):
    global PREV_DATA, URL_DATA
    try:
        if event.name == 'c' and keyboard.is_pressed('ctrl+alt'):
            local_clipboard = get_clipboard()  # Get local clipboard data
            if update_global_clipboard(local_clipboard):
                URL_DATA = local_clipboard  # Update URL_DATA to match local clipboard
        elif event.name == 'v' and keyboard.is_pressed('ctrl+alt'):
            remote_clipboard = fetch_clipboard()  # Fetch clipboard data from server
            if remote_clipboard:
                PREV_DATA = remote_clipboard
                set_clipboard(PREV_DATA)  # Update local clipboard with fetched data
                URL_DATA = PREV_DATA
    except AttributeError:
        pass

def track_key_combination():
    keyboard.on_press(on_press)
    keyboard.wait()

if __name__ == "__main__":
    track_key_combination()
