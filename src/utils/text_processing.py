import pyperclip
import re
from utils.notifications import send_notification

def sanitize_text(text, personal_data, choice):
    """
    Sanitizes the given text by either masking or removing personal data.
    Args:
        text (str): The input text to be sanitized.
        personal_data (dict): A dictionary where keys are personal data strings to be sanitized.
        choice (str): The sanitization method to use. 
                      "mask" will replace personal data with asterisks (*), 
                      "remove" will remove personal data from the text.
    Returns:
        str: The sanitized text with personal data either masked or removed.
    """
    if choice == "mask":
        for pi in personal_data.keys():
            text = text.replace(pi, "*" * len(pi))
    elif choice == "remove":
        for pi in personal_data.keys():
            pi = pi.strip()  # Ensure no extra spaces
            print(f"Removing: '{pi}' from text")  # Debugging

            # If text is an exact match, just clear it
            if text.strip() == pi:
                text = " "
            else:
                # Remove the personal data safely from any position
                text = re.sub(rf"\b{re.escape(pi)}\b", "", text)

            print(f"Updated text: '{text}'")  # Debugging

    return text

def finalize_text(text, root=None):
    """
    Finalizes the given text by copying it to the clipboard and sending a notification.
    If the text is empty, a notification indicating that sensitive data was removed is sent.
    If a root window is provided, it is destroyed after processing the text.
    Args:
        text (str): The text to be processed and copied to the clipboard.
        root (optional): The root window to be destroyed after processing the text.
    """
    if text: 
        pyperclip.copy(text)
        send_notification("Processed text copied to clipboard!")
    else:
        send_notification("Sensitive data was completely removed.")

    if root:
        root.destroy()
