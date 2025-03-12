import os
import keyboard
import threading
import pyperclip
import psutil
import pyautogui
import win32gui
import win32process
from utils.detection import get_response
from utils.alert_ui import show_alert_and_get_choice
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONITORED_APPS = os.getenv("MONITORED_APPS", "").lower().split(",")
print(f"Monitoring applications: {MONITORED_APPS}")
typed_text = ""

def get_window_under_cursor():
    """Gets the process name of the window under the cursor."""
    try:
        x, y = pyautogui.position()  # Get cursor position
        hwnd = win32gui.WindowFromPoint((x, y))  # Get window handle at cursor position

        if hwnd:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get process ID
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if proc.info['pid'] == pid:
                    return proc.info['name'].lower()  # Return process name
    except Exception as e:
        print(f"Error detecting window under cursor: {e}")

    return None  # No match found

def process_text_input():
    """Processes typed text and checks for sensitive data."""
    global typed_text
    if typed_text.strip():
        personal_data = get_response(typed_text)
        if personal_data:
            show_alert_and_get_choice(personal_data, typed_text)
    typed_text = ""

def on_key_event(event):
    """Tracks typed text and handles key events."""
    global typed_text
    if event.event_type == "down":
        if event.name == "enter":
            threading.Thread(target=process_text_input).start()
        elif event.name == "backspace":
            typed_text = typed_text[:-1]
        elif event.name == "space":
            typed_text += " "
        elif len(event.name) == 1:
            typed_text += event.name

def on_paste():
    """Handles paste events and checks if the cursor is inside a monitored application."""
    active_app = get_window_under_cursor()
    print(f"Paste detected in: {active_app}")

    if active_app and (not MONITORED_APPS or active_app in MONITORED_APPS):
        pasted_text = pyperclip.paste().strip()
        if pasted_text:
            personal_data = get_response(pasted_text)
            if personal_data:
                show_alert_and_get_choice(personal_data, pasted_text)

def start_keyboard_listener():
    """Starts monitoring keyboard input and paste events."""
    keyboard.hook(on_key_event)
    keyboard.add_hotkey("ctrl+v", on_paste)
    print("Monitoring text input... Press 'Esc' to exit.")
    keyboard.wait("esc")  # Stop script on 'Esc' key press

if __name__ == "__main__":
    start_keyboard_listener()
