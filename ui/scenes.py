def show_splash():
    with open("assets/ascii/splash.txt") as f:
        print(f.read())

def show_intro_scene():
    print("welcome to the game")
def show_win_scene():
    print("You win!")

def show_lose_scene():
    print("your entire party died")