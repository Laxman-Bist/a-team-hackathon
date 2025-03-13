import os
import winsound
import tkinter as tk
from tkinter import scrolledtext
from utils.text_processing import sanitize_text, finalize_text

def play_alert_sound():
    """Plays an alert sound based on the operating system."""
    try:
        if os.name == "nt":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        elif os.name == "posix":
            os.system('afplay /System/Library/Sounds/Ping.aiff')  # Mac
            os.system('canberra-gtk-play --id="message-new-instant"')  # Linux
    except:
        pass

def show_alert_and_get_choice(personal_data, text):
    """Displays a scrollable GUI alert window for sensitive data detection."""
    root = tk.Tk()
    root.title("Sensitive Data Detected")
    root.geometry("450x350")
    root.resizable(True, True)  # Allow resizing

    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    play_alert_sound()

    details = "\n".join([f"{k}: {v}" for k, v in personal_data.items()])

    # Frame for scrollable text
    text_frame = tk.Frame(root)
    text_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Scrollable text widget
    text_area = scrolledtext.ScrolledText(text_frame, wrap="word", height=8, width=50)
    text_area.insert("1.0", f"Detected Sensitive Data:\n\n{details}")
    text_area.config(state="disabled")  # Make text read-only
    text_area.pack(fill="both", expand=True)

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Mask", command=lambda: finalize_text(sanitize_text(text, personal_data, "mask"), root), width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Remove", command=lambda: finalize_text(sanitize_text(text, personal_data, "remove"), root), width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Ignore", command=root.destroy, width=10).pack(side="left", padx=5)

    root.mainloop()
