from game.actions import check_team, explore_city, update_to_next_location, attempt_IPO
from ui.display import styled_input, print_summary

class GameEngine:
    def __init__(self, state):
        self.state = state
        self.running = True

    def step(self):
        if self.check_game_over():
            self.running = False
            return "exit"
        
        print("=========== SUMMARY ===========")
        print_summary(self.state)
        print("=========== MENU ===========")
        print("\nWhat would you like to do?")
        print("1. Explore area")
        print("2. Check in with team")
        print("3. Next destination")
        print("4. Save and Quit")
        
        if len(self.state.locations_visited) >= 10:
            print("5. Attempt IPO")
        
        print("==========================")
        choice = styled_input("Choose: ")
        result = self.handle_choice(choice)
        
    
        if result != "exit":
            self.state.day += 1  
        
        return result

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
        elif choice == "5" and len(self.state.locations_visited) >= 10:
            result = attempt_IPO(self.state)
            if result:
                print("YOU WON! Thank you for playing")
                return "exit"
            else:
                return "menu"
        else:
            print("invalid choice")   
            return "menu"
        
        
    def check_game_over(self):
        if self.state.funding <= 0:
            print("You ran out of money... Game over")
            return True
        if len(self.state.team) == 0:
            print("Everyone decided to quit... Game over")
            return True
        return False

    def run(self):
        print("-------- GAME START ------- \n")
        while self.running:
            result = self.step()
            if result == "exit":
                print("Exiting game...")
                break
        return "exit"