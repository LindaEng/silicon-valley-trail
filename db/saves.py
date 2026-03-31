import json
from game.state import GameState

def save_game(conn, state, name="run"):
    data = json.dumps(state.to_dict())

    cursor = conn.execute(
        "INSERT INTO saves (name, state) VALUES (?, ?)",
        (name, data)
    )

    conn.commit()

    return cursor.lastrowid

def load_game(conn, save_id):
    row = conn.execute(
        "SELECT state FROM saves WHERE id = ?",
        (save_id,)
    ).fetchone()

    data = json.loads(row[0])

    return GameState.from_dict(data)



def list_saves(conn):
    rows = conn.execute(
        "SELECT id, name, created_at FROM saves"
    ).fetchall()

    return rows