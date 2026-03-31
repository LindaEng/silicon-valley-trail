from db.database import init_db, get_connection
from db.saves import save_game, load_game, list_saves
from game.actions import load_characters, choose_team
from game.state import GameState

def main():
    conn = get_connection()
    init_db(conn)

    state = GameState()
    print("Initial:", state.to_dict())

    save_id = save_game(conn, state)
    print("Saved game")

    loaded = load_game(conn, save_id)
    print("Loaded:", loaded.to_dict())

    print("All saves")
    for row in list_saves(conn):
        print(row)
    
    characters = load_characters()
    team = choose_team(characters)

    state.team = team
    print("Selected team:", state.team)

    conn.close()

if __name__ == "__main__":
    main()