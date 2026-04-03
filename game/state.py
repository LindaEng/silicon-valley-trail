class GameState:
    def __init__(self, funding=1000, morale=100, popularity = 100, team=None, location=None, day=1, locations_visited=None):
        self.funding = funding
        self.morale = morale 
        self.popularity = popularity
        self.location = location or {"name": "unknown"}
        self.team = team or []
        self.day = day
        self.locations_visited = locations_visited or []
    
    def to_dict(self):
        return {
            "funding": self.funding,
            "morale": self.morale,
            "popularity": self.popularity,
            "team": self.team,
            "location": self.location,
            "day": self.day,
            "locations_visited": self.locations_visited
        }
    
    @staticmethod
    def from_dict(data):
        return GameState(**data)