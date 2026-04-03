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
    try:
        row = conn.execute(
            "SELECT state FROM saves WHERE id = ?",
            (save_id,)
        ).fetchone()
        
        if row is None:
            print(f"No save found with id {save_id}")
            return None
        
        print(f"DEBUG: row[0] type = {type(row[0])}")
        print(f"DEBUG: row[0] first 200 chars = {row[0][:200]}")
        
        data = json.loads(row[0])
        print(f"DEBUG: data keys = {data.keys()}")
        print(f"DEBUG: data has 'locations_visited'? {'locations_visited' in data}")
        
        state = GameState.from_dict(data)
        print(f"DEBUG: state created successfully, funding={state.funding}")
        
        return state
    except Exception as e:
        print(f"Error loading save {save_id}: {e}")
        import traceback
        traceback.print_exc()
        return None


def list_saves(conn):
    rows = conn.execute(
        "SELECT id, name, state, created_at FROM saves"
    ).fetchall()

    return rows