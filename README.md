# **Sensitive Data Detection and Masking Tool**  

## **Overview**  
This tool monitors text input from the keyboard and clipboard, detects sensitive personal information (PI) using Google Gemini AI, and provides options to **mask**, **remove**, or **ignore** the detected data. It also includes **system notifications** and an **alert window** for user interaction.

---

## **Features**  
✅ **Real-time text monitoring** (keyboard and clipboard)  
✅ **Personal data detection** using Google Gemini AI  
✅ **User alert system** (foreground pop-up and notification sound)  
✅ **Options to mask, remove, or ignore detected PI**  
✅ **Processed text copied back to clipboard**  

---

## **Project Structure**  
```
project-root/
│── src/
│   ├── utils/                    # Utility functions
│   │   ├── config.py             # Configuration (API keys, settings)
│   │   ├── detection.py          # PI detection logic
│   │   ├── notifications.py      # System notifications
│   │   ├── text_processing.py    # Text sanitization
│   │   ├── keyboard_listener.py  # Keyboard and clipboard event handling
│   │   ├── alert_ui.py           # UI elements for alert handling
|   ├── main.py                   # Entry point
│── requirements.txt               # Python dependencies
│── .env                           # Environment variables (API keys)
│── README.md                      # Project documentation
```

---

## **Installation**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/Laxman-Bist/a-team-hackathon.git
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Set Up API Key**  
Create a `.env` file and add:  
```
GEMINI_API_KEY=your-google-gemini-api-key
```

---

## **Usage**  

### **Run the Program**  
```bash
python src/main.py
```
The program will start monitoring **keyboard input and clipboard data**.  
- Press **Enter** to analyze typed text.  
- Press **Ctrl + V** to check clipboard content.  
- Press **Esc** to exit.  

When sensitive data is detected, a **notification** and **pop-up alert** will appear, allowing you to:  
✅ **Mask** (replace PI with `****`)  
✅ **Remove** (delete PI)  
✅ **Ignore** (keep original text)  

Processed text is automatically copied to the clipboard.

---

## **Dependencies**  
Check `requirements.txt` for all dependencies. Main libraries include:  
- `keyboard` → Captures keystrokes  
- `pyperclip` → Handles clipboard interactions  
- `plyer` → System notifications  
- `tkinter` → GUI pop-up for user actions  
- `google.generativeai` → AI-based PI detection  
- `python-dotenv` → Loads API keys securely  

---

## **Contributing**  
Feel free to fork this repo and submit pull requests. Improvements are welcome!  

---