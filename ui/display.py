import sys
from tabulate import tabulate

def _is_testing():
    return 'pytest' in sys.modules

if not _is_testing():
    class _Colors:
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BOLD = '\033[1m'
        END = '\033[0m'
else:
    class _Colors:
        CYAN = GREEN = YELLOW = BOLD = END = ''

def styled_input(prompt):
    """Like input() but with a nicer prompt style"""
    return input(f"{_Colors.CYAN}➜ {prompt}{_Colors.END} ").strip()

def print_characters_grid(characters, cols=3):
    """Display characters using tabulate for perfect alignment"""

    table_data = []
    for m in characters:
        table_data.append([
            m['name'],
            m['productivity'],
            m['cost'],
            m['moraleImpact'],
            m['motivation']
        ])
    
    headers = ["Name", "Prod", "Cost", "Morale", "Motive"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_travel_summary(state, travel_cost, location):
    """Print travel summary using tabulate"""
    table_data = [
        ["📍 Welcome to:", location['name']],
        ["✈️ Travel cost:", f"${travel_cost:.2f}"],
    ]
    
    print("\n" + tabulate(table_data, tablefmt="grid"))

from tabulate import tabulate

def print_summary(state):
    """Print game summary using tabulate"""
    # Create a formatted string for cities with line breaks
    if state.locations_visited:
        cities_display = "\n".join([f"  • {city}" for city in state.locations_visited])
    else:
        cities_display = "None"
    
    table_data = [
        ["💰 Funding:", f"${state.funding:.2f}"],
        ["😊 Morale:", f"{state.morale:.2f}"],
        ["👥 Team size:", len(state.team)],
        ["⭐ Popularity:", f"{state.popularity:.2f}"],
        ["🏙️ Cities Visited:", cities_display]
    ]
    
    print("\n" + tabulate(table_data, tablefmt="grid"))
