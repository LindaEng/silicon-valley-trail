from game.engine import GameEngine
from game.state import GameState

def test_step_increments_day():
    state = GameState(day=1)
    engine = GameEngine(state)

    engine.step()

    assert state.day == 2