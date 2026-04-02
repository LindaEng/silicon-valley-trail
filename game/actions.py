from utils.loader import load_json
from utils.random import calc_productivity_increase, calc_morale_increase, calc_funding_increase, calc_restaurant_cost
from pathlib import Path
from game.state import GameState
from services.map_service import get_location, get_nearby


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
                  f"Productivity: {member['productivity']} \n"
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
        choose_cafe_restaurants(res, state)
    elif choice == "2":
        get_nearby(["coworking_space", "events"],location["lat"], location["lon"])
    elif choice == "3":
        get_nearby(["bar"],location["lat"], location["lon"])
    elif choice == "4":
        return "menu"
    else:
        print("Invalid choice")

# 0,1,2,3,4
def choose_cafe_restaurants(restaurants, state):
    for i, res in enumerate(restaurants):
        name = res["tags"].get("name", "NAME UNKNOWN")
        cuisine = res["tags"].get("cuisine", "yummy :p")
        print(f"{i}. Name: {name} - Cuisine: {cuisine} \n")
    
    choice = input("Choose a place to eat: Enter number or 0 to go back")

    try:
        if choice == "0":
            return "main"
        print("BEFORE ", state.funding, " ", state.productivity)
        # Decrease from funding cost
        state.funding -= calc_restaurant_cost(state)
        # Boost productivity 
        state.productivity += calc_productivity_increase(state)
        print("AFTER ", state.funding, " ", state.productivity)
    except (ValueError):
        print(ValueError)


