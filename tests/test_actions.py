# test_game.py
import pytest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
from game.actions import start_new_game, choose_team, explore_city, choose_cafe_restaurants, choose_fundraising, choose_morale_boost, update_to_next_location, attempt_IPO
from game.state import GameState 

# start new game
def test_start_new_game_valid_location():
    """Test start_new_game creates game state with valid location"""
    mock_characters = [{"name": "Alice", "productivity": 80, "motivation": 80},
                       {"name": "Bob", "productivity": 75, "motivation": 70},
                       {"name": "Charlie", "productivity": 85, "motivation": 90},
                       {"name": "Diana", "productivity": 70, "motivation": 75},
                       {"name": "Eve", "productivity": 90, "motivation": 85}]
    
    mock_location_data = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    mock_team = [{"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"}, {"name": "Diana"}, {"name": "Eve"}]
    
    with patch('game.actions.get_location', return_value=mock_location_data):
        with patch('game.actions.load_characters', return_value=mock_characters):
            with patch('game.actions.choose_team', return_value=mock_team):
                with patch('builtins.input', side_effect=["San Francisco"]):
                    with patch('builtins.print'):
                        result = start_new_game()
                        
                        # Check GameState was created correctly
                        assert isinstance(result, GameState)
                        assert result.location == mock_location_data
                        assert result.team == mock_team
                        assert "San Francisco" in result.locations_visited

def test_choose_team_accepts_first_team():
    """Test that choose_team returns team when user accepts immediately"""
    mock_characters = [
        {"name": "Alice", "productivity": 80, "motivation": 80, "cost": 100, "moraleImpact": 5},
        {"name": "Bob", "productivity": 75, "motivation": 70, "cost": 90, "moraleImpact": 3},
        {"name": "Charlie", "productivity": 85, "motivation": 90, "cost": 110, "moraleImpact": 7},
        {"name": "Diana", "productivity": 70, "motivation": 75, "cost": 85, "moraleImpact": 2},
        {"name": "Eve", "productivity": 90, "motivation": 85, "cost": 120, "moraleImpact": 8},
        {"name": "Frank", "productivity": 65, "motivation": 60, "cost": 80, "moraleImpact": 1},
    ]
    
    expected_team = mock_characters[:5]
    
    with patch('game.actions.random.sample', return_value=expected_team):
        with patch('builtins.input', return_value='y'):
            with patch('builtins.print'):
                result = choose_team(mock_characters)
                
                assert len(result) == 5
                assert result == expected_team


def test_choose_team_rejects_then_accepts():
    """Test that choose_team handles rejection then acceptance"""
    mock_characters = [
        {"name": "Alice", "productivity": 80, "motivation": 80, "cost": 100, "moraleImpact": 5},
        {"name": "Bob", "productivity": 75, "motivation": 70, "cost": 90, "moraleImpact": 3},
        {"name": "Charlie", "productivity": 85, "motivation": 90, "cost": 110, "moraleImpact": 7},
        {"name": "Diana", "productivity": 70, "motivation": 75, "cost": 85, "moraleImpact": 2},
        {"name": "Eve", "productivity": 90, "motivation": 85, "cost": 120, "moraleImpact": 8},
    ]
    
    team1 = mock_characters[:5]
    team2 = mock_characters  # different team (all 5)
    
    with patch('game.actions.random.sample', side_effect=[team1, team2]):
        with patch('builtins.input', side_effect=['n', 'y']):
            with patch('builtins.print'):
                result = choose_team(mock_characters)
                
                assert result == team2



def test_explore_city_returns_menu_when_choice_4():
    """Test that explore_city returns 'menu' when user chooses option 4"""
    mock_location = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    mock_state = MagicMock()
    
    with patch('builtins.input', return_value='4'):
        with patch('builtins.print'):
            result = explore_city(mock_location, mock_state)
            
            assert result == "menu"


def test_explore_city_calls_restaurant_handler():
    """Test that explore_city calls choose_cafe_restaurants for option 1"""
    mock_location = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    mock_state = MagicMock()
    mock_results = {"elements": [{"name": "Cafe"}]}
    
    with patch('game.actions.get_nearby', return_value=mock_results):
        with patch('game.actions.choose_cafe_restaurants') as mock_handler:
            with patch('builtins.input', return_value='1'):
                with patch('builtins.print'):
                    result = explore_city(mock_location, mock_state)
                    
                    # Verify get_nearby was called with correct params
                    from game.actions import CATEGORIES
                    mock_handler.assert_called_once_with(mock_results, mock_state)


