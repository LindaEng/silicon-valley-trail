import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from game.engine import GameEngine
from game.state import GameState
from ui.display import styled_input, print_summary 


def test_step_increments_day():
    """Test that step() increases day by 1"""
    state = GameState(day=1)
    state.location = {"name": "Test City"}
    state.locations_visited = []
    state.funding = 1000
    state.team = [{"name": "Test"}]
    
    engine = GameEngine(state)
    
    # Choose a non-exit option (1 = explore) then next step will handle exit
    with patch('game.engine.styled_input', return_value="1"):
        with patch('game.engine.explore_city'):  # Mock explore_city
            with patch('builtins.print'):
                result = engine.step()
    
    assert state.day == 2


def test_run_advances_multiple_days():
    """Test that run() advances multiple days"""
    state = GameState(day=1)
    state.location = {"name": "Test City"}
    state.locations_visited = []
    state.funding = 1000
    state.team = [{"name": "Test"}]
    
    engine = GameEngine(state)
    
    # Mock 5 non-exit choices, then an exit
    # This simulates playing for 5 days then quitting
    user_inputs = ["1", "1", "1", "1", "1", "4"]
    
    with patch('game.engine.styled_input', side_effect=user_inputs):
        with patch('game.engine.explore_city'):  # Mock explore_city
            with patch('builtins.print'):
                engine.run()
    
    # After 5 steps, day should be 6 (started at 1, +5 days)
    assert state.day == 6


def test_step_does_not_increment_day_on_exit():
    """Test that day does NOT increment when exiting immediately"""
    state = GameState(day=5)
    state.location = {"name": "Test City"}
    state.locations_visited = []
    state.funding = 1000
    state.team = [{"name": "Test"}]
    
    engine = GameEngine(state)
    
    with patch('game.engine.styled_input', return_value="4"):  # Exit
        with patch('builtins.print'):
            result = engine.step()
    
    # Day should NOT increment when exiting
    assert state.day == 5
    assert result == "exit"


def test_check_game_over_funding_zero():
    """Test game over when funding reaches 0"""
    state = GameState(funding=0)
    engine = GameEngine(state)
    
    with patch('builtins.print'):
        result = engine.check_game_over()
    
    assert result is True


def test_check_game_over_no_team():
    """Test game over when team is empty"""
    state = GameState(team=[])
    engine = GameEngine(state)
    
    with patch('builtins.print'):
        result = engine.check_game_over()
    
    assert result is True


def test_check_game_over_continues():
    """Test game continues with positive funding and team"""
    state = GameState(funding=1000, team=[{"name": "Test"}])
    engine = GameEngine(state)
    
    result = engine.check_game_over()
    
    assert result is False


def test_handle_choice_explore():
    """Test choice 1 calls explore_city"""
    state = GameState()
    state.location = {"name": "Test", "lat": 0, "lon": 0}
    engine = GameEngine(state)
    
    with patch('game.engine.explore_city') as mock_explore:
        result = engine.handle_choice("1")
        mock_explore.assert_called_once_with(state.location, state)
        assert result is None


def test_handle_choice_check_team():
    """Test choice 2 calls check_team and returns menu"""
    state = GameState()
    engine = GameEngine(state)
    
    with patch('game.engine.check_team') as mock_check:
        result = engine.handle_choice("2")
        mock_check.assert_called_once_with(state)
        assert result == "menu"


def test_handle_choice_next_destination():
    """Test choice 3 calls update_to_next_location"""
    state = GameState()
    engine = GameEngine(state)
    
    with patch('game.engine.update_to_next_location') as mock_update:
        result = engine.handle_choice("3")
        mock_update.assert_called_once_with(state)
        assert result is None


def test_handle_choice_quit():
    """Test choice 4 returns exit"""
    state = GameState()
    engine = GameEngine(state)
    
    result = engine.handle_choice("4")
    
    assert result == "exit"


def test_handle_choice_invalid():
    """Test invalid choice prints error and returns menu"""
    state = GameState()
    engine = GameEngine(state)
    
    with patch('builtins.print') as mock_print:
        result = engine.handle_choice("99")
        mock_print.assert_called_with("invalid choice")
        assert result == "menu"


def test_handle_choice_ipo_available():
    """Test IPO option appears after 10 locations visited"""
    state = GameState()
    state.locations_visited = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    engine = GameEngine(state)
    
    with patch('game.engine.attempt_IPO', return_value=True):
        with patch('builtins.print'):
            result = engine.handle_choice("5")
            assert result == "exit"


def test_handle_choice_ipo_not_available():
    """Test IPO option not available before 10 locations"""
    state = GameState()
    state.locations_visited = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    engine = GameEngine(state)
    
    result = engine.handle_choice("5")
    
    # Should treat as invalid choice
    assert result == "menu"

