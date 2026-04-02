from db.database import init_db, get_connection
from db.saves import save_game, load_game, list_saves
from game.actions import load_splash, start_new_game, load_characters, choose_team
from game.state import GameState
from game.engine import GameEngine

import json

def main():
    conn = get_connection()
    init_db(conn)
    print("starting game")
    choice = load_splash()

    state = None

    if choice == "1":
        print("STARTTTT ")
        state = start_new_game()

    elif choice == "2":
        print("Continue game")
        saves = list_saves(conn)
        if not saves:
            print("No saved games found.")
            state = start_new_game()
        else:
            print("\nAvailable saves:")
            for row in saves:
                data = json.loads(row[2])
                print(f"Slot {row[0]}: Location: {data['location']['name']}, Day: {data['day']}")
            slot = input("Choose save slot to load from: ")
            try:
                slot = int(slot)
                state = load_game(conn, slot)
            except:
                print("Invalid selection, starting new game.")
                state = start_new_game()

    engine = GameEngine(state)
    result = engine.run()

    if result == "exit":
        save_game(conn, state)
        print("Game saved!! ")

    conn.close()

if __name__ == "__main__":
    main()