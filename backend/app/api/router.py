from fastapi import APIRouter
from app.api.v1 import series, game_types

api_router = APIRouter()
api_router.include_router(series.router, prefix="/series", tags=["series"])
api_router.include_router(game_types.router, prefix="/game_types", tags=["game_types"])
# Add other routers here as needed
