# All GET Commands for Games API

## Base URL
```
http://localhost:8000
```

---

## 1. Get All Games
```bash
curl http://localhost:8000/api/games
```

**Browser:**
```
http://localhost:8000/api/games
```

**Response:** Returns all 98 games with timestamp and total count

---

## 2. Get New Releases
```bash
curl http://localhost:8000/api/games/new-releases
```

**Browser:**
```
http://localhost:8000/api/games/new-releases
```

**Response:** Returns only games where `new_release: true`

---

## 3. Get Highest Rated Games
```bash
curl http://localhost:8000/api/games/highest-rated
```

**Browser:**
```
http://localhost:8000/api/games/highest-rated
```

**Response:** Returns only games where `highest_rated: true`

---

## 4. Get Games with Discounts
```bash
curl http://localhost:8000/api/games/discounts
```

**Browser:**
```
http://localhost:8000/api/games/discounts
```

**Response:** Returns all games with their discount information

---

## 5. Search for Specific Game by Title
```bash
curl "http://localhost:8000/api/games/search?title=Minecraft"
curl "http://localhost:8000/api/games/search?title=Cyberpunk%202077"
curl "http://localhost:8000/api/games/search?title=Elden%20Ring"
```

**Browser:**
```
http://localhost:8000/api/games/search?title=Minecraft
http://localhost:8000/api/games/search?title=Cyberpunk 2077
http://localhost:8000/api/games/search?title=Elden Ring
```

**Note:** Use `%20` for spaces in curl, or just use spaces in browser

**More Examples:**
```bash
curl "http://localhost:8000/api/games/search?title=The%20Witcher%203"
curl "http://localhost:8000/api/games/search?title=God%20of%20War%20Ragnarök"
curl "http://localhost:8000/api/games/search?title=Baldur's%20Gate%203"
```

---

## 6. Filter Games by Genre
```bash
curl "http://localhost:8000/api/games/genre?genre=RPG"
curl "http://localhost:8000/api/games/genre?genre=FPS"
curl "http://localhost:8000/api/games/genre?genre=Horror"
curl "http://localhost:8000/api/games/genre?genre=Action"
curl "http://localhost:8000/api/games/genre?genre=Simulation"
```

**Browser:**
```
http://localhost:8000/api/games/genre?genre=RPG
http://localhost:8000/api/games/genre?genre=FPS
http://localhost:8000/api/games/genre?genre=Horror
http://localhost:8000/api/games/genre?genre=Action
http://localhost:8000/api/games/genre?genre=Multiplayer
```

**All Available Genres:**
```bash
# Action Games
curl "http://localhost:8000/api/games/genre?genre=Action"

# RPG Games
curl "http://localhost:8000/api/games/genre?genre=RPG"

# FPS Games
curl "http://localhost:8000/api/games/genre?genre=FPS"

# Horror Games
curl "http://localhost:8000/api/games/genre?genre=Horror"

# Survival Games
curl "http://localhost:8000/api/games/genre?genre=Survival"

# Open World Games
curl "http://localhost:8000/api/games/genre?genre=Open%20World"

# Multiplayer Games
curl "http://localhost:8000/api/games/genre?genre=Multiplayer"

# Strategy Games
curl "http://localhost:8000/api/games/genre?genre=Strategy"

# Simulation Games
curl "http://localhost:8000/api/games/genre?genre=Simulation"

# Platformer Games
curl "http://localhost:8000/api/games/genre?genre=Platformer"

# Puzzle Games
curl "http://localhost:8000/api/games/genre?genre=Puzzle"

# Story Games
curl "http://localhost:8000/api/games/genre?genre=Story"

# Stealth Games
curl "http://localhost:8000/api/games/genre?genre=Stealth"

# Fighting Games
curl "http://localhost:8000/api/games/genre?genre=Fighting"

# Racing Games
curl "http://localhost:8000/api/games/genre?genre=Racing"

# Sports Games
curl "http://localhost:8000/api/games/genre?genre=Sports"

# Sandbox Games
curl "http://localhost:8000/api/games/genre?genre=Sandbox"

# Roguelike Games
curl "http://localhost:8000/api/games/genre?genre=Roguelike"

# Turn-Based Strategy Games
curl "http://localhost:8000/api/games/genre?genre=Turn-Based%20Strategy"

# Real-Time Strategy Games
curl "http://localhost:8000/api/games/genre?genre=Real-Time%20Strategy"

# Metroidvania Games
curl "http://localhost:8000/api/games/genre?genre=Metroidvania"

# TPS (Third-Person Shooter) Games
curl "http://localhost:8000/api/games/genre?genre=TPS"

# Tower Defense Games
curl "http://localhost:8000/api/games/genre?genre=Tower%20Defense"

# Card/Deck-Building Games
curl "http://localhost:8000/api/games/genre?genre=Card%20/%20Deck-Building"
```

---

## 7. Health Check
```bash
curl http://localhost:8000/api/health
```

**Browser:**
```
http://localhost:8000/api/health
```

**Response:** Returns server health status with timestamp, uptime, and request ID

---

## Special Management Endpoints

### View Request Logs
```bash
curl http://localhost:8000/__logs
```

**Browser:**
```
http://localhost:8000/__logs
```

**Response:** Returns last 100 request logs

---

## PowerShell Commands (Windows)

```powershell
# Get all games
Invoke-WebRequest -Uri "http://localhost:8000/api/games" | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Get new releases
Invoke-WebRequest -Uri "http://localhost:8000/api/games/new-releases" | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Search for a game
Invoke-WebRequest -Uri "http://localhost:8000/api/games/search?title=Minecraft" | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Filter by genre
Invoke-WebRequest -Uri "http://localhost:8000/api/games/genre?genre=RPG" | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

---

## Python Requests Examples

```python
import requests

# Get all games
response = requests.get("http://localhost:8000/api/games")
games = response.json()

# Get new releases
response = requests.get("http://localhost:8000/api/games/new-releases")
new_games = response.json()

# Search for a game
response = requests.get("http://localhost:8000/api/games/search", params={"title": "Minecraft"})
game = response.json()

# Filter by genre
response = requests.get("http://localhost:8000/api/games/genre", params={"genre": "RPG"})
rpg_games = response.json()
```

---

## JavaScript Fetch Examples

```javascript
// Get all games
fetch('http://localhost:8000/api/games')
  .then(response => response.json())
  .then(data => console.log(data));

// Get new releases
fetch('http://localhost:8000/api/games/new-releases')
  .then(response => response.json())
  .then(data => console.log(data));

// Search for a game
fetch('http://localhost:8000/api/games/search?title=Minecraft')
  .then(response => response.json())
  .then(data => console.log(data));

// Filter by genre
fetch('http://localhost:8000/api/games/genre?genre=RPG')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## Quick Test Commands

```bash
# Test all endpoints quickly
curl http://localhost:8000/api/games | python -m json.tool | head -20
curl http://localhost:8000/api/games/new-releases | python -m json.tool | head -20
curl http://localhost:8000/api/games/highest-rated | python -m json.tool | head -20
curl "http://localhost:8000/api/games/search?title=Minecraft" | python -m json.tool
curl "http://localhost:8000/api/games/genre?genre=Horror" | python -m json.tool | head -30
curl http://localhost:8000/api/health | python -m json.tool
```
