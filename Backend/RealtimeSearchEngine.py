from groq import Groq # Importing the Groq library to use its API.
from json import load, dump # Importing functions to read and write JSON files.
import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment vawhriables from a .env file.
from tavily import TavilyClient
import os

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
TavilyKeys = [
    env_vars.get("TavilyAPIKey1"), 
    env_vars.get("TavilyAPIKey2"), 
    env_vars.get("TavilyAPIKey3")
]
current_key_index = 0

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
# System prompt ko thoda adaptive banate hain
System = f"""Hello, I am {Username}. You are {Assistantname}, my smart AI.
*** Strictly provide very short, direct, and perfect answers in 1 or 2 lines only. ***
*** Do not give long explanations or disclaimers. ***
*** Use the provided search data to give a crisp reply. ***
*** If I ask about myself ({Username}), talk to me directly. ***"""

# Ensure Data directory exists so it doesn't crash
if not os.path.exists("Data"):
    os.makedirs("Data")

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    global current_key_index
    
    while current_key_index < len(TavilyKeys):
        current_key = TavilyKeys[current_key_index]
        
        if not current_key:
            current_key_index += 1
            continue

        try:
            # Tavily client initialization with rotation logic
            tavily = TavilyClient(api_key=current_key)
            response = tavily.search(query=query, search_depth="basic", max_results=5)
            results = response.get('results', [])
            
            if not results:
                return f"No search results found for '{query}'."

            Answer = f"The search results for '{query}' are:\n[start]\n"
            for r in results:
                Answer += f"Title: {r.get('title', 'No Title')}\nDescription: {r.get('content', 'No Description')}\n\n"
            Answer += "[end]"
            
            return Answer

        except Exception as e:
            error_str = str(e).lower()
            # Key rotation logic if limit exceeded
            if "limit" in error_str or "429" in error_str:
                current_key_index += 1
            else:
                return f"Error during search: {e}"

    return "Bhai, saari Tavily API keys khatam ho gayi hain!"

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.4, 
        max_tokens=150,  
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry point of the program for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))