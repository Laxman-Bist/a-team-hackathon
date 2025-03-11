import os
import winsound
from tkinter import Tk, Button, Label
from utils.text_processing import sanitize_text, finalize_text

def play_alert_sound():
    """
    Plays an alert sound based on the operating system.
    For Windows, it plays the "SystemExclamation" sound using the winsound module.
    For macOS, it plays the "Ping" sound using the afplay command.
    For Linux, it plays the "message-new-instant" sound using the canberra-gtk-play command.
    If an error occurs while attempting to play the sound, it will be silently ignored.
    """
    try:
        if os.name == "nt":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        elif os.name == "posix":
            os.system('afplay /System/Library/Sounds/Ping.aiff')  # Mac
            os.system('canberra-gtk-play --id="message-new-instant"')  # Linux
    except:
        pass

def show_alert_and_get_choice(personal_data, text):
    """
    Displays a GUI alert window to notify the user of detected sensitive data and provides options to mask, remove, or ignore the data.
    Args:
        personal_data (dict): A dictionary containing the detected sensitive data with keys as data types and values as the corresponding data.
        text (str): The original text containing the sensitive data.
    Returns:
        None
    """
    root = Tk()
    root.title("Sensitive Data Detected")
    root.geometry("400x300")
    root.resizable(False, False)

    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    play_alert_sound()

    details = "\n".join([f"{k}: {v}" for k, v in personal_data.items()])

    label = Label(root, text=f"Detected Sensitive Data:\n\n{details}", wraplength=350, justify="left")
    label.pack(pady=10)

    Button(root, text="Mask", command=lambda: finalize_text(sanitize_text(text, personal_data, "mask"), root), width=10).pack(pady=5)
    Button(root, text="Remove", command=lambda: finalize_text(sanitize_text(text, personal_data, "remove"), root), width=10).pack(pady=5)
    Button(root, text="Ignore", command=root.destroy, width=10).pack(pady=5)

    root.mainloop()
