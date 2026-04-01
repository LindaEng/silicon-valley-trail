from game.actions import check_team, explore_city

class GameEngine:
    def __init__(self, state):
        self.state = state

    def step(self):
        print(f"\nDay: {self.state.day}")
        print(f"\nLocation: {self.state.location["name"]}")
        print("\nWhat would you like to do?")
        print("1. Explore area")
        print("2. Check in with team")
        print("3. Next destination")

        choice = input("Choose: ")

        result = self.handle_choice(choice)
        if result == "menu":
            return
        # self.state.day += 1       

    def handle_choice(self, choice):
        if choice == "1":
            explore_city(self.state.location)
        elif choice == "2":
            check_team(self.state)
            return "menu"
        elif choice == "3":
            print("STUB IN FOR NEXT DESTINATION")
            return "menu"
        

    def run(self):
        print("-------- GAME START ------- \n")
        while True:
            self.step()


            