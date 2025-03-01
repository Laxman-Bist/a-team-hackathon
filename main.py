import keyboard
import pyperclip
import time
import threading
import win32gui
import re
import pyautogui

typed_text = ""  # Store typed text
captured_data = []
last_key = None  # Track the last pressed key to prevent duplicate entries

def get_active_window_title():
    """Returns the title of the active window."""
    window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(window)
    return window_title

def is_pii(text):
    """Checks if the given text contains PII."""
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'\b\d{10}\b')

    match = email_pattern.search(text) or phone_pattern.search(text)
    return bool(match)

def alert_pii_detected(text, window_title):
    """Displays a popup alert when PII is detected."""
    print(f"⚠️ ALERT: PII detected in {window_title}: {text}")
    
    time.sleep(0.5)  # Ensure GUI responsiveness

    try:
        pyautogui.alert(f"⚠️ PII Detected!\n\nSensitive data found in: {window_title}\n\nText: {text}", "PII Warning")
    except Exception as e:
        print(f"ERROR: PyAutoGUI Alert Failed - {e}")

def capture_keyboard_event(event):
    """Processes keyboard input and checks for PII."""
    global typed_text, last_key

    if event.event_type == keyboard.KEY_DOWN and event.name != last_key:
        last_key = event.name  # Update last key to avoid duplication

        if event.name == "space":
            typed_text += " "  # Handle space properly
        elif event.name == "backspace":
            typed_text = typed_text[:-1]  # Remove last character on backspace
        elif len(event.name) == 1:  # Normal character input
            typed_text += event.name

        active_window = get_active_window_title()
        captured_data.append(f"{typed_text} in {active_window}")

        print(f"DEBUG: Current Typed Text: {typed_text}")  # Debug print

        # Check for PII in the accumulated text
        if is_pii(typed_text):
            alert_pii_detected(typed_text, active_window)
            typed_text = ""  # Clear text after alert

def monitor_keyboard():
    """Continuously monitors keyboard input."""
    while True:
        event = keyboard.read_event()
        capture_keyboard_event(event)

def start_monitoring():
    """Starts monitoring keyboard in a separate thread."""
    keyboard_thread = threading.Thread(target=monitor_keyboard, daemon=True)
    keyboard_thread.start()

    try:
        while True:
            time.sleep(5)  # Collect data every 5 seconds
            print("Captured Data:", captured_data)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    start_monitoring()