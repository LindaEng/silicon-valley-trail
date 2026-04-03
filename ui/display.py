import sys


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

def print_character(member):
    lines = [
        f"Name: {member['name']}",
        f"Productivity: {member['productivity']}",
        f"Cost: {member['cost']}",
        f"Morale: {member['moraleImpact']}",
        f"Motivation: {member['motivation']}",
    ]

    width = max(len(line) for line in lines) + 4

    print("+" + "-" * width + "+")
    for line in lines:
        print(f"|  {line.ljust(width - 4)}  |")
    print("+" + "-" * width + "+")