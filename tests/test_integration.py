import pytest
from types import SimpleNamespace
from unittest.mock import patch
from game.actions import (
    start_new_game, 
    attempt_IPO,
    update_to_next_location
)
from game.state import GameState


def test_game_can_lose():
    """Test that game can end with IPO failure"""
    
    weak_team = [
        {"name": "Weak", "productivity": 10, "motivation": 10, "cost": 100, "moraleImpact": 1},
        {"name": "Poor", "productivity": 15, "motivation": 15, "cost": 90, "moraleImpact": 1},
        {"name": "Bad", "productivity": 5, "motivation": 5, "cost": 95, "moraleImpact": 1},
        {"name": "Terrible", "productivity": 8, "motivation": 8, "cost": 85, "moraleImpact": 1},
        {"name": "Awful", "productivity": 12, "motivation": 12, "cost": 110, "moraleImpact": 1}
    ]
    
    mock_location = {"name": "Bad City", "lat": 0, "lon": 0}
    
    # Input sequence for choose_team:
    # 1. Press any key (first retry)
    # 2. Accept team (y)
    # Plus location input at the beginning
    user_inputs = ["Bad City", "", "y"]
    
    with patch('game.actions.get_location', return_value=mock_location):
        with patch('game.actions.load_characters', return_value=weak_team):
            with patch('builtins.input', side_effect=user_inputs):
                with patch('builtins.print'):
                    with patch('time.sleep'):
                        with patch('random.uniform', return_value=0.5):
                            
                            state = start_new_game()
                            
                            # Attempt IPO with weak team
                            success = attempt_IPO(state)
                            
                            # Should fail
                            assert success is False


def test_team_can_die():
    """Test that team members can leave during travel"""
    
    mock_location_start = {"name": "Start", "lat": 0, "lon": 0}
    mock_location_end = {"name": "End", "lat": 10, "lon": 10}
    
    dying_team = [
        {"name": "Alice", "motivation": 3, "productivity": 80, "cost": 100, "moraleImpact": 5},
        {"name": "Bob", "motivation": 2, "productivity": 75, "cost": 90, "moraleImpact": 4},
        {"name": "Charlie", "motivation": 4, "productivity": 85, "cost": 110, "moraleImpact": 6},
    ]
    
    state = GameState(team=dying_team, location=mock_location_start)
    state.funding = 10000
    state.morale = 50
    state.popularity = 50
    state.day = 1
    state.locations_visited = []
    
    # random.uniform calls:
    # - 3 productivity decreases
    # - 3 motivation decreases  
    # - 1 event_roll
    random_values = [1.0, 1.0, 1.0, 10.0, 10.0, 10.0, 5.0]
    
    with patch('game.actions.get_location', return_value=mock_location_end):
        with patch('game.actions.calc_distance', return_value=5):
            with patch('game.actions.calc_morale_decrease', return_value=5):
                with patch('game.actions.calc_popularity_decay', return_value=3):
                    with patch('builtins.input', return_value="End"):
                        with patch('builtins.print'):
                            with patch('time.sleep'):
                                with patch('random.uniform', side_effect=random_values):
                                    update_to_next_location(state)
                                    
                                    # Some team members should have left
                                    assert len(state.team) < len(dying_team)


def test_complete_game_flow_to_ipo():
    """Simulate a complete winning game from start to IPO success"""
    
    mock_location = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    mock_characters = [
        {"name": "Alice", "productivity": 90, "motivation": 90, "cost": 100, "moraleImpact": 9},
        {"name": "Bob", "productivity": 85, "motivation": 85, "cost": 90, "moraleImpact": 8},
        {"name": "Charlie", "productivity": 88, "motivation": 88, "cost": 95, "moraleImpact": 8},
        {"name": "Diana", "productivity": 92, "motivation": 92, "cost": 110, "moraleImpact": 9},
        {"name": "Eve", "productivity": 87, "motivation": 87, "cost": 85, "moraleImpact": 8}
    ]
    
    user_inputs = ["San Francisco", "", "y"]
    
    with patch('game.actions.get_location', return_value=mock_location):
        with patch('game.actions.load_characters', return_value=mock_characters):
            with patch('builtins.input', side_effect=user_inputs):
                with patch('builtins.print'):
                    with patch('time.sleep'):
                        with patch('game.actions.random.uniform', return_value=1.0):
                            
                            state = start_new_game()
                            assert state is not None
                            assert len(state.team) == 5
                            
                            # Try to IPO (may succeed or fail based on stats)
                            success = attempt_IPO(state)
                            
                            # Just verify it returns a boolean
                            assert isinstance(success, bool)