# Games API Endpoints

## Available Endpoints

### 1. Get All Games
```
GET /api/games
```
Returns all games in the database.

**Example:**
```bash
curl http://localhost:8000/api/games
```

---

### 2. Get New Releases
```
GET /api/games/new-releases
```
Returns only games marked as new releases.

**Example:**
```bash
curl http://localhost:8000/api/games/new-releases
```

---

### 3. Get Highest Rated Games
```
GET /api/games/highest-rated
```
Returns only games marked as highest rated.

**Example:**
```bash
curl http://localhost:8000/api/games/highest-rated
```

---

### 4. Get Games with Discounts
```
GET /api/games/discounts
```
Returns all games with their discount information.

**Example:**
```bash
curl http://localhost:8000/api/games/discounts
```

---

### 5. Search for a Specific Game
```
GET /api/games/search?title=<game_title>
```
Returns a specific game by its exact title.

**Parameters:**
- `title` (required): The exact title of the game

**Example:**
```bash
curl "http://localhost:8000/api/games/search?title=Minecraft"
curl "http://localhost:8000/api/games/search?title=Cyberpunk%202077"
```

**Response:**
```json
{
  "game": {
    "title": "Minecraft",
    "discounts_and_events": "50%",
    "new_release": false,
    "highest_rated": true,
    "genres": ["Sandbox", "Survival", "Open World"],
    "sales_leaderboard": 1
  },
  "timestamp": "2025-11-22T15:29:26.610126+00:00"
}
```

---

### 6. Filter Games by Genre
```
GET /api/games/genre?genre=<genre_name>
```
Returns all games that include the specified genre.

**Parameters:**
- `genre` (required): The genre to filter by (e.g., RPG, FPS, Action, Horror, etc.)

**Example:**
```bash
curl "http://localhost:8000/api/games/genre?genre=RPG"
curl "http://localhost:8000/api/games/genre?genre=Horror"
curl "http://localhost:8000/api/games/genre?genre=FPS"
```

**Available Genres:**
- Action
- RPG
- FPS
- Horror
- Survival
- Open World
- Multiplayer
- Strategy
- Simulation
- Platformer
- Puzzle
- Story
- Stealth
- Fighting
- Racing
- Sports
- Sandbox
- Roguelike
- Turn-Based Strategy
- Real-Time Strategy
- Metroidvania
- TPS (Third-Person Shooter)
- And more...

---

### 7. Health Check
```
GET /api/health
```
Returns server health status.

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

## Special Endpoints

### Reload Configuration
```
POST /__reload
```
Reloads the server configuration without restarting.

**Example:**
```bash
curl -X POST http://localhost:8000/__reload
```

---

### View Request Logs
```
GET /__logs
```
Returns the last 100 request logs.

**Example:**
```bash
curl http://localhost:8000/__logs
```

---

## Notes

- All responses include a `timestamp` field with the current UTC time
- URL encode special characters in query parameters (e.g., spaces as `%20`)
- The server supports CORS by default
- Latency and failure simulation can be configured per endpoint in `config.json`
