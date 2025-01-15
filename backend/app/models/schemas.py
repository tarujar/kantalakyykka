from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from enum import Enum
from typing import List, Optional, Literal
from datetime import date, datetime

class ThrowResult(str, Enum):
    VALID = "valid"
    HAUKI = "hauki"
    FAULT = "fault"

class GameTypeCreate(BaseModel):
    name: str
    max_players: int

class GameType(BaseModel):
    id: Optional[int]
    name: str
    max_players: int

    class Config:
        orm_mode = True

class PlayerBase(BaseModel):
    name: str
    email: EmailStr

class PlayerCreate(PlayerBase):
    pass

class Player(BaseModel):
    id: Optional[int]
    name: str
    position: int

    class Config:
        orm_mode = True

class SeriesCreate(BaseModel):
    name: str
    season_type: Literal['summer', 'winter']
    year: int
    status: Optional[Literal['upcoming', 'ongoing', 'completed']] = "upcoming"
    registration_open: Optional[bool] = True
    game_type_id: int

    @model_validator(mode='after')
    def validate_unique_name_year(self):
        # Note: Actual DB-level uniqueness check needed in service layer
        return self

class Series(BaseModel):
    id: Optional[int]
    name: str
    max_players: int

    class Config:
        orm_mode = True

class TeamInSeriesCreate(BaseModel):
    series_id: int
    team_name: str
    team_abbreviation: str
    contact_player_id: int

    @model_validator(mode='after')
    def validate_unique_in_series(self):
        # Note: Actual DB-level uniqueness check needed in service layer
        return self

class Team(BaseModel):
    id: Optional[int]
    name: str

    class Config:
        orm_mode = True

class TeamInSeries(TeamInSeriesCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TeamHistoryCreate(BaseModel):
    previous_registration_id: int
    next_registration_id: int
    relation_type: str
    notes: Optional[str]

class TeamHistory(TeamHistoryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SingleThrowCreate(BaseModel):
    throw_type: ThrowResult
    throw_score: int

    @field_validator('throw_score')
    def validate_throw_score(cls, v, values):
        throw_type = values.data.get('throw_type')
        if throw_type == ThrowResult.VALID and not -80 <= v <= 80:
            raise ValueError("Valid throw score must be between -80 and 80")
        elif throw_type != ThrowResult.VALID and v != 0:
            raise ValueError("Non-valid throws must have score 0")
        return v

class SingleThrow(SingleThrowCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SingleRoundThrowsCreate(BaseModel):
    game_id: int
    game_set_index: int = Field(ge=1, le=2)
    throw_position: int = Field(ge=1, le=5)
    home_team: bool
    player_id: int
    throw_1: int
    throw_2: int
    throw_3: int
    throw_4: int

class SingleRoundThrows(SingleRoundThrowsCreate):
    id: int

    @model_validator(mode='after')
    def validate_unique_game_set_position(self):
        # Note: Actual DB-level uniqueness check needed in service layer
        return self

    model_config = ConfigDict(from_attributes=True)

class GameCreate(BaseModel):
    round: Optional[str]
    is_playoff: Optional[bool] = False
    series_id: int
    game_date: date
    team_1_id: int
    team_2_id: int
    score_1_1: int
    score_1_2: int
    score_2_1: int
    score_2_2: int

    @model_validator(mode='after')
    def validate_different_teams(self):
        if self.team_1_id == self.team_2_id:
            raise ValueError("team_1_id and team_2_id must be different")
        return self

class Game(BaseModel):
    id: Optional[int]
    type_id: int
    series_id: int
    starting_team_id: int

    class Config:
        orm_mode = True