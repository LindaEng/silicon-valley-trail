from game.engine import GameEngine
from game.state import GameState

def test_step_increments_day():
    state = GameState(day=1)
    engine = GameEngine(state)

    engine.step()

    assert state.day == 2

def test_run_advances_multiple_days():
    state = GameState(day=1)
    engine = GameEngine(state)

    engine.run()

    assert state.day == 6  