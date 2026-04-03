# Core imports
import time
import random
from pathlib import Path

# Game modules
from game.state import GameState
from game.events import random_blessing, random_curse

# Utils imports
from utils.loader import load_json
from utils.calc import (
    calc_popularity_increase,
    calc_morale_increase,
    calc_funding_increase,
    calc_restaurant_cost,
    calc_morale_decrease,
    calc_popularity_decay,
    calc_distance,
    calc_fun_cost,
)
from utils.cache import CATEGORIES

# UI imports
from ui.display import styled_input, print_characters_grid, print_travel_summary

# Service imports
from services.map_service import get_location, get_nearby
from services.ai_service import get_fun_fact, create_intro, create_character_lore, get_action_fact, create_ipo_lore, create_ipo_failure_lore


def load_splash():
    splash_path = Path(__file__).parent.parent / "assets" / "ascii"/ "splash.txt"
    with open(splash_path, "r", encoding="utf-8") as f:
        print(f.read())
    
    print("=== Silicon Valley Trail ===\n" \
          "1. New Game\n" \
          "2. Continue\n")
    
    choice = styled_input("Choose an Option: ")
    return choice


def start_new_game():
    # Header and intro
    print("\n---New Game---")
    print("\nYou are setting out on a journey through Silicon Valley...")
    print("Build your team. Navigate the chaos. Ship or die.\n")
    print("But first -- where would you like to start?\n")

    # Get location from player
    location = input("Enter location ").strip()
    location_data = get_location(location)
    
    if location_data:
        print(f"You chose: {location}")
    else:
        print("Location not found, using raw input")
    
    print("------------------------------")
    print(f"Location: {location}", create_intro(location))
    
    # Get team selection
    print("Before we start lets choose a dream team!")
    team = choose_team(load_characters())
    
    # Create game state
    new_game_state = GameState(
        team=team, 
        location=location_data or {"name": location}
    )
    new_game_state.locations_visited.append(location)
    
    
    return new_game_state


def load_characters():
    return load_json("data/characters.json")

def choose_team(characters):
    MAX_RETRIES = 3
    TEAM_SIZE = 5
    retries_left = MAX_RETRIES
    
    while retries_left > 0:
        # Show available characters
        print("Choose your team (at least 5, comma separated indices):")
        print_characters_grid(characters)
        
        # Wait for player to be ready
        input(f"We will randomly select {TEAM_SIZE} players. You have {retries_left} retr{'y' if retries_left == 1 else 'ies'}. Press any key to continue")
        
        try:
            # Generate and display random team
            print("Finding your dream team ... ")
            time.sleep(2)
            team = random.sample(characters, TEAM_SIZE)
            
            print("Here is the team!")
            print_characters_grid(team)
            
            # Get player approval
            choice = styled_input(f"Accept this team? (y/n) - {retries_left - 1} retr{'y' if retries_left - 1 == 1 else 'ies'} left: ").lower()
            
            if choice == 'y':
                return team
            
            # Handle rejection
            retries_left -= 1
            if retries_left > 0:
                print("Let's try to find a better team...")
                time.sleep(2)
            
        except (ValueError, IndexError):
            print("Invalid input. Try again.\n")
    
    # No retries remaining
    print("No more retries - assigning final team")
    time.sleep(2)
    print_characters_grid(team)
    return team

def check_team(state):
    while True:
        print("\n Your team: ")
        print_characters_grid(state.team)
        for mem in state.team:
            print(create_character_lore(mem, state.team))
        back = input("Go back to menu? y/n: ")
        if back == "y":
            return "menu"
       

def explore_city(location, state):
    print(f"{location["name"]}: ", get_fun_fact(location))
    print("=================\n\nWhat would you like to do?\n")
    menu_items = {
        "1": ("Find cafes/restaurants", "restaurants", choose_cafe_restaurants),
        "2": ("Find events to raise money", "events", choose_fundraising),
        "3": ("Team Booster", "fun", choose_morale_boost),
        "4": ("Back to Menu", None, None),
    }
    
    for key, (desc, _, _) in menu_items.items():
        print(f"{key}. {desc}")
    
    choice = styled_input("\nYour choice (1-4): ").strip()
    
    if choice == "4":
        return "menu"
    
    if choice not in menu_items:
        print("Invalid choice")
        return
    print("Looking up some spots! ")
    time.sleep(2)
    _, category, handler = menu_items[choice]
    lat, lon = location["lat"], location["lon"]
    results = get_nearby(CATEGORIES[category], lat, lon)
    
    if not (results and isinstance(results, dict) and results.get("elements")):
        print(f"No {category} found nearby. Try another option.")
        return
    
    handler(results, state)

def choose_cafe_restaurants(restaurants, state):
    if not isinstance(restaurants, dict):
        print("No restaurants found nearby.")
        return
    
    places = restaurants.get("elements", [])
    if not places:
        print("No restaurants found nearby.")
        return
    
    #LLM fun fact
    print("-----------------------------------------------")
    print(get_action_fact(state.location["name"], "restaurants"))
    print("-----------------------------------------------")
    # Display options
    for i, place in enumerate(places[:5]):
        tags = place.get("tags", {}) if isinstance(place, dict) else {}
        name = tags.get("name", "NAME UNKNOWN")
        cuisine = tags.get("cuisine", "yummy :p")
        print(f"{i+1}. {name} - {cuisine}")
    
    # Get selection
    choice = styled_input("Choose a place to eat (number) or 0 to go back: ").strip()
    if choice == "0":
        return "main"
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(places):
            selected = places[idx]
            name = selected.get("tags", {}).get("name", "Unknown place") if isinstance(selected, dict) else "Unknown place"
            print(f"Your team eats at {name} and recharges")
        
        time.sleep(2)
        cost = calc_restaurant_cost(state)
        state.funding -= cost
        print(f"Meal cost: ${cost:.2f} | Funding: ${state.funding:.2f}")
        
        morale_boost = calc_morale_increase(state)
        state.morale += morale_boost
        print(f"Morale +{morale_boost:.2f} | Now: {state.morale:.2f}")
    except (ValueError, IndexError):
        print("Invalid input")

