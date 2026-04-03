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
    """Print game summary"""
    
    print("\n" + "="*50)
    print("📊 GAME SUMMARY")
    print("="*50)
    print(f"💰 Funding:    ${state.funding:,.2f}")
    print(f"😊 Morale:     {state.morale:.1f}%")
    print(f"👥 Team size:  {len(state.team)}")
    print(f"⭐ Popularity: {state.popularity:.1f}%")
    print("-"*50)
    print("🏙️  Cities Visited:")
    
    if state.locations_visited:
        for city in state.locations_visited:
            print(f"   • {city}")
    else:
        print("   • None")
    print("="*50 + "\n")
