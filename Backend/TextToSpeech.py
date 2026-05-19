import pygame  # Import pygame library for handling audio playback
import random  # Import random for generating random choices
import asyncio # Import asyncio for asynchronous operations
import edge_tts # Import edge_tts for text-to-speech functionality
import os      # Import os for file path handling
from dotenv import dotenv_values # Import dotenv for reading environment variables from a .env file

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice") # Get the AssistantVoice from the environment variables

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3" # Define the path where the speech file will be saved

    if os.path.exists(file_path): # Check if the file already exists
        os.remove(file_path) # If it exists, remove it to avoid overwriting errors

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+25Hz', rate='+18%')
    await communicate.save(r"Data\speech.mp3") # Save the generated speech as an MP3 file

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play() # Play the audio

            # Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False: # Check if the external function returns False
                    break
                pygame.time.Clock().tick(10) # Limit the loop to 10 ticks per second

            return True # Return True if the audio played successfully

        except Exception as e: # Handle any exception during the process
            print(f"Error in TTS: {e}")

        finally:
            try:
                # Call the provided function with False to signal the end of TTS
                func(False)
                pygame.mixer.music.stop() # Stop the audio playback
                pygame.mixer.quit() # Quit the pygame mixer

            except Exception as e: # Handle any exceptions during cleanup
                print(f"Error in finally block: {e}")

# Function to manage Text-to-Speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") # Split the text by periods into a list of sentences

    # List of predefined responses for cases where the text is too long
    responses = [
    "बाकी का रिजल्ट चैट स्क्रीन पर प्रिंट हो गया है, सर एक बार चेक कर लें।",
    "बाकी का टेक्स्ट अब चैट स्क्रीन पर है सर, प्लीज इसे चेक करें।",
    "सर, आप बाकी का टेक्स्ट चैट स्क्रीन पर देख सकते हैं।",
    "टेक्स्ट का बचा हुआ पार्ट अब चैट स्क्रीन पर है, सर।",
    "सर, आपको चैट स्क्रीन पर और भी टेक्स्ट मिल जाएगा देखने के लिए।",
    "बाकी का आंसर अब चैट स्क्रीन पर है, सर।",
    "सर, प्लीज चैट स्क्रीन पर देखिए, बाकी का आंसर वहीं है।",
    "सर, आपको पूरा आंसर चैट स्क्रीन पर मिल जाएगा।",
    "टेक्स्ट का अगला पार्ट चैट स्क्रीन पर है, सर।",
    "सर, और इंफॉर्मेशन के लिए प्लीज चैट स्क्रीन चेक करें।",
    "सर, आपके लिए चैट स्क्रीन पर और भी टेक्स्ट है।",
    "सर, एक्स्ट्रा टेक्स्ट के लिए एक बार चैट स्क्रीन देख लीजिए।",
    "सर, आपको चैट स्क्रीन पर और भी पढ़ने को मिल जाएगा।",
    "सर, बाकी का टेक्स्ट चैट स्क्रीन पर चेक कर लें।",
    "चैट स्क्रीन पर ही बाकी का टेक्स्ट है, सर।",
    "सर, चैट स्क्रीन पर और भी है, प्लीज देख लीजिए।",
    "सर, टेक्स्ट का आगे का पार्ट चैट स्क्रीन पर दिया गया है।",
    "सर, आपको पूरा आंसर चैट स्क्रीन पर मिल जाएगा, प्लीज चेक कर लें।",
    "सर, बाकी का टेक्स्ट देखने के लिए प्लीज चैट स्क्रीन चेक करें।",
    "सर, पूरा आंसर देखने के लिए चैट स्क्रीन पर देखिए।"
]

    # If the text is very long (more than 4 sentences and 250 characters), add a response message
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)

    # Otherwise, just play the whole text
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech function
        TextToSpeech(input("Enter the text: "))