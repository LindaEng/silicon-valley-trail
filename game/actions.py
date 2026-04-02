from utils.loader import load_json
from utils.calc import calc_popularity_increase, calc_morale_increase, calc_funding_increase, calc_restaurant_cost, calc_morale_decrease,  calc_popularity_decay, calc_distance, calc_fun_cost
from pathlib import Path
from game.state import GameState
from services.map_service import get_location, get_nearby
import time
import random


def load_splash():
    splash_path = Path(__file__).parent.parent / "assets" / "ascii"/ "splash.txt"
    with open(splash_path, "r", encoding="utf-8") as f:
        print(f.read())
    
    print("=== Silicon Valley Trail ===\n" \
          "1. New Game\n" \
          "2. Continue\n")
    
    choice = input("Choose an Option: ")
    return choice


def start_new_game():
    print("\n---New Game---")

    print("\nYou are setting out on a journey through Silicon Valley...")
    print("Build your team. Navigate the chaos. Ship or die.\n")
    print("But first -- where would you like to start?\n")

    # first_state = GameState()
    location = input("Enter location ")
    location_data = get_location(location)
    if location_data:

        print("You chose: ", location)
    else:
        print("Location not found, using raw input")
    print("------------------------------")
    print("Lets choose your dream team! ")
    team = choose_team(load_characters())
    print(team)
    new_game_state = GameState(team = team, location = location_data or {"name": location})
    print("THIS IS YOUR FINAL TEAM ", new_game_state.to_dict())
    return new_game_state


def load_characters():
    return load_json("data/characters.json")

def choose_team(characters):
    while True:
        print("Choose your team (at least 5, comma separated indices):")

        for i, char in enumerate(characters):
            print(f"{i}: {char['name']}")

        choices = input("Your team: ")

        try:
            indices = [int(i.strip()) for i in choices.split(",")]

            if len(indices) < 5:
                print("Please select at least 5 characters.\n")
                continue

            return [characters[i] for i in indices]

        except (ValueError, IndexError):
            print("Invalid input. Try again.\n")

def check_team(state):
    while True:
        print("\n Your team: ")
        for i, member in enumerate(state.team):
            print("=================")
            print(f"{i}: \n")
            print(f"Name: {member['name']}: \n"
                  f"Motivation: {member['motivation']} \n"
                  f"popularity: {member['popularity']} \n"
                  f"Cost: {member['cost']} \n"
                  f"Morale Impact: {member['moraleImpact']} \n"
                  )
        
        back = input("Go back to menu? y/n: ")
        if back == "y":
            return "menu"
       

def explore_city(location, state):
    print("=================")
    print("\n What would you like to do? \n")
    print("1. Find cafes/restaurants \n")
    print("2. Find events to raise money\n")
    print("3. Team Booster \n")
    print("4. Back to Menu")

    choice = input("Your choice: Input number ")

    if choice == "1":
        res = get_nearby(["cafe", "restaurant"],location["lat"], location["lon"])
        if len(res): 
            choose_cafe_restaurants(res, state)
    elif choice == "2":
        res = get_nearby(["coworking_space", "events"],location["lat"], location["lon"])
        if len(res):
            choose_fundraising(res, state)
    elif choice == "3":
        res = get_nearby(["bar", "gym"],location["lat"], location["lon"])
        if len(res):
            choose_morale_boost(res, state)
    elif choice == "4":
        return "menu"
    else:
        print("Invalid choice")

# 0,1,2,3,4
def choose_cafe_restaurants(restaurants, state):
    for i, res in enumerate(restaurants):
        name = res["tags"].get("name", "NAME UNKNOWN")
        cuisine = res["tags"].get("cuisine", "yummy :p")
        print(f"{i+1}. Name: {name} - Cuisine: {cuisine} \n")
    
    choice = input("Choose a place to eat: Enter number or 0 to go back ")

    try:
        if choice == "0":
            return "main"
        print("Your team decides to get a bite to eat and recharge ")
        time.sleep(2)
        cost = calc_restaurant_cost(state)
        state.funding -= cost
        print(f"That meal cost your team: ${cost}. Your total funding is now ${state.funding}")
        time.sleep(1)
        morale_boost = calc_morale_increase(state)
        state.morale += morale_boost
        print(f"Your team feels recharged! Morale up by {morale_boost}. Morale is now: {state.morale}")
    except (ValueError):
        print(ValueError)

