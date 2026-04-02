import random

def calc_productivity_increase(state):
    avg = sum(m["productivity"] for m in state.team) / len(state.team)
    return avg * random.uniform(0.1, 1)

def calc_morale_increase(state):
    avg = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    return avg * random.uniform(0.8, 1.2)

def calc_funding_increase(state):
    prod = sum(m["productivity"] for m in state.team) / len(state.team)
    morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)

    return 1000 * (prod/10) * (1 + morale/10) * random.uniform(0.9, 1.1)

def calc_restaurant_cost(state):
    return random.uniform(6, 25) * len(state.team)

def calc_fundraising_cost(state):
    avg_prod = sum(m["productivity"] for m in state.team) / len(state.team)
    avg_cost = sum(m["cost"] for m in state.team) / len(state.team)

    return max(
        random.uniform(50, 500) * (1 + avg_cost/100 - avg_prod/100),
        0
    )

def calc_productivity_decay(state):
    morale = sum(m["moraleImpact"] for m in state.team) / len(state.team)
    