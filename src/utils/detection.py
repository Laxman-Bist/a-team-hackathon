

import google.generativeai as genai
from utils.config import API_KEY

# Configure AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Context for AI detection
context = """Inside quotations, there is a text. Check if the text contains any personal information (PI).
The output should strictly follow this format:

yes
<data>: <type>
<data>: <type>

Else, return:

no
null

Example Output:
yes
8888464964: phone number
user@example.com: email

If no PI is found:
no
null
"""

# Extracts PI details from AI response
def extract_personal_info(response_text):
    """
    Extracts personal information from a given response text.
    The function processes the response text by splitting it into lines and 
    extracting key-value pairs of personal information. If the first line 
    of the response text is 'no' (case insensitive), the function returns None.
    Args:
        response_text (str): The response text containing personal information.
    Returns:
        dict or None: A dictionary containing extracted personal information 
                      as key-value pairs, or None if the first line is 'no'.
    """
    lines = response_text.strip().split('\n')
    if lines[0].lower() == 'no':
        return None

    personal_info = {}
    for line in lines[1:]:
        if line.strip() and ": " in line:
            value, info_type = line.split(': ', 1)
            personal_info[value.strip()] = info_type.strip()
    return personal_info

# Calls Gemini AI to check for PI
def get_response(user_text):
    """
    Generates a response based on the provided user text.
    Args:
        user_text (str): The input text from the user.
    Returns:
        str: Extracted personal information from the generated response.
    """
    total_input = context + f'\n"{user_text}"'
    response = model.generate_content(total_input)
    return extract_personal_info(response.text)