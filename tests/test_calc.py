import random
from game.state import GameState

def calc_popularity_increase(state):
    avg = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return round((avg * random.uniform(0.1, 1)),2)

def calc_morale_increase(state):
    avg = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return round((avg * random.uniform(0.8, 1.2)),2)

def calc_funding_increase(state):
    prod = sum(m["productivity"] for m in state.team) / len(state.team)
    morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return round((100000 * (prod/10) * (1 + morale/10) * random.uniform(0.5, 5)),2)

def calc_restaurant_cost(state):
    return round((random.uniform(6, 25) * len(state.team)),2)

def calc_fun_cost(state):
    return round((random.uniform(10, 50) * len(state.team)),2)

def calc_morale_decrease():
    return round(random.uniform(1,3))

def calc_popularity_decay(state):
    avg_morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    morale_factor = avg_morale / 10
    base_decay = random.uniform(0.05, 0.15)
    decay = base_decay - morale_factor
    return round(max(decay, 0),2)

def calc_fundraising_cost(state):
    avg_prod = sum(m["productivity"] for m in state.team) / len(state.team)
    avg_cost = sum(m["cost"] for m in state.team) / len(state.team)
    return round(max(random.uniform(50, 500) * (1 + avg_cost/100 - avg_prod/100), 0),2)

def calc_distance(loc1, loc2):
    lat1 = float(loc1["lat"])
    lon1 = float(loc1["lon"])
    lat2 = float(loc2["lat"])
    lon2 = float(loc2["lon"])
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2
    return (lat_diff**2 + lon_diff**2) ** 0.5

def create_test_team():
    return [
        {"name": "Alice", "moraleImpact": 8, "productivity": 7, "cost": 100},
        {"name": "Bob", "moraleImpact": 6, "productivity": 5, "cost": 80},
        {"name": "Charlie", "moraleImpact": 9, "productivity": 8, "cost": 120},
        {"name": "Diana", "moraleImpact": 7, "productivity": 6, "cost": 90},
        {"name": "Eve", "moraleImpact": 5, "productivity": 4, "cost": 70}
    ]

def run_calc_tests():
    print("="*50)
    print("CALCULATION TESTS")
    print("="*50)
    
    state = GameState()
    state.team = create_test_team()
    state.funding = 100000
    state.morale = 75
    state.popularity = 50
    
    print("\nTEST DATA:")
    print(f"  Team size: {len(state.team)}")
    print(f"  Starting funding: ${state.funding}")
    print(f"  Starting morale: {state.morale}")
    print(f"  Starting popularity: {state.popularity}")
    
    print("\n" + "-"*30)
    print("TEST 1: Restaurant Cost")
    cost = calc_restaurant_cost(state)
    print(f"  Cost for {len(state.team)} people: ${cost}")
    if 6 * len(state.team) <= cost <= 25 * len(state.team):
        print(f"  PASSED (between ${6*len(state.team)} and ${25*len(state.team)})")
    else:
        print(f"  FAILED (should be between ${6*len(state.team)} and ${25*len(state.team)})")
    
    print("\n" + "-"*30)
    print("TEST 2: Fun Activity Cost")
    cost = calc_fun_cost(state)
    print(f"  Cost for {len(state.team)} people: ${cost}")
    if 10 * len(state.team) <= cost <= 50 * len(state.team):
        print(f"  PASSED (between ${10*len(state.team)} and ${50*len(state.team)})")
    else:
        print(f"  FAILED (should be between ${10*len(state.team)} and ${50*len(state.team)})")
    
    print("\n" + "-"*30)
    print("TEST 3: Morale Decrease")
    decrease = calc_morale_decrease()
    print(f"  Morale loss: {decrease}")
    if 1 <= decrease <= 3:
        print(f"  PASSED (between 1 and 3)")
    else:
        print(f"  FAILED (should be between 1 and 3)")
    
    print("\n" + "-"*30)
    print("TEST 4: Popularity Increase")
    results = []
    for _ in range(10):
        results.append(calc_popularity_increase(state))
    avg = sum(results) / len(results)
    min_val = min(results)
    max_val = max(results)
    print(f"  Range: {min_val} to {max_val}")
    print(f"  Average: {avg:.2f}")
    if avg > 0 and max_val > min_val:
        print(f"  PASSED (varies randomly)")
    else:
        print(f"  FAILED (no variation)")
    
    print("\n" + "-"*30)
    print("TEST 5: Morale Increase")
    results = []
    for _ in range(10):
        results.append(calc_morale_increase(state))
    avg = sum(results) / len(results)
    min_val = min(results)
    max_val = max(results)
    print(f"  Range: {min_val} to {max_val}")
    print(f"  Average: {avg:.2f}")
    if avg > 0 and max_val > min_val:
        print(f"  PASSED (varies randomly)")
    else:
        print(f"  FAILED (no variation)")
    
    print("\n" + "-"*30)
    print("TEST 6: Funding Increase")
    results = []
    for _ in range(10):
        results.append(calc_funding_increase(state))
    avg = sum(results) / len(results)
    min_val = min(results)
    max_val = max(results)
    print(f"  Range: ${min_val:.2f} to ${max_val:.2f}")
    print(f"  Average: ${avg:.2f}")
    if avg > 0 and max_val > min_val:
        print(f"  PASSED (varies randomly)")
    else:
        print(f"  FAILED (no variation)")
    
    print("\n" + "-"*30)
    print("TEST 7: Popularity Decay")
    results = []
    for _ in range(10):
        results.append(calc_popularity_decay(state))
    avg = sum(results) / len(results)
    print(f"  Decay values: {results[:5]}...")
    print(f"  Average decay: {avg:.2f}")
    if all(d >= 0 for d in results):
        print(f"  PASSED (all non-negative)")
    else:
        print(f"  FAILED (negative decay found)")
    
    print("\n" + "-"*30)
    print("TEST 8: Fundraising Cost")
    results = []
    for _ in range(10):
        results.append(calc_fundraising_cost(state))
    avg = sum(results) / len(results)
    min_val = min(results)
    max_val = max(results)
    print(f"  Range: ${min_val:.2f} to ${max_val:.2f}")
    print(f"  Average: ${avg:.2f}")
    if all(c >= 0 for c in results):
        print(f"  PASSED (all non-negative)")
    else:
        print(f"  FAILED (negative cost found)")
    
    print("\n" + "-"*30)
    print("TEST 9: Distance Calculation")
    loc1 = {"lat": "37.7749", "lon": "-122.4194"}
    loc2 = {"lat": "37.4419", "lon": "-122.1430"}
    distance = calc_distance(loc1, loc2)
    print(f"  SF to Palo Alto distance: {distance:.4f}")
    if distance > 0:
        print(f"  PASSED (positive distance)")
    else:
        print(f"  FAILED (zero distance)")
    
    print("\n" + "-"*30)
    print("TEST 10: Same Location Distance")
    distance = calc_distance(loc1, loc1)
    print(f"  Same location distance: {distance:.4f}")
    if distance == 0:
        print(f"  PASSED (zero distance)")
    else:
        print(f"  FAILED (should be zero)")

