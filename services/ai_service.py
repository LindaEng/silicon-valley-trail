import os
import requests
import random

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

def get_action_fact(location, action) -> str:
    
    # Check if we have an API token
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "Oh what an interesting place with a lot of history!"
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful travel guide. Keep responses short and fun."
            },
            {
                "role": "user",
                "content": f"Tell me one short fun fact about {action} in {location}. Keep it to one sentence."
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
            fact = fact.replace(f"One short fun fact about {action} in {location}:", "").strip()
            fact = fact.replace(f"Fun fact about {action} in {location}:", "").strip()
            
            if fact and len(fact) > 5:
                return f"📚 {fact}"
                
    except Exception as e:
        # Silent fail - use fallback
        pass
    
    # Fallback message
    return "Look at all these interesting options!"

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


def create_character_lore(character: dict, game_state) -> str:
    """Generate dynamic lore when checking in with a team member"""
    
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "💬 The team is doing their best"
    
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    # Get morale/motivation status
    morale_status = _get_status(character.get("morale", 100), "morale")
    motivation_status = _get_status(character.get("motivation", 100), "motivation")
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a startup team member. Respond in 1 sentence with personality. Be brief."
            },
            {
                "role": "user",
                "content": f"You are {character['name']} (Prod:{character['productivity']}/10, Skill:{character['skill']}/10). Morale: {morale_status}, Motivation: {motivation_status}. Say ONE sentence checking in."
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": 50,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            lore = response.json()["choices"][0]["message"]["content"].strip()
            if lore and len(lore) > 5:
                return f"💬 {character['name']}: {lore}"
    except:
        pass
    
    return "💬 The team is doing their best"


def _get_status(value: int, status_type: str) -> str:
    """Simple status converter"""
    if value >= 70:
        return "high"
    elif value >= 40:
        return "medium"
    else:
        return "low"