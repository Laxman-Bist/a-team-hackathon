import re

# Define regex patterns for emails and phone numbers
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'\b\d{10}\b'  # Matches 10-digit phone numbers

# Contextual function to detect personal information using regex
def get_response(user_text):
    """
    Detects email addresses and phone numbers using regex.
    Returns a dictionary with detected data and their types.
    """
    personal_info = {}

    # Find all email matches
    emails = re.findall(EMAIL_PATTERN, user_text)
    for email in emails:
        personal_info[email] = "email"

    # Find all phone number matches
    phone_numbers = re.findall(PHONE_PATTERN, user_text)
    for phone in phone_numbers:
        personal_info[phone] = "phone number"

    # Return result in the expected format
    return personal_info if personal_info else None

# Example Usage:
if __name__ == "__main__":
    test_text = "Contact me at user@example.com or 8888464964."
    result = get_response(test_text)

    if result:
        print("yes")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("no\nnull")