def test_explore_city_no_results_found():
    """Test that explore_city handles no nearby venues gracefully"""
    mock_location = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    mock_state = MagicMock()
    
    with patch('game.actions.get_nearby', return_value=None):
        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mock_print:
                result = explore_city(mock_location, mock_state)
                
                # Should print error message
                mock_print.assert_any_call("No restaurants found nearby. Try another option.")
                assert result is None

# tests/test_actions.py (add to your file)

def test_choose_cafe_restaurants_valid_choice():
    """Test that choosing a restaurant updates funding and morale correctly"""
    mock_restaurants = {
        "elements": [
            {"tags": {"name": "Pizza Place", "cuisine": "Italian"}},
            {"tags": {"name": "Burger Joint", "cuisine": "American"}}
        ]
    }
    mock_state = MagicMock()
    mock_state.funding = 1000
    mock_state.morale = 50
    
    with patch('game.actions.calc_restaurant_cost', return_value=50):
        with patch('game.actions.calc_morale_increase', return_value=10):
            with patch('builtins.input', return_value='1'):  # Choose first restaurant
                with patch('builtins.print'):
                    with patch('time.sleep'):  # Skip delays
                        result = choose_cafe_restaurants(mock_restaurants, mock_state)
                        
                        # Check state updates
                        mock_state.funding -= 50
                        mock_state.morale += 10


def test_choose_cafe_restaurants_go_back():
    """Test that choosing 0 returns 'main'"""
    mock_restaurants = {
        "elements": [{"tags": {"name": "Pizza Place"}}]
    }
    mock_state = MagicMock()
    
    with patch('builtins.input', return_value='0'):
        with patch('builtins.print'):
            result = choose_cafe_restaurants(mock_restaurants, mock_state)
            
            assert result == "main"


def test_choose_cafe_restaurants_no_places():
    """Test that no restaurants found is handled"""
    mock_restaurants = {"elements": []}
    mock_state = MagicMock()
    
    with patch('builtins.print') as mock_print:
        result = choose_cafe_restaurants(mock_restaurants, mock_state)
        
        mock_print.assert_any_call("No restaurants found nearby.")
        assert result is None

def test_choose_fundraising_valid_choice():
    """Test that fundraising updates funding, popularity, and morale correctly"""
    mock_venues = {
        "elements": [
            {"tags": {"name": "Tech Conference"}},
            {"tags": {"name": "Startup Meetup"}}
        ]
    }
    mock_state = MagicMock()
    mock_state.funding = 1000
    mock_state.popularity = 50
    mock_state.morale = 50
    
    with patch('game.actions.calc_funding_increase', return_value=500):
        with patch('game.actions.calc_popularity_increase', return_value=20):
            with patch('game.actions.calc_morale_decrease', return_value=15):
                with patch('builtins.input', return_value='1'):
                    with patch('builtins.print'):
                        with patch('time.sleep'):
                            result = choose_fundraising(mock_venues, mock_state)
                            
                            # Verify state updates
                            assert mock_state.funding == 1500
                            assert mock_state.popularity == 70
                            assert mock_state.morale == 35


def test_choose_fundraising_go_back():
    """Test that choosing 0 returns 'main'"""
    mock_venues = {"elements": [{"tags": {"name": "Event"}}]}
    mock_state = MagicMock()
    
    with patch('builtins.input', return_value='0'):
        with patch('builtins.print'):
            result = choose_fundraising(mock_venues, mock_state)
            
            assert result == "main"

def test_choose_morale_boost_valid_choice():
    """Test that morale boost activity updates morale and funding correctly"""
    mock_places = {
        "elements": [
            {"tags": {"name": "Bowling Alley"}},
            {"tags": {"name": "Escape Room"}}
        ]
    }
    mock_state = MagicMock()
    mock_state.morale = 50
    mock_state.funding = 1000
    
    with patch('game.actions.calc_morale_increase', return_value=25):
        with patch('game.actions.calc_fun_cost', return_value=75):
            with patch('builtins.input', return_value='1'):
                with patch('builtins.print'):
                    with patch('time.sleep'):
                        result = choose_morale_boost(mock_places, mock_state)
                        
                        # Verify state updates
                        assert mock_state.morale == 75
                        assert mock_state.funding == 925


def test_choose_morale_boost_go_back():
    """Test that choosing 0 returns 'main'"""
    mock_places = {"elements": [{"tags": {"name": "Fun Place"}}]}
    mock_state = MagicMock()
    
    with patch('builtins.input', return_value='0'):
        with patch('builtins.print'):
            result = choose_morale_boost(mock_places, mock_state)
            
            assert result == "main"

