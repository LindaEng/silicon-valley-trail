# Silicon Valley Trail

An interactive text-based startup road trip game where you build a team, travel between cities, manage morale and funding, and try to take your company public before everything falls apart.

## Game Overview

You play as the leader of a startup chasing an IPO. Each turn, you decide whether to explore your current city, check in with the team, travel somewhere new, save your run, or attempt an IPO once you have built enough momentum.

### Core Mechanics

- Turn-based progression with daily decisions
- Dynamic resource simulation where funding, morale, and popularity shift based on team makeup and team health
- Team drafting with randomized startup characters
- City exploration powered by live map lookups and local fallbacks
- Dynamic AI-generated flavor text with offline-safe fallback responses
- Local save and continue support using SQLite
- IPO win condition unlocked after visiting at least 10 cities

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository.

```bash
git clone https://github.com/yourusername/silicon-valley-trail.git
cd silicon-valley-trail
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Optional: enable AI flavor text by creating a local environment file.

```bash
cp .env.example .env
```

Then add your Hugging Face token to `.env`:

```env
HF_TOKEN=hf_your_token_here
```

## Running The Game

```bash
python main.py
```

When the game starts, you can begin a new run or continue from a saved slot.

## Running Tests

```bash
pytest tests/ -v
```

## How To Play

### Main Menu

- `1. Explore area` - Find restaurants, fundraising venues, or morale boosts in the current city
- `2. Check in with team` - Review your current team and generate character flavor dialogue
- `3. Next destination` - Travel to a new city and pay distance-based travel costs
- `4. Save and Quit` - Store your current run in the local SQLite database
- `5. Attempt IPO` - Try to win once you have visited at least 10 cities

### Key Resources

- Funding: Changes with team decisions and team performance across actions like travel, fundraising, and recovery.
- Morale: Reflects current team health and directly responds to who is on your team and how hard you push them.
- Popularity: Moves up or down with execution quality, which is influenced by team composition and current condition.
- Team motivation: Individual members can burn out and leave, which reshapes your team and dynamically changes all resource outcomes.

In short, resources are not static bars. They are emergent outputs of who your team is, how healthy they are, and what choices you make each day.

### Winning And Losing

Win by successfully completing an IPO after building enough strength across multiple cities.

Lose if either of these happens:

- Your funding drops to zero or below
- Every team member leaves

## API Integration

### Hugging Face Inference API

If `HF_TOKEN` is set, the game uses Hugging Face chat completions to generate:

- Location intros
- City fun facts
- Team check-in dialogue
- Action flavor text
- IPO success and failure narration

If no token is configured, the game falls back to built-in text so it remains fully playable.

### Map And Location Services

The game also uses public OpenStreetMap services to make travel and city exploration feel grounded:

- Nominatim for location lookup
- Overpass for nearby places such as restaurants and venues

When these services are slow or unavailable, the game falls back to generated local recommendations.

## Architecture Overview

```text
silicon-valley-trail/
├── main.py                # Entry point, save/load flow, dotenv bootstrap
├── assets/
│   └── ascii/
│       └── splash.txt     # Startup splash screen
├── data/
│   └── characters.json    # Team member definitions
├── db/
│   ├── database.py        # SQLite connection and schema setup
│   └── saves.py           # Save/load/list game state
├── game/
│   ├── actions.py         # Explore, travel, team, and IPO actions
│   ├── engine.py          # Main loop and menu handling
│   ├── events.py          # Random blessings and curses
│   └── state.py           # GameState model
├── services/
│   ├── ai_service.py      # Hugging Face integration and fallback lore
│   └── map_service.py     # Geocoding and nearby place lookup
├── ui/
│   └── display.py         # Console formatting and tables
├── utils/
│   ├── cache.py           # Nearby-search category mappings
│   ├── calc.py            # Funding, morale, popularity, and distance calculations
│   └── loader.py          # JSON loading helpers
├── tests/                 # Unit and integration tests
├── requirements.txt       # Python dependencies
└── .env.example           # Optional Hugging Face token template
```

### Data Flow

1. `main.py` initializes the database and starts a new or saved run.
2. `GameEngine` presents the menu and routes player choices.
3. `game/actions.py` updates `GameState` based on exploration, travel, and IPO decisions.
4. `services/map_service.py` fetches real locations and nearby venues.
5. `services/ai_service.py` adds optional narrative flavor with fallback text.
6. `db/saves.py` persists runs to SQLite when the player exits.

## Design Decisions And Tradeoffs

### Why Hugging Face

- Low/No-cost optional text generation
- Straightforward token-based API
- Easy to disable without breaking gameplay

### Why Public Map APIs

- Real locations make travel choices feel more concrete
- Nearby venue lookup creates variety without hardcoding every city
- Fallback responses keep the game usable when requests fail

### Save System

- SQLite is simple to ship with a CLI game
- Save slots require no extra services or setup
- Stored state is easy to inspect and test

### Save/Load As A Startup Time Machine

Every time you choose `Save and Quit`, the game writes a full JSON snapshot of your company state into SQLite and assigns it a new slot ID. That means your saves are not just checkpoints, they become a timeline of your startup story.

- Keep multiple branches of the same run (safe play vs risky play)
- Revisit older slots to compare how team choices changed morale and funding
- Treat slots like milestones on the road to IPO (Day 3 pivot, Day 7 hiring spree, Day 12 moonshot)

When you choose Continue, the game lists your available slots with city and day so you can jump back into any chapter of your journey.

### Tradeoffs

- Text-first design keeps the project small and testable
- External APIs make the game more dynamic, but add network variability
- Character and event systems are simple enough to extend without changing the core loop

## Testing

The test suite covers core game behavior including:

- Action calculations
- Character and team flow
- Engine behavior
- Event outcomes
- Save/load persistence
- Integration paths around travel and IPO attempts

Run all tests with:

```bash
pytest tests/ -v
```

## Example Session

```text
---New Game---

