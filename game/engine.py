from game.actions import check_team

class GameEngine:
    def __init__(self, state):
        self.state = state

    def step(self):
        print(f"\nDay: {self.state.day}")
        print(f"\nLocation: {self.state.location}")
        print("\nWhat would you like to do?")
        print("1. Explore area")
        print("2. Check in with team")
        print("3. Next destination")

        choice = input("Choose: ")

        self.handle_choice(choice)
        # self.state.day += 1       

    def handle_choice(self, choice):
        if choice == "1":
            print("STUB IN FOR MAPS")
        elif choice == "2":
            check_team(self.state)
        elif choice == "3":
            print("STUB IN FOR NEXT DESTINATION")

    def run(self):
        print("-------- GAME START ------- \n")
        while True:
            self.step()