def run_edge_cases():
    print("\n" + "="*50)
    print("EDGE CASE TESTS")
    print("="*50)
    
    print("\nTesting with team of 1:")
    state = GameState()
    state.team = [{"name": "Solo", "moraleImpact": 5, "productivity": 5, "cost": 100}]
    
    cost = calc_restaurant_cost(state)
    print(f"  Restaurant cost for 1 person: ${cost}")
    if 6 <= cost <= 25:
        print(f"  PASSED")
    else:
        print(f"  FAILED")
    
    print("\nTesting with large team (10 people):")
    state.team = [{"name": f"P{i}", "moraleImpact": 5, "productivity": 5, "cost": 100} for i in range(10)]
    
    cost = calc_restaurant_cost(state)
    print(f"  Restaurant cost for 10 people: ${cost}")
    if 60 <= cost <= 250:
        print(f"  PASSED")
    else:
        print(f"  FAILED")
    
    print("\nTesting with zero morale team:")
    state.team = [{"name": "Low", "moraleImpact": 0, "productivity": 0, "cost": 0}]
    
    decay = calc_popularity_decay(state)
    print(f"  Popularity decay: {decay}")
    if decay >= 0:
        print(f"  PASSED")
    else:
        print(f"  FAILED")

def quick_test():
    print("\n" + "="*50)
    print("QUICK SUMMARY")
    print("="*50)
    
    state = GameState()
    state.team = create_test_team()
    
    tests_passed = 0
    tests_total = 6
    
    if 6 * len(state.team) <= calc_restaurant_cost(state) <= 25 * len(state.team):
        tests_passed += 1
    
    if 10 * len(state.team) <= calc_fun_cost(state) <= 50 * len(state.team):
        tests_passed += 1
    
    if 1 <= calc_morale_decrease() <= 3:
        tests_passed += 1
    
    if calc_popularity_increase(state) > 0:
        tests_passed += 1
    
    if calc_morale_increase(state) > 0:
        tests_passed += 1
    
    if calc_funding_increase(state) > 0:
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} basic tests passed")
    
    if tests_passed == tests_total:
        print("\nALL CALCULATIONS WORKING CORRECTLY!")
    else:
        print(f"\n{tests_total - tests_passed} tests failed - check your calc functions")

if __name__ == "__main__":
    random.seed(42)
    run_calc_tests()
    run_edge_cases()
    quick_test()