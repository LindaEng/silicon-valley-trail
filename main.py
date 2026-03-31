from db.database import init_db, get_connection
from db.saves import save_game, load_game, list_saves
from game.actions import load_splash, start_new_game, load_characters, choose_team
from game.state import GameState
from game.engine import GameEngine

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
        print("continue game")
        #get saved game from db and load it

    engine = GameEngine(state)
    engine.run()

    conn.close()

if __name__ == "__main__":
    main()