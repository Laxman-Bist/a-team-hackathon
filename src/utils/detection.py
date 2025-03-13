

import google.generativeai as genai
from utils.config import API_KEY

# Configure AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Context for AI detection
context = """
Inside quotations, there is a text. Check if the text contains any personal information (PI).  
Inside quotations, there is a text. Check if the text contains any personal information (PI).  

### **Rules for Detection:**  
1. **Ignore masked data** → If the personal information is replaced with asterisks (`*****` or `********`), it should not be considered as PI.  
2. **Ignore removed data** → If a field label exists but no data follows it (e.g., `Client Name:` with nothing after it), treat it as if the PI is removed and do not flag it.  
   - Example of no PI (data removed):  
     ```
     Client Name:  
     Client ID:  
     Account Type: Chase Private Client  
     Account Number:  
     Routing Number:  
     SSN:  
     Date of Birth:  
     Home Address:  
     Phone:  
     Email:  
     Wealth Manager: (JPMC Wealth Advisory - ID: )  
     Richard maintains a portfolio exceeding , including structured derivatives, municipal bonds, and hedge fund investments. His latest trade, executed on , involved purchasing worth of JPMorgan Equity Premium Income ETF (JEPI). His authorized financial power of attorney is his spouse, .  
     ```
     - **Expected Output:**  
       ```
       no  
       null  
       ```

3. **Only return "yes" if actual, unmasked PI is found.**  

### **Expected Output Format:**  
- If PI is found:  
yes
<data>: <type>
<data>: <type>
- If no PI is found:  
no
null


### **Example:**  
#### **Input:**  
Client Name: Richard Montgomery
Client ID: JPMC-1123456789
Account Type: Chase Private Client
Account Number: 9876 5432 1098 7654
Routing Number: 021000021
SSN: 123-45-6789
Date of Birth: March 12, 1975
Home Address: 48 Park Avenue, New York, NY 10016
Phone: (212) 555-0187
Email: richard.montgomery@client.jpmc.com
Wealth Manager: David Carlson (JPMC Wealth Advisory - ID: WMA-45689)
Richard maintains a portfolio exceeding $12.5M, including structured derivatives, municipal bonds, and hedge fund investments. His latest trade, executed on March 5, 2025, involved purchasing $1.2M worth of JPMorgan Equity Premium Income ETF (JEPI). His authorized financial power of attorney is his spouse, Emily Montgomery.

#### **Expected Output:**  
yes
JPMC-1123456789: client ID
9876 5432 1098 7654: account number
021000021: routing number
123-45-6789: SSN
March 12, 1975: date of birth
48 Park Avenue, New York, NY 10016: address
(212) 555-0187: phone number
richard.montgomery@client.jpmc.com: email
David Carlson: name
WMA-45689: employee ID
Richard Montgomery: name
Emily Montgomery: name
$12.5M: money
$1.2M: money
March 5, 2025: date


### **Example:**  
#### **Input:**
my email is laxman@gmail.com and my phone number is 8888464964
#### **Expected Output:**  
yes
8888464964: phone number
laxman@gmail.com: email
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