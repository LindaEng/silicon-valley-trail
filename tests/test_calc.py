import pytest
import random
from unittest.mock import patch
from types import SimpleNamespace
from utils.calc import (
    calc_popularity_increase,
    calc_morale_increase,
    calc_funding_increase,
    calc_restaurant_cost,
    calc_fun_cost,
    calc_morale_decrease,
    calc_popularity_decay,
    calc_fundraising_cost,
    calc_distance
)

@pytest.fixture
def sample_team():
    """Create a sample team for testing"""
    return [
        {"name": "Alice", "moraleImpact": 8, "productivity": 7, "cost": 100},
        {"name": "Bob", "moraleImpact": 6, "productivity": 5, "cost": 80},
        {"name": "Charlie", "moraleImpact": 9, "productivity": 8, "cost": 120},
        {"name": "Diana", "moraleImpact": 7, "productivity": 6, "cost": 90},
        {"name": "Eve", "moraleImpact": 5, "productivity": 4, "cost": 70}
    ]

@pytest.fixture
def sample_state(sample_team):
    """Create a sample game state"""
    state = SimpleNamespace()
    state.team = sample_team
    state.funding = 100000
    state.morale = 75
    state.popularity = 50
    return state


class TestRestaurantCost:
    def test_cost_per_person_range(self, sample_state):
        """Restaurant cost should be $6-25 per person"""
        with patch('random.uniform', return_value=10):
            cost = calc_restaurant_cost(sample_state)
            expected = 10 * len(sample_state.team)
            assert cost == expected

    def test_cost_scales_with_team_size(self, sample_state):
        """Larger team = higher cost"""
        costs = []
        for size in [1, 3, 5]:
            state = SimpleNamespace(team=[{"name": "test"}] * size)
            with patch('random.uniform', return_value=10):
                costs.append(calc_restaurant_cost(state))
        assert costs[0] < costs[1] < costs[2]


class TestFunCost:
    def test_cost_per_person_range(self, sample_state):
        """Fun cost should be $10-50 per person"""
        with patch('random.uniform', return_value=25):
            cost = calc_fun_cost(sample_state)
            expected = 25 * len(sample_state.team)
            assert cost == expected


class TestMoraleDecrease:
    def test_decrease_range(self):
        """Morale decrease should be between 1-3"""
        with patch('random.uniform', return_value=2):
            result = calc_morale_decrease()
            assert result == 2

    def test_decrease_is_random(self):
        """Should return different values"""
        with patch('utils.calc.random.uniform', side_effect=[1.1, 2.9]):
            r1 = calc_morale_decrease()
            r2 = calc_morale_decrease()
            assert r1 == 1
            assert r2 == 3
            assert r1 != r2


class TestPopularityIncrease:
    def test_returns_positive_value(self, sample_state):
        """Should return a positive number"""
        with patch('random.uniform', return_value=0.5):
            result = calc_popularity_increase(sample_state)
            assert result > 0

    def test_scales_with_morale_impact(self, sample_state):
        """Higher moraleImpact = higher popularity increase"""
        high_morale = SimpleNamespace(team=[{"moraleImpact": 10}])
        low_morale = SimpleNamespace(team=[{"moraleImpact": 1}])
        
        with patch('random.uniform', return_value=0.5):
            high_result = calc_popularity_increase(high_morale)
            low_result = calc_popularity_increase(low_morale)
            assert high_result > low_result


class TestMoraleIncrease:
    def test_returns_positive_value(self, sample_state):
        """Should return a positive number"""
        with patch('random.uniform', return_value=1.0):
            result = calc_morale_increase(sample_state)
            assert result > 0

    def test_scales_with_morale_impact(self, sample_state):
        """Higher moraleImpact = higher morale increase"""
        high_morale = SimpleNamespace(team=[{"moraleImpact": 10}])
        low_morale = SimpleNamespace(team=[{"moraleImpact": 1}])
        
        with patch('random.uniform', return_value=1.0):
            high_result = calc_morale_increase(high_morale)
            low_result = calc_morale_increase(low_morale)
            assert high_result > low_result


class TestFundingIncrease:
    def test_returns_positive_value(self, sample_state):
        """Should return a positive funding amount"""
        with patch('random.uniform', return_value=1.0):
            result = calc_funding_increase(sample_state)
            assert result > 0

    def test_scales_with_productivity(self, sample_state):
        """Higher productivity = higher funding"""
        high_prod = SimpleNamespace(team=[{"productivity": 10, "moraleImpact": 5}])
        low_prod = SimpleNamespace(team=[{"productivity": 1, "moraleImpact": 5}])
        
        with patch('random.uniform', return_value=1.0):
            high_result = calc_funding_increase(high_prod)
            low_result = calc_funding_increase(low_prod)
            assert high_result > low_result


class TestPopularityDecay:
    def test_never_negative(self, sample_state):
        """Popularity decay should never be negative"""
        with patch('random.uniform', return_value=0.1):
            result = calc_popularity_decay(sample_state)
            assert result >= 0

    def test_high_morale_reduces_decay(self):
        """Higher team morale should reduce decay"""
        high_morale = SimpleNamespace(team=[{"moraleImpact": 10}])
        low_morale = SimpleNamespace(team=[{"moraleImpact": 0}])
        
        with patch('random.uniform', return_value=0.1):
            high_result = calc_popularity_decay(high_morale)
            low_result = calc_popularity_decay(low_morale)
            assert high_result < low_result


class TestFundraisingCost:
    def test_never_negative(self, sample_state):
        """Fundraising cost should never be negative"""
        with patch('random.uniform', return_value=100):
            result = calc_fundraising_cost(sample_state)
            assert result >= 0

    def test_high_productivity_lowers_cost(self):
        """Higher productivity should lower cost"""
        high_prod = SimpleNamespace(team=[{"productivity": 10, "cost": 100}])
        low_prod = SimpleNamespace(team=[{"productivity": 1, "cost": 100}])
        
        with patch('random.uniform', return_value=100):
            high_result = calc_fundraising_cost(high_prod)
            low_result = calc_fundraising_cost(low_prod)
            assert high_result < low_result


class TestDistance:
    def test_different_locations_positive_distance(self):
        """Different locations should have positive distance"""
        loc1 = {"lat": "37.7749", "lon": "-122.4194"}
        loc2 = {"lat": "37.4419", "lon": "-122.1430"}
        result = calc_distance(loc1, loc2)
        assert result > 0

    def test_same_location_zero_distance(self):
        """Same location should have zero distance"""
        loc1 = {"lat": "37.7749", "lon": "-122.4194"}
        result = calc_distance(loc1, loc1)
        assert result == 0

    def test_handles_string_coordinates(self):
        """Should handle string lat/lon values"""
        loc1 = {"lat": "37.7749", "lon": "-122.4194"}
        loc2 = {"lat": "37.4419", "lon": "-122.1430"}
        result = calc_distance(loc1, loc2)
        assert isinstance(result, float)