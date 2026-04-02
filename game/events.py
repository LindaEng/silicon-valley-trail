import random
import time

def random_blessing(state):
    categories = [
        "funding",
        "morale",
        "productivity"
    ]

    random_idx = random.randint(0, len(categories) - 1)
    random_cat = categories[random_idx]
    if random_cat == "funding":
        time.sleep(1)
        rand = random.randint(150,250)
        state.funding += rand
        print(f"Funding blessing: You secured an unexpected grant of ${rand}!")
    elif random_cat == "morale":
        rand = random.randint(5, 20)
        state.morale += rand
        print(f"Morale blessing: The team’s spirits lifted by {rand}% after a surprise celebration!")
    else:
        rand = random.randint(10, 35)
        state.popularity += rand
        print(f"Popularity increased by {rand} thanks to a viral post about our product!")


    



