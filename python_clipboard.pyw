import keyboard
import time
import win32clipboard
import requests
from plyer import notification

URL = "https://zppishnnovduq3jt5cbo2f7vuu0vrfsv.lambda-url.ap-south-1.on.aws"
ICON_URL = r"./clipboard.ico"

def get_clipboard_text():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()
    return data.decode("utf-8") if data else ""

def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=3,
        app_icon=ICON_URL,
    )

def sync_clipboard(URL):
    headers = {'Content-type': 'application/json'}
    prev_data = ""

    while True:
        if keyboard.is_pressed('ctrl+alt+v'):
            response = requests.get(f"{URL}/getText", headers=headers)
            if response.ok:
                data = response.json().get('body', '')
                set_clipboard_text(data)
                show_notification("Clipboard Sync", "Synced clipboard with server successfully")
            else:
                show_notification("Clipboard Sync Failed", "Failed to sync clipboard with server")

        elif keyboard.is_pressed('ctrl+alt+c'):
            time.sleep(0.01)
            data = get_clipboard_text()

            if data != prev_data:
                response = requests.post(f"{URL}/setText", json={'text': f'{data}'}, headers=headers)
                if response.ok:
                    prev_data = data
                    show_notification("Clipboard Copy", "Copied clipboard content to server successfully")
                else:
                    show_notification("Clipboard Copy Failed", "Failed to copy clipboard content to server")

        elif keyboard.is_pressed('ctrl+alt+esc'):
            show_notification("Program Terminated", "Clipboard sync program terminated successfully")
            exit()

        time.sleep(0.01)

if __name__ == "__main__":
    sync_clipboard(URL)
