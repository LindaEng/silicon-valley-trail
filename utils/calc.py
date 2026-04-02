import random
import math

def calc_popularity_increase(state):
    avg = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return round((avg * random.uniform(0.1, 1)),2)

def calc_morale_increase(state):
    avg = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return round((avg * random.uniform(0.8, 1.2)),2)

def calc_funding_increase(state):
    prod = sum(m["productivity"] for m in state.team) / len(state.team)
    morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)

    return round((1000 * (prod/10) * (1 + morale/10) * random.uniform(0.9, 1.1)),2)

def calc_restaurant_cost(state):
    return round((random.uniform(6, 25) * len(state.team)),2)

def calc_fun_cost(state):
    return round((random.uniform(10, 50) * len(state.team)),2)

def calc_morale_decrease(state):
    return round(random.uniform(1,5) * len(state.team))

def calc_popularity_decay(state):
    avg_morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    morale_factor = avg_morale / 10
    base_decay = random.uniform(0.05, 0.15)
    decay = base_decay - morale_factor
    return round(max(decay, 0),2)  # never negative decay

def calc_fundraising_cost(state):
    avg_prod = sum(m["productivity"] for m in state.team) / len(state.team)
    avg_cost = sum(m["cost"] for m in state.team) / len(state.team)

    return round(max(
        random.uniform(50, 500) * (1 + avg_cost/100 - avg_prod/100),
        0
    ),2)

def calc_distance(loc1, loc2):
    lat1 = float(loc1["lat"])
    lon1 = float(loc1["lon"])
    lat2 = float(loc2["lat"])
    lon2 = float(loc2["lon"])

    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2

    return (lat_diff**2 + lon_diff**2) ** 0.5
