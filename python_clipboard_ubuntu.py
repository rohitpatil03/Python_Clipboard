import time
import subprocess
import requests
import json
from pynput import keyboard

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

def on_press(key):
    global PREV_DATA, URL_DATA
    try:
        if key.char == 'c' and any([key_mod in pressed_keys for key_mod in (keyboard.Key.ctrl, keyboard.Key.alt)]):
            local_clipboard = get_clipboard()  
            if update_global_clipboard(local_clipboard):
                URL_DATA = local_clipboard  
        elif key.char == 'v' and any([key_mod in pressed_keys for key_mod in (keyboard.Key.ctrl, keyboard.Key.alt)]):
            remote_clipboard = fetch_clipboard()  
            if remote_clipboard:
                PREV_DATA = remote_clipboard
                set_clipboard(PREV_DATA)  
                URL_DATA = PREV_DATA
    except AttributeError:
        pass

pressed_keys = set()

def on_press_handler(key):
    global pressed_keys
    try:
        if key == keyboard.Key.ctrl or key == keyboard.Key.alt:
            pressed_keys.add(key)
    except AttributeError:
        pass

def on_release_handler(key):
    global pressed_keys
    try:
        if key == keyboard.Key.ctrl or key == keyboard.Key.alt:
            pressed_keys.remove(key)
    except AttributeError:
        pass

def track_key_combination():
    with keyboard.Listener(on_press=on_press_handler, on_release=on_release_handler) as listener:
        with keyboard.Listener(on_press=on_press) as listener2:
            listener.join()
            listener2.join()

if __name__ == "__main__":
    track_key_combination()
