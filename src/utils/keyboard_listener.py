import keyboard
import threading
import pyperclip
from utils.detection import get_response
from utils.alert_ui import show_alert_and_get_choice

typed_text = ""

def process_text_input():
    """
    Processes the text input stored in the global variable `typed_text`.
    If `typed_text` is not empty or whitespace, it retrieves a response using the `get_response` function.
    If a response is obtained, it displays an alert and gets a choice using the `show_alert_and_get_choice` function.
    Finally, it resets `typed_text` to an empty string.
    """
    global typed_text
    if typed_text.strip():
        personal_data = get_response(typed_text)
        if personal_data:
            show_alert_and_get_choice(personal_data, typed_text)
    typed_text = ""

def on_key_event(event):
    """
    Handles keyboard events and updates the global typed_text variable based on the key pressed.
    Args:
        event: An object representing the keyboard event. It should have the attributes:
            - event_type (str): The type of the event, e.g., "down" for key press.
            - name (str): The name of the key that triggered the event.
    Behavior:
        - If the event type is "down" and the key is "enter", it starts a new thread to process the text input.
        - If the key is "backspace", it removes the last character from the typed_text.
        - If the key is "space", it appends a space to the typed_text.
        - If the key name is a single character, it appends the character to the typed_text.
    """
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
    """
    Handles the paste event by retrieving the text from the clipboard,
    processing it to check for personal data, and if found, shows an alert
    and gets the user's choice.
    Steps:
    1. Retrieves the text from the clipboard and strips any leading/trailing whitespace.
    2. Checks if the pasted text is not empty.
    3. If the pasted text is not empty, it processes the text to check for personal data.
    4. If personal data is found, it shows an alert and gets the user's choice.
    Returns:
        None
    """
    pasted_text = pyperclip.paste().strip()
    if pasted_text:
        personal_data = get_response(pasted_text)
        if personal_data:
            show_alert_and_get_choice(personal_data, pasted_text)

def start_keyboard_listener():
    """
    Starts a keyboard listener that monitors text input and listens for specific hotkeys.
    This function hooks into the keyboard events and sets up a hotkey for 'ctrl+v' to trigger
    the `on_paste` function. It also prints a message indicating that text input is being monitored
    and waits for the 'Esc' key to be pressed to stop the script.
    Note:
        The `keyboard` module must be installed and imported for this function to work.
    Usage:
        start_keyboard_listener()
    """
    keyboard.hook(on_key_event)
    keyboard.add_hotkey("ctrl+v", on_paste)
    print("Monitoring text input... Press 'Esc' to exit.")
    keyboard.wait("esc")  # Stop script on 'Esc' key press