def choose_fundraising(venues, state):
    places = venues.get("elements", []) if isinstance(venues, dict) else []
    
    if not places:
        print("No venues found nearby.")
        return
    
    #LLM fun fact
    print("-----------------------------------------------")
    print(get_action_fact(state.location, "venues for fundraising"))
    print("-----------------------------------------------")
    # Display venues
    for i, place in enumerate(places[:5]):
        name = place.get("tags", {}).get("name", "Unknown venue") if isinstance(place, dict) else "Unknown venue"
        print(f"{i+1}. {name}")
    
    choice = styled_input("Choose a venue (number) or 0 to go back: ").strip()
    if choice == "0":
        return "main"
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(places):
            name = places[idx].get("tags", {}).get("name", "Unknown venue") if isinstance(places[idx], dict) else "Unknown venue"
            print(f"Raising money at {name}...")
        
        time.sleep(2)
        print("...")
        time.sleep(3)
        
        # Apply all effects
        money_raised = calc_funding_increase(state)
        state.funding += money_raised
        state.popularity += calc_popularity_increase(state)
        state.morale -= calc_morale_decrease()
        
        print(f"Raised: ${money_raised:.2f} | Funding: ${state.funding:.2f}")
        print(f"Popularity +{calc_popularity_increase(state):.2f} | Now: {state.popularity:.2f}")
        print(f"Morale -{calc_morale_decrease():.2f} | Now: {state.morale:.2f}")
    except (ValueError, IndexError):
        print("Invalid input")


def choose_morale_boost(places, state):
    venues = places.get("elements", []) if isinstance(places, dict) else []
    
    if not venues:
        print("No places found nearby.")
        return
    #LLM fun fact
    print("-----------------------------------------------")
    print(get_action_fact(state.location, "local night life"))    
    print("-----------------------------------------------")
    # Display venues
    for i, venue in enumerate(venues[:5]):
        name = venue.get("tags", {}).get("name", "Unknown place") if isinstance(venue, dict) else "Unknown place"
        print(f"{i+1}. {name}")
    
    choice = styled_input("Choose a place for fun (number) or 0 to go back: ").strip()
    if choice == "0":
        return "main"
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(venues):
            name = venues[idx].get("tags", {}).get("name", "Unknown place") if isinstance(venues[idx], dict) else "Unknown place"
            print(f"Your team goes to {name} to have fun...")
        
        time.sleep(2)
        print("... did everyone bring their ID?")
        time.sleep(3)
        
        # Apply effects
        morale_boost = calc_morale_increase(state)
        state.morale += morale_boost
        money_spent = calc_fun_cost(state)
        state.funding -= money_spent
        
        print(f"🎉 Morale +{morale_boost:.2f} | Now: {state.morale:.2f}")
        print(f"💰 Spent: ${money_spent:.2f} | Funding: ${state.funding:.2f}")
    except (ValueError, IndexError):
        print("Invalid input")


def update_to_next_location(state):
    new_location = input("Where would you like to go next? ").strip()
    found_location = get_location(new_location)
    
    if not found_location:
        print("Location not found.")
        return
    #llm fun fact
    print(f"\n{get_fun_fact(found_location['name'])}\n")
    print(f"\nTraveling from {state.location['name']} to {found_location['name']}...")
    state.locations_visited.append(new_location)
    time.sleep(2)
    
    # Travel costs
    distance = calc_distance(state.location, found_location)
    travel_cost = distance * len(state.team)
    
    if state.funding < travel_cost:
        print("Location too expensive, try somewhere closer...")
        return
    
    state.funding -= travel_cost
    
    # Team attrition
    leavers = []
    for member in state.team:
        member["productivity"] = max(member["productivity"] - random.uniform(0.5, 2), 0)
        member["motivation"] = max(member["motivation"] - random.uniform(1, 3), 0)
        if member["motivation"] <= 0:
            leavers.append(member)
    
    for m in leavers:
        print(f"{m['name']} left due to low motivation")
    
    state.team = [m for m in state.team if m["motivation"] > 0]
    
    # Events and decay
    event_roll = random.uniform(0, 10)
    if event_roll <= 2:
        random_blessing(state)
    elif event_roll >= 8:
        random_curse(state)
    
    state.morale -= calc_morale_decrease()
    state.popularity -= calc_popularity_decay(state)
    
    # Finalize
    state.location = found_location
    state.day += 1
    time.sleep(2)
    
    print_travel_summary(state, travel_cost, found_location)

def attempt_IPO(state):
    funding_score = min(state.funding / 1_000_000, 1)
    morale_score = min(state.morale / 100, 1)
    popularity_score = min(state.popularity / 100, 1)
    
    base_score = funding_score * 0.4 + morale_score * 0.3 + popularity_score * 0.3
    
    # Strong teams are consistent, weak teams get more narrow win scope
    luck = random.uniform(0.95, 1.05) if base_score >= 0.7 else random.uniform(0.8, 1.3)
    
    total_score = base_score * luck
    
    print("Attempting IPO..."); time.sleep(1); print("...Causing a huge ruckus in town"); time.sleep(1)
    
    if total_score >= 0.8:
        print(create_ipo_lore(state))
        print("\n🏆 CONGRATULATIONS! YOU WON! 🏆")
        return True
    print(create_ipo_failure_lore(state))
    print("\nKeep building. Your IPO moment will come!")
    return False