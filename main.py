#!/usr/bin/env python3
"""
Main entry point for Local API Mock Server
"""

import sys
import os
import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# IMPORTANT: Replace with your actual frontend Render URL
origins = [
"https://local-mock-api-server-3.onrender.com"  ,
"http://localhost:3000",   # optional for local testing
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"message": "Backend is working!"}

# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---------------- CORS Setup ----------------
origins = [
    "https://your-frontend-on-render.com",  # replace with your actual frontend URL
    "http://localhost:3000"                 # optional for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Health Check ----------------
@app.get("/api/health")
def health():
    return {"status": "ok"}

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
def search_games(title: str = Query(..., description="Game title to search")):
    # For demo, return the search term as a match
    return [{"title": title, "genre": "Demo"}]

@app.get("/api/games/genre")
def get_genre(genre: str = Query(..., description="Genre to filter")):
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
# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

# Import after path is set
from mock_server import MockServerConfig, MockRequestHandler, RequestLogger, WishlistManager
from http.server import HTTPServer

def main():
    """Main entry point with default config path."""
    parser = argparse.ArgumentParser(description='Local API Mock Server')
    parser.add_argument('--config', default='config/config.json', help='Configuration file path')
    parser.add_argument('--port', type=int, help='Server port (overrides config)')
    args = parser.parse_args()
    
    # Initialize configuration, logger, and wishlist manager
    config = MockServerConfig(args.config)
    logger = RequestLogger()
    wishlist_manager = WishlistManager()
    
    # Set class variables
    MockRequestHandler.config = config
    MockRequestHandler.logger = logger
    MockRequestHandler.wishlist_manager = wishlist_manager
    
    # Determine port
    port = args.port or config.get('port', 8000)
    
    # Start server
    server = HTTPServer(('', port), MockRequestHandler)
    print(f"Mock Server running on http://localhost:{port}")
    print(f"Config: {args.config}")
    print(f"Reload: POST http://localhost:{port}/__reload")
    print(f"Logs: GET http://localhost:{port}/__logs")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹ Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    main()