def choose_fundraising(venues, state):
    for i, res in enumerate(venues):
        name = res["tags"].get("name", "NAME UNKNOWN")
        print(f"{i+1}. Name: {name} \n")
    
    choice = input("Choose a place to fundraise: Enter number or 0 to go back")

    try:
        if choice == "0":
            return "main"
        print("Your team tries to raise money.... ")
        time.sleep(2)
        print("...")
        time.sleep(3)
        money_raised = calc_funding_increase(state)
        state.funding += money_raised
        print(f"Your team has raised {money_raised}, now totaling: ${state.funding}. ")
        time.sleep(2)
        increased_pop = calc_popularity_increase(state)
        state.popularity += increased_pop
        print(f"All that talking has caused quite the buzz... popularity increased by {increased_pop}. ")
        time.sleep(2)
        decr_morale = calc_morale_decrease(state)
        state.morale -= decr_morale
        print(f"All that talking is pretty tiring... Morale decreased by {decr_morale}")
    except (ValueError):
        print(ValueError)


def choose_morale_boost(places, state):
    for i, res in enumerate(places):
        name = res["tags"].get("name", "NAME UNKNOWN")
        print(f"{i}. Name: {name} \n")
    
    choice = input("Choose a place to have fun: Enter number or 0 to go back")

    try:
        if choice == "0":
            return "main"
        print("Your team jumps for joy as they go do something fun.... ")
        time.sleep(2)
        print("... did everyone bring their ID? ")
        time.sleep(3)
        morale_boost = calc_morale_increase(state)
        state.morale += morale_boost
        print(f"Your team feels better bonded! hip hip hooray! Moral has increased +{morale_boost} totaling: {state.morale}")
        time.sleep(2)
        print("Having fun also means spending $ and burning time away from working towards an IPO... ")
        money_spent = calc_fun_cost(state)
        state.popularity -= money_spent
        print("AFTER ", state.funding, " ", state.popularity)
    except (ValueError):
        print(ValueError)    


def update_to_next_location(state):
    new_location = input("Where would you like to go next? ")
    found_location = get_location(new_location)

    if not found_location:
        print("Location not found.")
        return

    print(f"\nTraveling to {found_location['name']}...")
    time.sleep(2)
    # --- COST ---
    travel_cost = calc_distance(state.location, found_location) * len(state.team)
    if state.funding < travel_cost:
        print("Location too expensive, try somewhere closer...")
        return
    state.funding -= travel_cost

    # --- TEAM EFFECTS ---
    leavers = []
    
    for member in state.team:
        member["productivity"] = max(member["productivity"] - random.uniform(0.5, 2), 0)
        member["motivation"] = max(member["motivation"] - random.uniform(1, 3), 0)

        if member["motivation"] <= 0:
            leavers.append(member)

    avg_morale = (sum(m["motivation"] for m in state.team) / len(state.team)) / 100 
    state.morale = state.morale * avg_morale
    state.popularity -= random.uniform(5,10)
    # --- REMOVE MEMBERS WITH 0 MORALE ---

    # print who left
    for m in leavers:
        print(f"{m['name']} has left the team due to low morale....")

    # update team
    state.team = [m for m in state.team if m["motivation"] > 0]
    
    # --- UPDATE LOCATION ---
    state.location = found_location
    time.sleep(2)
    print(f"Welcome to: {found_location['name']}")
    print(f"Travel cost: ${travel_cost:.2f}")
    print(f"Remaining team members: {len(state.team)}")
    print(f"Team Health = \n",
          f" Funding: {state.funding:.2f}\n"
          f" Morale: {state.morale}\n"
          f" popularity: {state.morale}\n"
          f" Day: {state.day}\n")
