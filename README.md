# Python_Clipboard

## Windows Installation and Usage
```
git clone https://github.com/rohitpatil03/Python_Clipboard.git
cd Python_Clipboard
pip install -r requirements.txt
python python_clipboard.pyw
```

## Ubuntu Installation
```
sudo apt-get install xclip
```
```
git clone https://github.com/rohitpatil03/Python_Clipboard.git
pip install -r requirements-u.txt # may require breaking system package flag set
cd Python_Clipboard
python python_clipboard_ubuntu.py
```


## Keyboard Shortcuts

- **Ctrl+Alt+V:** Fetches clipboard data from the server and updates the local clipboard.
- **Ctrl+Alt+C:** Copies the local clipboard data to the server.
- **Ctrl+Alt+Esc:** Exits the script.

## Notes

- Ensure that your machine has an active internet connection.
- The script runs in the background, continuously monitoring the specified keyboard shortcuts.
- Adjustments to keyboard shortcuts and server URL can be made within the script.