You are setting out on a journey through Silicon Valley...
Build your team. Navigate the chaos. Ship or die.

But first -- where would you like to start?

Enter location: San Francisco
You chose: San Francisco

Before we start lets choose a dream team!
Choose your team (at least 5, comma separated indices):
...

=========== SUMMARY ===========
Day: 1
Funding: $1000.00
Morale: 100.00
Popularity: 100.00
=========== MENU ===========
1. Explore area
2. Check in with team
3. Next destination
4. Save and Quit
```

## Troubleshooting

### Game crashes on startup

- Make sure your virtual environment is activated
- Reinstall dependencies with `pip install -r requirements.txt`
- Check that `data/characters.json` exists

### Hugging Face text is not showing up

- Verify `HF_TOKEN` is set in `.env`
- Restart the game after editing environment variables
- The game will still run using fallback text if the token is missing or invalid

### Nearby places are not loading

- Public map APIs can be slow or rate-limited
- The game should fall back to generated recommendations automatically

## Dependencies

- `requests` for HTTP calls to external APIs
- `python-dotenv` for loading `.env` during local development
- `tabulate` for console table formatting
- `pytest` for tests

See `requirements.txt` for the installable set.

## AI Usage

AI support was used in two focused ways during development:

- Test generation: Used AI assistance to draft and expand unit/integration test cases, especially for gameplay flows and edge cases.
- Hugging Face feature: Used AI assistance to help design and implement the optional Hugging Face-powered narrative layer (fun facts, intros, team dialogue, and IPO lore) with graceful fallback behavior.

The core game design, mechanics, and project structure decisions were still guided and finalized manually.

## Credits

Built as a CLI game project demonstrating:

- Game loop design
- State management
- External API integration with graceful fallbacks
- Save/load persistence
- Automated test coverage
