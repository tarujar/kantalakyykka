from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Optional

class ThrowResult(str, Enum):
    VALID = "valid"
    HAUKI = "hauki"
    FAULT = "fault"

class GameTypeCreate(BaseModel):
    name: str
    max_players: int

class GameType(BaseModel):
    id: int
    name: str
    max_players: int
    created_at: Optional[str]

    class Config:
        orm_mode: True

class PlayerCreate(BaseModel):
    name: str
    email: EmailStr

class Player(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: Optional[str]

    class Config:
        orm_mode: True

class SeriesCreate(BaseModel):
    name: str
    season_type: str
    year: int
    status: Optional[str] = "upcoming"
    registration_open: Optional[bool] = True
    game_type_id: int

class Series(BaseModel):
    id: int
    name: str
    season_type: str
    year: int
    status: Optional[str]
    registration_open: Optional[bool]
    game_type_id: int
    created_at: Optional[str]

    class Config:
        orm_mode: True

class TeamInSeries(BaseModel):
    series_id: int
    team_name: str
    team_abbreviation: str
    contact_player_id: int

class RosterPlayer(BaseModel):
    registration_id: int
    player_id: int

class GameCreate(BaseModel):
    game_type_id: int
    game_date: str
    team_1_id: int
    team_2_id: int
    score_1_1: int
    score_1_2: int
    score_2_1: int
    score_2_2: int

class Game(BaseModel):
    id: int
    game_type_id: int
    game_date: str
    team_1_id: int
    team_2_id: int
    score_1_1: int
    score_1_2: int
    score_2_1: int
    score_2_2: int
    created_at: Optional[str]

    class Config:
        orm_mode: True

class GameResult(BaseModel):
    game_id: int
    sets: List[dict]  # Define the structure of sets as needed