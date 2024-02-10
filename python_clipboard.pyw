import keyboard
import time
import win32clipboard
import requests
import json

URL = "https://zppishnnovduq3jt5cbo2f7vuu0vrfsv.lambda-url.ap-south-1.on.aws"
PREV_DATA = ""
URL_DATA = ""

def track_key_combination(URL,PREV_DATA, URL_DATA):
    headers ={'Content-type': 'application/json'}

    while True:
        
        if keyboard.is_pressed('ctrl+alt+v'):
            # print("Ctrl+Alt+V pressed")
            response = requests.get(f"{URL}/getText", headers=headers)
            if response.ok:
                res = response.json()
                URL_DATA = res.get('body', '')
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(URL_DATA, win32clipboard.CF_TEXT)
                win32clipboard.CloseClipboard()
            # keyboard.press_and_release('ctrl+v')
        
        elif keyboard.is_pressed('ctrl+alt+c'):
            # print("Ctrl+Alt+C pressed")
            # keyboard.press_and_release('ctrl+c')
            time.sleep(0.1)
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            data = data.decode("utf-8")
            win32clipboard.CloseClipboard()

            if data != PREV_DATA:
                
                PREV_DATA = data
                response = requests.post(f"{URL}/setText", json={'text':f'{PREV_DATA}'}, headers=headers)
                if response.ok:
                    URL_DATA = PREV_DATA
        
        elif keyboard.is_pressed('ctrl+alt+esc'):
            exit()

        time.sleep(0.1)

track_key_combination(URL,PREV_DATA, URL_DATA)