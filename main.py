#!/usr/bin/env python3
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---------------- CORS ----------------
origins = [
    "https://local-mock-api-server-3.onrender.com/",  # replace with your deployed frontend URL
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Test Route ----------------
@app.get("/test")
def test():
    return {"message": "Backend is working!"}

# ---------------- Game Endpoints ----------------
@app.get("/api/games")
def get_games():
    return [
        {"title": "Minecraft", "genre": "Sandbox"},
        {"title": "Valorant", "genre": "FPS"},
        {"title": "The Witcher 3", "genre": "RPG"}
    ]

@app.get("/api/games/new-releases")
def new_releases():
    return [
        {"title": "Cyberpunk 2077", "release_date": "2023-12-01"},
        {"title": "Elden Ring", "release_date": "2023-11-15"}
    ]

@app.get("/api/games/highest-rated")
def highest_rated():
    return [
        {"title": "The Witcher 3", "rating": 9.5},
        {"title": "God of War", "rating": 9.4}
    ]

@app.get("/api/games/discounts")
def discounts():
    return [
        {"title": "Among Us", "discount": "50%"},
        {"title": "Stardew Valley", "discount": "30%"}
    ]

@app.get("/api/games/search")
def search_games(title: str = Query(...)):
    return [{"title": title, "genre": "Demo"}]

@app.get("/api/games/genre")
def get_genre(genre: str = Query(...)):
    return [
        {"title": f"Sample {genre} Game 1", "genre": genre},
        {"title": f"Sample {genre} Game 2", "genre": genre}
    ]

@app.post("/api/games/review")
def post_review(title: str = Query(...), review: str = Query(...)):
    return {"message": f"Review for {title} received!", "review": review}

@app.get("/api/games/wishlist")
def get_wishlist():
    return [{"title": "Minecraft"}, {"title": "Valorant"}]

@app.post("/api/games/wishlist")
def add_wishlist(title: str = Query(...)):
    return {"message": f"{title} added to wishlist!"}

@app.delete("/api/games/wishlist")
def remove_wishlist(title: str = Query(...)):
    return {"message": f"{title} removed from wishlist!"}
