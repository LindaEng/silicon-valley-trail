class GameEngine:
    def __init__(self, state):
        self.state = state

    def step(self):
        print(f"Day {self.state.day}")
        self.state.day += 1

    def run(self):
        while self.state.day <= 5:
            self.step()