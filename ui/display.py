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