from utils.loader import load_json
from pathlib import Path


def load_splash():
    splash_path = Path(__file__).parent.parent / "assets" / "ascii"/ "splash.txt"
    with open(splash_path, "r", encoding="utf-8") as f:
        print(f.read())
    
    print("=== Silicon Valley Trail ===\n" \
          "1. New Game\n" \
          "2. Continue\n")
    
    choice = input("Choose an Option: ")

    return choice
          


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

            return [characters[i]["name"] for i in indices]

        except (ValueError, IndexError):
            print("Invalid input. Try again.\n")