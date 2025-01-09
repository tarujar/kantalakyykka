from fastapi import FastAPI
from app.api import games, players

def create_app() -> FastAPI:
    app = FastAPI(title="Kyykka API")
    app.include_router(games.router, prefix="/api/v1")
    app.include_router(players.router, prefix="/api/v1")
    return app

app = create_app() 