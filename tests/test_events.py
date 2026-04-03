import random
from unittest.mock import patch
from game.events import random_blessing, random_curse

class MockState:
    def __init__(self):
        self.funding = 100000
        self.morale = 75
        self.popularity = 50

def test_events():
    print("="*50)
    print("EVENTS TESTS")
    print("="*50)
    
    tests_passed = 0
    tests_total = 6
    
    with patch('time.sleep', return_value=None):
        # Test 1: Blessing increases funding
        state = MockState()
        with patch('random.randint', side_effect=[0, 200]):
            random_blessing(state)
            if state.funding > 100000:
                tests_passed += 1
                print("  PASSED - Blessing funding")
            else:
                print("  FAILED - Blessing funding")
        
        # Test 2: Blessing increases morale
        state = MockState()
        with patch('random.randint', side_effect=[1, 15]):
            random_blessing(state)
            if state.morale > 75:
                tests_passed += 1
                print("  PASSED - Blessing morale")
            else:
                print("  FAILED - Blessing morale")
        
        # Test 3: Blessing increases popularity
        state = MockState()
        with patch('random.randint', side_effect=[2, 25]):
            random_blessing(state)
            if state.popularity > 50:
                tests_passed += 1
                print("  PASSED - Blessing popularity")
            else:
                print("  FAILED - Blessing popularity")
        
        # Test 4: Curse decreases funding
        state = MockState()
        with patch('random.randint', side_effect=[0, 200]):
            random_curse(state)
            if state.funding < 100000:
                tests_passed += 1
                print("  PASSED - Curse funding")
            else:
                print("  FAILED - Curse funding")
        
        # Test 5: Curse decreases morale
        state = MockState()
        with patch('random.randint', side_effect=[1, 15]):
            random_curse(state)
            if state.morale < 75:
                tests_passed += 1
                print("  PASSED - Curse morale")
            else:
                print("  FAILED - Curse morale")
        
        # Test 6: Curse decreases popularity
        state = MockState()
        with patch('random.randint', side_effect=[2, 25]):
            random_curse(state)
            if state.popularity < 50:
                tests_passed += 1
                print("  PASSED - Curse popularity")
            else:
                print("  FAILED - Curse popularity")
    
    print(f"\n{tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("\nALL EVENT FUNCTIONS WORKING CORRECTLY")
    else:
        print(f"\n{tests_total - tests_passed} tests failed")

if __name__ == "__main__":
    test_events()
