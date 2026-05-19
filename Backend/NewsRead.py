import requests
import json
from Backend.TextToSpeech import TextToSpeech # Dora ki main awaaz use hogi

def latestnews(field="general"):
    # API Key yahan ek baar daal do (NewsAPI.org se free milti hai)
    api_key = "9db4964a28e547df86efcc7e08715a33" 
    
    # Categories map
    url = f"https://newsapi.org/v2/top-headlines?country=in&category={field}&apiKey={api_key}"

    print(f"Connecting to satellites for {field} news...")
    
    try:
        response = requests.get(url)
        news = json.loads(response.text)
        
        if news["status"] == "ok":
            articles = news["articles"]
            TextToSpeech(f"Boss, here are the top headlines in {field}.")
            
            # Sirf top 3 headlines taaki i3 hang na ho aur time bache
            for i, arts in enumerate(articles[:3]):
                title = arts["title"]
                print(f"{i+1}: {title}")
                TextToSpeech(f"News {i+1}: {title}")
                
            TextToSpeech("That's the current update. What's next on the agenda?")
        else:
            TextToSpeech("I couldn't fetch the news. Please check the API key.")
            
    except Exception as e:
        print(f"Error: {e}")
        TextToSpeech("Network issue detected. I can't reach the news servers.")