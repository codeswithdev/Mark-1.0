from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import sys

# 1. Environment variables and Configuration
env_vars = dotenv_values(".env")
# Default language is Hinglish (hi-IN handles mix well)
InputLanguage = env_vars.get("InputLanguage", "hi-IN") 

# 2. Advanced HTML with Auto-Restart and Error Recovery
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Advanced Speech AI</title>
</head>
<body style="background-color: black; color: white;">
    <button id="start" onclick="startRecognition()">Start</button>
    <button id="end" onclick="stopRecognition()">Stop</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let isStopping = false;

        function startRecognition() {{
            recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.continuous = true;
            recognition.interimResults = true; // Fast detection

            recognition.onresult = function(event) {{
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {{
                    if (event.results[i].isFinal) {{
                        finalTranscript += event.results[i][0].transcript;
                    }}
                }}
                if (finalTranscript) {{
                    output.textContent = finalTranscript;
                }}
            }};

            recognition.onend = function() {{
                if (!isStopping) recognition.start(); // Auto-restart if it drops
            }};

            recognition.start();
        }}

        function stopRecognition() {{
            isStopping = true;
            if (recognition) recognition.stop();
            output.innerHTML = "";
        }}
    </script>
</body>
</html>'''

# Create Data directory and write file
os.makedirs("Data", exist_ok=True)
with open(os.path.join("Data", "Voice.html"), "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# 3. Optimized WebDriver Setup (Universal Path Handling)
def SetupDriver():
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')
    
    # Auto-Binary Detection (Fixes your previous error)
    common_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for path in common_paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            break

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

driver = SetupDriver()
Link = "file:///" + os.path.abspath("Data/Voice.html").replace("\\", "/")

# 4. Smart Query & Language Logic
def QueryModifier(Query):
    if not Query: return ""
    Query = Query.strip().capitalize()
    
    # Smart Punctuation
    questions = ['kya', 'kyun', 'how', 'what', 'where', 'whoom', 'which',  'when', 'who', 'is', 'can you']
    if any(word in Query.lower() for word in questions):
        if not Query.endswith('?'): Query += '?'
    else:
        if not Query.endswith('.'): Query += '.'
    return Query

def UniversalTranslator(Text, target_lang='en'):
    try:
        return mt.translate(Text, target_lang, "auto")
    except:
        return Text

def SetAssistantStatus(Status):
    path = "Frontend/Files"
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/Status.data", "w", encoding="utf-8") as f:
        f.write(Status)

# 5. Core Recognition Loop
def SpeechRecognition():
    driver.get(Link)
    driver.execute_script("startRecognition()")
    
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                # Clear browser text immediately to prepare for next sentence
                driver.execute_script("document.getElementById('output').textContent = ''")
                
                # Fast Response Logic
                processed_text = QueryModifier(Text)
                
                # Detect language switch command
                if "speak in english" in Text.lower():
                    return "System: Switching to English focus."
                
                return processed_text
        except Exception:
            continue

# 6. Execution Block
if __name__ == "__main__":
    SetAssistantStatus("Available")
    print(">>> AI is listening (All Languages Supported)...")
    
    try:
        while True:
            raw_text = SpeechRecognition()
            if raw_text:
                print(f"User: {raw_text}")
                
                # Translation logic for AI brain (if input is not English)
                # You can send 'translated_text' to your LLM
                translated_text = UniversalTranslator(raw_text, 'en')
                
                # logic to keep things moving fast
                SetAssistantStatus("Thinking...")
                # Yahan tum apna AI Response logic add kar sakte ho
                SetAssistantStatus("Available")

    except KeyboardInterrupt:
        driver.quit()
        sys.exit()