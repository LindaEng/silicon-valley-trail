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
                try:
                    save_id = row[0]
                    data = row[1]  
                    
                    if data:
                        print(f"Slot {save_id}: Location: {data.get('location', {}).get('name', 'Unknown')}, Day: {data.get('day', 'Unknown')}")
                    else:
                        print(f"Slot {save_id}: Corrupted save data")
                except Exception as e:
                    print(f"Slot {row[0]}: Error - {e}")
            
            slot = input("Choose save slot to load from: ")
            try:
                slot = int(slot)
                if slot < 1:  
                    print("Invalid selection, starting new game.")
                    state = start_new_game()
                else:
                    state = load_game(conn, slot)
                    if state is None:
                        print("Failed to load save, starting new game.")
                        state = start_new_game()
            except ValueError:
                print("Invalid selection, starting new game.")
                state = start_new_game()

    if state is None:
        print("Something went wrong, starting new game.")
        state = start_new_game()

    engine = GameEngine(state)
    result = engine.run()

    if result == "exit":
        save_game(conn, state)
        print("Game saved!! ")

    conn.close()

if __name__ == "__main__":
    main()