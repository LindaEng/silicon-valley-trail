from utils.loader import load_json
from utils.calc import calc_popularity_increase, calc_morale_increase, calc_funding_increase, calc_restaurant_cost, calc_morale_decrease,  calc_popularity_decay, calc_distance, calc_fun_cost
from ui.display import print_character
from pathlib import Path
from game.state import GameState
from game.events import random_blessing, random_curse
from services.map_service import get_location, get_nearby
from utils.cache import CATEGORIES
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
    new_game_state.locations_visited.append(location)
    print("THIS IS YOUR FINAL TEAM ", new_game_state.to_dict())
    return new_game_state


def load_characters():
    return load_json("data/characters.json")

def choose_team(characters):
    retries = 3
    while retries > 0:
        print("Choose your team (at least 5, comma separated indices):")

        for character in characters:
            print_character(character)

        input(f"We will randomly select a group of 5 players. You have {retries} retries. press any key to continue")

        try:
            print("Finding your dream team ... ")
            time.sleep(2)
            team = random.sample(characters, 5)
            print("Here is the team! ")
            for member in team:
                print_character(member)
            choice = input(f"Do you accept this team? press 'y' to accept or 'n' to re-pick team. {retries - 1} left. ")
            if choice == 'y':
                return team
            retries -= 1
            print("Let's try to find a better team... ")
            time.sleep(2)
            if retries == 0:
                print("No more retries - assigning final team")
                time.sleep(2)
                for member in team:
                    print_character(member)
                return team
        except (ValueError, IndexError):
            print("Invalid input. Try again.\n")

def check_team(state):
    while True:
        print("\n Your team: ")
        for member in state.team:
            print_character(member)
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
    lat = location["lat"]
    lon = location["lon"]
    
    if choice == "1":
        res = get_nearby(CATEGORIES["restaurants"], lat, lon)
        if res and isinstance(res, dict) and res.get("elements") and len(res["elements"]) > 0:
            choose_cafe_restaurants(res, state)
        else:
            print("No restaurants or cafes found nearby. Try another option.")
            
    elif choice == "2":
        res = get_nearby(CATEGORIES["events"], lat, lon)
        if res and isinstance(res, dict) and res.get("elements") and len(res["elements"]) > 0:
            choose_fundraising(res, state)
        else:
            print("No events found nearby. Try another option.")
            
    elif choice == "3":
        res = get_nearby(CATEGORIES["fun"], lat, lon)
        if res and isinstance(res, dict) and res.get("elements") and len(res["elements"]) > 0:
            choose_morale_boost(res, state)
        else:
            print("No entertainment venues found nearby. Try another option.")
            
    elif choice == "4":
        return "menu"
    else:
        print("Invalid choice")

def choose_cafe_restaurants(restaurants, state):
    
    if not isinstance(restaurants, dict) or "elements" not in restaurants:
        print("No restaurants found nearby.")
        return
    
    places = restaurants["elements"]
    
    if not places:
        print("No restaurants found nearby.")
        return
    
    for i, place in enumerate(places[:5]):
        if isinstance(place, dict) and "tags" in place:
            name = place["tags"].get("name", "NAME UNKNOWN")
            cuisine = place["tags"].get("cuisine", "yummy :p")
            print(f"{i+1}. Name: {name} - Cuisine: {cuisine}")
        else:
            print(f"{i+1}. Unknown place")
    
    choice = input("Choose a place to eat: Enter number or 0 to go back ")

    try:
        if choice == "0":
            return "main"
        idx = int(choice) - 1
        if 0 <= idx < len(places):
            selected = places[idx]
            if isinstance(selected, dict) and "tags" in selected:
                name = selected["tags"].get("name", "Unknown place")
                print(f"Your team decides to get a bite to eat at {name} and recharge")
        else:
            print("Invalid choice, using default")
        
        time.sleep(2)
        cost = calc_restaurant_cost(state)
        state.funding -= cost
        print(f"That meal cost your team: ${cost:.2f}. Your total funding is now ${state.funding:.2f}")
        time.sleep(1)
        morale_boost = calc_morale_increase(state)
        state.morale += morale_boost
        print(f"Your team feels recharged! Morale up by {morale_boost:.2f}. Morale is now: {state.morale:.2f}")
    except (ValueError, IndexError):
        print("Invalid input")

def choose_fundraising(venues, state):
    if not isinstance(venues, dict) or "elements" not in venues:
        print("No venues found nearby.")
        return
    
    places = venues["elements"]
    
    if not places:
        print("No venues found nearby.")
        return
    
    for i, place in enumerate(places[:5]):
        if isinstance(place, dict) and "tags" in place:
            name = place["tags"].get("name", "NAME UNKNOWN")
            print(f"{i+1}. Name: {name}")
        else:
            print(f"{i+1}. Unknown venue")
    
    choice = input("Choose a place to fundraise: Enter number or 0 to go back ")

    try:
        if choice == "0":
            return "main"
        idx = int(choice) - 1
        if 0 <= idx < len(places):
            selected = places[idx]
            if isinstance(selected, dict) and "tags" in selected:
                name = selected["tags"].get("name", "Unknown venue")
                print(f"Your team tries to raise money at {name}....")
        else:
            print("Invalid choice, using default")
        
        time.sleep(2)
        print("...")
        time.sleep(3)
        money_raised = calc_funding_increase(state)
        state.funding += money_raised
        print(f"Your team has raised ${money_raised:.2f}, now totaling: ${state.funding:.2f}. ")
        time.sleep(2)
        increased_pop = calc_popularity_increase(state)
        state.popularity += increased_pop
        print(f"All that talking has caused quite the buzz... popularity increased by {increased_pop:.2f}. ")
        time.sleep(2)
        decr_morale = calc_morale_decrease(state)
        state.morale -= decr_morale
        print(f"All that talking is pretty tiring... Morale decreased by {decr_morale:.2f}")
    except (ValueError, IndexError):
        print("Invalid input")


