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
        
        data = json.loads(row[0])
        state = GameState.from_dict(data)
        
        return state
    except Exception as e:
        print(f"Error loading save {save_id}: {e}")
        return None


def list_saves(conn):
    rows = conn.execute(
        "SELECT id, state FROM saves ORDER BY id"
    ).fetchall()
    
    # Convert state from JSON string to dict for each row
    result = []
    for row in rows:
        save_id = row[0]
        state_data = row[1]
        
        # Parse the JSON string to dict
        if isinstance(state_data, str):
            try:
                state_dict = json.loads(state_data)
                result.append((save_id, state_dict))
            except:
                print(f"Warning: Could not parse save {save_id}")
                result.append((save_id, None))
        else:
            result.append((save_id, state_data))
    
    return result