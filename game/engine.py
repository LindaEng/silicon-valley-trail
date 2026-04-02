from game.actions import check_team, explore_city, update_to_next_location, attempt_IPO

class GameEngine:
    def __init__(self, state):
        self.state = state

    def step(self):
        if self.check_game_over() == True:
            return "exit"
        self.print_summary()
        print("\nWhat would you like to do?")
        print("1. Explore area")
        print("2. Check in with team")
        print("3. Next destination")
        print("4. Save and Quit")
        # Only show if we went to more than 5 locations
        if len(self.state.locations_visited) > 5:
            print("5. Attempt IPO")
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
        elif choice == "5" and len(self.state.locations_visited) > 5:
            result = attempt_IPO(self.state)
            if result == True:
                print("YOU WON! Thank you for playing")
                return "exit"
            else:
                return "menu"
        else:
            print("invalid choice")   
            return "menu"
        
    def print_summary(self):
        print(f"Day: {self.state.day}\n")
        print(f"Current Location: {self.state.location["name"]}\n")
        print(f"Funding: {self.state.funding:.2f}\n")
        print(f"Morale: {self.state.morale}\n")
        print(f"Popularity: {self.state.popularity}\n")
        print("========================================")
        print("Cities that you have visited so far: ")
        for i, loc in enumerate(self.state.locations_visited):
            print(f"{i}: {loc}")
        

    def check_game_over(self):
        if self.state.funding <= 0:
            print("You ran out of money... Game over")
            return True
        if len(self.state.team) == 0:
            print("Everyone decided to quit... Game over")
            return True
        return False

    def back_to_menu():
        return "menu"

    def run(self):
        print("-------- GAME START ------- \n")
        while True:
            result = self.step()
            if result == "exit":
                print("Exiting game...")
                return "exit"



            