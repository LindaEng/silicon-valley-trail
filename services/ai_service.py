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
    
def create_ipo_lore(game_state) -> str:
    """Generate dramatic IPO lore based on team performance and journey"""
    
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return _get_ipo_fallback(game_state)
    
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    # Gather context about the game state
    total_productivity = sum(m.get('productivity', 0) for m in game_state.team)
    total_skill = sum(m.get('skill', 0) for m in game_state.team)
    avg_morale = sum(m.get('morale', 100) for m in game_state.team) / len(game_state.team)
    cities_count = len(game_state.locations_visited)
    funding = game_state.funding
    
    # Determine team strength
    if total_productivity >= 70:
        team_strength = "an unstoppable powerhouse"
    elif total_productivity >= 50:
        team_strength = "a solid, capable team"
    elif total_productivity >= 30:
        team_strength = "a scrappy but determined group"
    else:
        team_strength = "a rag-tag bunch held together by duct tape and coffee"
    
    # Determine morale context
    if avg_morale >= 80:
        morale_context = "morale is through the roof"
    elif avg_morale >= 60:
        morale_context = "spirits are high"
    elif avg_morale >= 40:
        morale_context = "everyone's just pushing through"
    else:
        morale_context = "the team is running on fumes"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a dramatic startup narrator. Create hype, tension, and excitement about an IPO. Be cinematic and inspiring. Keep to 3 sentences max."
            },
            {
                "role": "user",
                "content": f"""Write a dramatic 2-3 sentence IPO announcement for a startup that:
- Has visited {cities_count} cities on their journey
- Has ${funding:.2f} in funding
- Has {team_strength} with {morale_context}
- Is about to go public

Make it epic and exciting!"""
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": 100,
        "temperature": 0.9
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            lore = response.json()["choices"][0]["message"]["content"].strip()
            if lore and len(lore) > 10:
                return f"🎉 {lore}\n"
    except:
        pass
    
    return _get_ipo_fallback(game_state)


def _get_ipo_fallback(game_state) -> str:
    """Fallback IPO messages based on game state"""
    
    total_productivity = sum(m.get('productivity', 0) for m in game_state.team)
    cities_count = len(game_state.locations_visited)
    funding = game_state.funding
    
    # Success scenarios (high funding/good team)
    if funding > 1000000 and total_productivity > 60:
        return "🎉 The confetti falls as the opening bell rings! Your startup has officially IPO'd at a valuation that makes headlines worldwide. The journey was worth every sleepless night!"
    
    elif funding > 500000:
        return "🚀 After an incredible journey through innovation and determination, your company hits the public market! Investors are buzzing, and the future has never looked brighter!"
    
    elif cities_count > 10:
        return "🌍 From humble beginnings to a global empire! Your IPO marks the culmination of a journey that spanned continents and captured imaginations. The world is now your stage!"
    
    # Medium success
    elif funding > 100000:
        return "📈 The stock exchange welcomes your company with open arms! It wasn't always easy, but your team's grit and vision paid off in the end. Time to celebrate!"
    
    # Barely made it
    elif funding > 50000:
        return "💪 Against all odds, you made it! The IPO was modest, but survival in the startup world is victory enough. Here's to building something greater!"
    
    # Scraping by
    else:
        return "🎯 You did it! The IPO might not have made you billionaires overnight, but you built something real, took it public, and proved the doubters wrong. That's a win!"


def create_ipo_failure_lore(game_state) -> str:
    """Generate dramatic lore for failed IPO attempts"""
    
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "The IPO didn't go as planned. Back to the drawing board..."
    
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    funding = game_state.funding
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a dramatic startup narrator. Describe failure in a way that's motivating, not crushing. Keep to 2 sentences."
            },
            {
                "role": "user",
                "content": f"A startup tried to IPO with only ${funding:.2f} in funding and failed. Write a dramatic but motivating 2-sentence message about regrouping and coming back stronger."
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "max_tokens": 80,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            lore = response.json()["choices"][0]["message"]["content"].strip()
            if lore:
                return f"😔 {lore}\n"
    except:
        pass
    
    # Fallback failure messages
    failure_messages = [
        "😔 The stock market wasn't ready for your vision. But every failure is just a setup for a greater comeback!",
        "📉 The IPO fell through... this time. Gather your team, learn from the experience, and prepare for round two!",
        "💔 Not today. But remember - Airbnb, Uber, and even Tesla had rocky starts. The story isn't over yet!",
        "🎢 The IPO rollercoaster had more downs than ups today. But real entrepreneurs don't quit - they pivot and persist!"
    ]
    
    return random.choice(failure_messages)