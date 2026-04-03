from db.database import init_db, get_connection
from db.saves import save_game, load_game
from game.state import GameState

def test_save_and_load():
    conn = get_connection()
    init_db(conn)

    # create state
    state = GameState(funding=500, morale=80, popularity="99", team=["A"], location="NYC", day=1, locations_visited=["NYC"])

    # test save
    save_id = save_game(conn, state)

    # test load 
    loaded = load_game(conn, save_id)

    assert loaded.to_dict() == state.to_dict()