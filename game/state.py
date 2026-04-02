class GameState:
    def __init__(self, funding=1000, morale=100, productivity = 100, team=None, location=None, day=1):
        self.funding = funding
        self.morale = morale
        self.productivity = productivity
        self.location = location or {"name": "unknown"}
        self.team = team or []
        self.day = day
    
    def to_dict(self):
        return {
            "funding": self.funding,
            "morale": self.morale,
            "productivity": self.productivity,
            "team": self.team,
            "location": self.location,
            "day": self.day
        }
    
    @staticmethod
    def from_dict(data):
        return GameState(**data)