def choose_morale_boost(places, state):
    if not isinstance(places, dict) or "elements" not in places:
        print("No places found nearby.")
        return
    
    venues = places["elements"]
    
    if not venues:
        print("No places found nearby.")
        return
    
    for i, venue in enumerate(venues[:5]):
        if isinstance(venue, dict) and "tags" in venue:
            name = venue["tags"].get("name", "NAME UNKNOWN")
            print(f"{i+1}. Name: {name}")
        else:
            print(f"{i+1}. Unknown place")
    
    choice = input("Choose a place to have fun: Enter number or 0 to go back ")

    try:
        if choice == "0":
            return "main"
        idx = int(choice) - 1
        if 0 <= idx < len(venues):
            selected = venues[idx]
            if isinstance(selected, dict) and "tags" in selected:
                name = selected["tags"].get("name", "Unknown place")
                print(f"Your team jumps for joy as they go to {name} to have fun....")
        else:
            print("Invalid choice, using default")
        
        time.sleep(2)
        print("... did everyone bring their ID? ")
        time.sleep(3)
        morale_boost = calc_morale_increase(state)
        print(f"Your team feels better bonded! hip hip hooray! Moral has increased +{morale_boost:.2f} going from {state.morale:.2f} to totaling: {state.morale + morale_boost:.2f}")
        state.morale += morale_boost
        time.sleep(2)
        money_spent = calc_fun_cost(state)

        print(f"Having fun also means spending $ and burning time away from working towards an IPO... You spent: ${money_spent:.2f}. Before: ${state.funding:.2f} -> After: ${state.funding - money_spent:.2f}")
        state.funding -= money_spent
    except (ValueError, IndexError):
        print("Invalid input")    


def update_to_next_location(state):
    new_location = input("Where would you like to go next? ")
    found_location = get_location(new_location)

    if not found_location:
        print("Location not found.")
        return

    print(f"\nTraveling from {state.location['name']} to {found_location['name']}...")

    state.locations_visited.append(new_location)
    time.sleep(2)

    distance_traveled = calc_distance(state.location, found_location)
    travel_cost = distance_traveled * len(state.team)
    if state.funding < travel_cost:
        print("Location too expensive, try somewhere closer...")
        return
    state.funding -= travel_cost

    leavers = []
    
    for member in state.team:
        member["productivity"] = max(member["productivity"] - random.uniform(0.5, 2), 0)
        member["motivation"] = max(member["motivation"] - random.uniform(1, 3), 0)
        if member["motivation"] <= 0:
            leavers.append(member)

    for m in leavers:
        print(f"{m['name']} has left the team due to low morale....")

    state.team = [m for m in state.team if m["motivation"] > 0]

    #------ Events -------#
    random_event = random.uniform(0,10)
    if random_event <= 2:
        random_blessing(state)
    elif random_event >= 8:
        random_curse(state)
    state.morale -= calc_morale_decrease()
    state.popularity -= calc_popularity_decay(state)
    #---------------------#
    state.location = found_location
    state.day += 1
    time.sleep(2)
    print(f"Welcome to: {found_location['name']}")
    print(f"Travel cost: ${travel_cost:.2f}")
    print(f"Remaining team members: {len(state.team)}")
    print(f" Team Health = \n",
          f" Funding: {state.funding:.2f}\n"
          f" Morale: {state.morale:.2f}\n"
          f" popularity: {state.morale:.2f}\n"
          f" Day: {state.day}\n")

def attempt_IPO(state):
    funding_score = min(state.funding / 1_000_000, 1)
    morale_score = min(state.morale / 100, 1)
    popularity_score = min(state.popularity / 100, 1)

    base_score = (
        funding_score * 0.5 +
        morale_score * 0.25 +
        popularity_score * 0.25
    )

    if base_score >= 0.8:
        luck = random.uniform(0.8, 1.3)
    elif base_score >= 0.5:
        luck = random.uniform(0.9, 1.1)
    else:
        luck = random.uniform(0.95, 1.05)

    total_score = base_score * luck
    print("Attempting to IPO ")
    time.sleep(1)
    print("... Causing a huge ruckus in town")
    time.sleep(1)
    if total_score >= 0.85:
        print("IPO successful 🚀")
        return True
    elif total_score >= 0.7:
        print("IPO almost made it — investors hesitant... keep building popularity and funding. You're almost there!")
        return False
    else:
        print("IPO failed — not enough traction")
        return False
