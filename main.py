from db.database import init_db, get_connection
from db.saves import save_game, load_game, list_saves
from game.actions import load_splash, load_characters, choose_team
from game.state import GameState
from game.engine import GameEngine

def main():
    conn = get_connection()
    init_db(conn)

    print("starting game")

    choice = load_splash()

    print("you chose: ", choice)

    conn.close()

if __name__ == "__main__":
    main()