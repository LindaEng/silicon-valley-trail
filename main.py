from db.database import init_db, get_connection
from db.saves import save_game, load_game, list_saves
from game.state import GameState

def main():
    # Entry Point
    init_db()
    conn = get_connection()

    state = GameState()
    print("Initial:", state.to_dict())

    save_game(conn, state)
    print("Saved game")

    loaded = load_game(conn, 1)
    print("Loaded:", loaded.to_dict())

    print("All saves")
    for row in list_saves(conn):
        print(row)

if __name__ == "__main__":
    main()