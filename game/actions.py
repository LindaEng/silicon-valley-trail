from utils.loader import load_json

def load_characters():
    return load_json("data/characters.json")

def choose_team(characters):
    print("Choose your team (enter indices, comma separated):")

    for i, char in enumerate(characters):
        print(f"{i}: {char['name']}")

    choices = input("Your team: ")
    indices = [int(i.strip()) for i in choices.split(",")]

    return [characters[i]["name"] for i in indices]