from game.actions import check_team, explore_city, update_to_next_location

class GameEngine:
    def __init__(self, state):
        self.state = state

    def step(self):
        self.print_summary()
        print("\nWhat would you like to do?")
        print("1. Explore area")
        print("2. Check in with team")
        print("3. Next destination")
        print("4. Save and Quit")

        choice = input("Choose: ")

        result = self.handle_choice(choice)
        if result == "menu":
            return
        if result == "exit":
            return "exit"
        # self.state.day += 1       

    def handle_choice(self, choice):
        if choice == "1":
            explore_city(self.state.location, self.state)
        elif choice == "2":
            check_team(self.state)
            return "menu"
        elif choice == "3":
            update_to_next_location(self.state)
        elif choice == "4":
            return "exit"
        
    def print_summary(self):
        print(f"Day: {self.state.day}\n")
        print(f"Current Location: {self.state.location["name"]}\n")
        print(f"Funding: {self.state.funding:.2f}\n")
        print(f"Morale: {self.state.morale}\n")
        print(f"Popularity: {self.state.popularity}\n")
        

    def back_to_menu():
        return "menu"

    def run(self):
        print("-------- GAME START ------- \n")
        while True:
            result = self.step()
            if result == "exit":
                print("Exiting game...")
                return "exit"



            