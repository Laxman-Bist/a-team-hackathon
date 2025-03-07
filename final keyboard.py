import keyboard
import pyperclip
from plyer import notification
import google.generativeai as genai
import os

typed_text = ""

genai.configure(api_key="AIzaSyAuyeQh5egMqrw3uTkEIPaMRt37rv-1GGw") 
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_personal_info(text):
    lines = text.split('\n')
    if lines[0].lower() == 'no':
        return None

    personal_info = {}
    for line in lines[1:]:
        if line:
            parts = line.split(': ')
            if len(parts) == 2:
                value, info_type = parts
                personal_info[value] = info_type.strip()
    return personal_info

context = """with quotations there is a text , check if the text has any personal information
the ouput should be yes or no on the first line , if yes then give list of all the words that are considered personal information and what kind of personal information it is ,else give null on the other line .
here is the text 
example ouput 
if there is any personal information in it :
yes
shubham: name
JHO1AC1245: account number
122214545: phone number

else : 
no 
null
"""

def get_response(usr_text):
    total_input = context + usr_text
    response = model.generate_content(total_input)
    personal_data = extract_personal_info(response.text)
    return personal_data

def format_dictionary(data_dict):
    formatted_string = ""
    for key, value in data_dict.items():
        formatted_string += f"{key}: {value}\n"
    return formatted_string.rstrip('\n')  # Remove trailing newline

def final_notification_text(response):
    response_text = "The entered input contains the following PIs"
    response_text += format_dictionary(response)
    return response_text

def on_key_event(event):
    global typed_text
    if event.event_type == "down":
        if event.name == "enter":  # User pressed Enter, assuming search
            if typed_text.strip():
                llm_response = get_response(typed_text)
                if llm_response != None:
                    notification.notify(
                        title="Personal Information Alert",
                        message=final_notification_text(llm_response),
                        timeout=5
                    )
            typed_text = ""  # Reset after search
        elif event.name == "backspace":
            typed_text = typed_text[:-1]  # Handle backspace
        elif event.name == "space":
            typed_text += " "  # Capture spaces
        elif len(event.name) == 1:  # Handle regular character input
            typed_text += event.name

def on_paste(event):
    if keyboard.is_pressed("ctrl") and event.name == "v":
        pasted_text = pyperclip.paste()  # Get clipboard content
        if pasted_text.strip():
            llm_response_paste = get_response(pasted_text)  # Ensure it's not empty
            notification.notify(
                title="Personal Information Alert",
                message=final_notification_text(llm_response_paste),
                timeout=5
            )



# Hook keyboard events
keyboard.hook(on_key_event)
keyboard.on_press(on_paste)

print("Monitoring text input... Press 'Esc' to exit.")
keyboard.wait("esc")  # Stop script on 'Esc' key press





