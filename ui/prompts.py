from ui.display import styled_input
def show_menu():
    print("1. New Game")
    print("2. Continue")
    choice = styled_input("Choose an option: ")
    return choice


    