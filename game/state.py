class GameState:
    def __init__(self, cash=1000, morale=100, team=None, location="start", day=1):
        self.cash = cash
        self.morale = morale
        self.team = team or []
        self.location = location
        self.day = day
    
    def to_dict(self):
        return {
            "cash": self.cash,
            "morale": self.morale,
            "team": self.team,
            "location": self.location
        }
    
    @staticmethod
    def from_dict(data):
        return GameState(**data)