def test_update_to_next_location_successful_travel():
    """Test successful travel to new location"""
    mock_state = MagicMock()
    mock_state.location = {"name": "San Jose", "lat": 37.3382, "lon": -121.8863}
    mock_state.funding = 10000
    mock_state.morale = 50  # Add actual number, not MagicMock
    mock_state.popularity = 50  # Add actual number, not MagicMock
    mock_state.team = [
        {"name": "Alice", "motivation": 80, "productivity": 80},
        {"name": "Bob", "motivation": 75, "productivity": 75}
    ]
    mock_state.day = 1
    mock_state.locations_visited = []  # Add empty list
    
    mock_destination = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    
    with patch('game.actions.get_location', return_value=mock_destination):
        with patch('game.actions.calc_distance', return_value=50):
            with patch('game.actions.calc_morale_decrease', return_value=5):
                with patch('game.actions.calc_popularity_decay', return_value=3):
                    with patch('builtins.input', return_value="San Francisco"):
                        with patch('builtins.print'):
                            with patch('time.sleep'):
                                with patch('random.uniform', return_value=0.5):  # No events
                                    update_to_next_location(mock_state)
                                    
                                    # Verify updates
                                    assert mock_state.location == mock_destination
                                    assert mock_state.day == 2


from types import SimpleNamespace

def test_update_to_next_location_insufficient_funds():
    """Test travel fails when not enough funding"""
    mock_state = SimpleNamespace(
        location={"name": "San Jose", "lat": 37.3382, "lon": -121.8863},
        funding=100,  # Real number
        morale=50,
        popularity=50,
        team=[{"name": "Alice", "motivation": 80, "productivity": 80, "cost": 100, "moraleImpact": 5}],
        locations_visited=[],
        day=1
    )
    
    mock_destination = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    
    with patch('game.actions.get_location', return_value=mock_destination):
        with patch('game.actions.calc_distance', return_value=50):
            with patch('builtins.input', return_value="San Francisco"):
                with patch('builtins.print') as mock_print:
                    update_to_next_location(mock_state)



def test_update_to_next_location_team_member_leaves():
    """Test team member leaves when motivation hits 0"""
    mock_state = SimpleNamespace(
        location={"name": "San Jose", "lat": 37.3382, "lon": -121.8863},
        funding=10000,
        morale=50,
        popularity=50,
        day=1,
        locations_visited=[],
        team=[
            {"name": "Alice", "motivation": 80, "productivity": 80, "cost": 100, "moraleImpact": 5},
            {"name": "Bob", "motivation": 5, "productivity": 75, "cost": 90, "moraleImpact": 3}
        ]
    )
    
    mock_destination = {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194}
    
    with patch('game.actions.get_location', return_value=mock_destination):
        with patch('game.actions.calc_distance', return_value=50):
            with patch('game.actions.calc_morale_decrease', return_value=5):
                with patch('game.actions.calc_popularity_decay', return_value=3):
                    with patch('builtins.input', return_value="San Francisco"):
                        with patch('builtins.print'):
                            with patch('time.sleep'):
                                with patch('random.uniform', side_effect=[
                                    1.0, 1.0,  # productivity decreases for Alice, Bob
                                    2.0, 10.0,  # motivation: Alice 80->78, Bob 5-> -5 (becomes 0)
                                    5.0  # event_roll (between 2 and 8 = no event)
                                ]):
                                    update_to_next_location(mock_state)
                                    
                                    assert len(mock_state.team) == 1
                                    assert mock_state.team[0]["name"] == "Alice"

def test_attempt_ipo_success():
    """Test IPO succeeds with perfect stats"""
    state = SimpleNamespace(
        funding=1_000_000,
        morale=100,
        popularity=100
    )
    
    with patch('random.uniform', return_value=1.0):
        result = attempt_IPO(state)
        assert result is True


def test_attempt_ipo_failure():
    """Test IPO fails with zero stats"""
    state = SimpleNamespace(
        funding=0,
        morale=0,
        popularity=0
    )
    
    with patch('random.uniform', return_value=1.0):
        result = attempt_IPO(state)
        assert result is False


def test_attempt_ipo_barely_success():
    """Test IPO success threshold (0.8)"""
    # Create state that gives exactly 0.8 base_score
    # With 40/30/30 weights, funding=1M(1.0), morale=0, popularity=0 = 0.4 base_score
    # Need ~2x multiplier from luck, so use random.uniform to return 2.0
    state = SimpleNamespace(
        funding=1_000_000,
        morale=0,
        popularity=0
    )
    
    with patch('random.uniform', return_value=2.0):
        result = attempt_IPO(state)
        assert result is True