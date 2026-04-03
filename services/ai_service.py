import os
import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"

def get_fun_fact(city_name: str) -> str:
    """Get a fun fact about a city using Hugging Face API"""
    
    # Check if we have an API token
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "Oh what an interesting place with a lot of history!"
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # Prepare the request - asking for a city fun fact
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful travel guide. Keep responses short and fun."
            },
            {
                "role": "user",
                "content": f"Tell me one short fun fact about {city_name}. Keep it to one sentence."
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": 60,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            fact = result["choices"][0]["message"]["content"].strip()
            
            # Clean up any repetition
            fact = fact.replace(f"One short fun fact about {city_name}:", "").strip()
            fact = fact.replace(f"Fun fact about {city_name}:", "").strip()
            
            if fact and len(fact) > 5:
                return f"📚 {fact}"
                
    except Exception as e:
        # Silent fail - use fallback
        pass
    
    # Fallback message
    return "Oh what an interesting place with a lot of history!"

# services/ai_service.py
import os
import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"

def create_intro(city_name: str) -> str:
    """Generate an adventurous intro/lore about starting your IPO journey in a city"""
    
    # Check if we have an API token
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "Your adventure begins now. Where will your journey take you?"
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a game master creating an exciting startup adventure. Be dramatic, fun, and inspiring. Keep responses to 2-3 sentences."
            },
            {
                "role": "user",
                "content": f"Create a dramatic 2-sentence startup adventure intro about trying to IPO a company in {city_name}. Mention something unique about {city_name} and the challenges/opportunities there."
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": 80,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            lore = result["choices"][0]["message"]["content"].strip()
            
            if lore and len(lore) > 10:
                return f"🏢 {lore}\n"
                
    except Exception as e:
        # Silent fail - use fallback
        pass
    
    # Generic short fallback
    return "Your adventure begins now. Where will your journey take you?"