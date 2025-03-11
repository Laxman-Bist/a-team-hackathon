from plyer import notification

def send_notification(message):
    """
    Sends a desktop notification with the given message.
    Args:
        message (str): The message to be displayed in the notification.
    """
    notification.notify(
        title="Sensitive Data Detected",
        message=message,
        timeout=5
    )