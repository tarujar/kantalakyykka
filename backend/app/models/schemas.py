from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from enum import Enum
from typing import Optional, Literal
from datetime import date, datetime

class ThrowInput(str, Enum):
    VALID = "valid"
    HAUKI = "hauki"
    FAULT = "fault"

class GameTypeCreate(BaseModel):
    name: str
    team_player_amount: int
    team_throws_in_set: int
    game_player_amount: int
    kyykka_amount: int

class GameType(BaseModel):
    id: Optional[int]
    name: str
    team_player_amount: int
    team_throws_in_set: int
    game_player_amount: int
    kyykka_amount: int

    model_config = ConfigDict(from_attributes=True)

class PlayerBase(BaseModel):
    name: str
    email: EmailStr

class PlayerCreate(PlayerBase):
    pass

class Player(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SeriesCreate(BaseModel):
    name: str
    season_type: Literal['summer', 'winter']
    year: int
    status: Optional[Literal['upcoming', 'ongoing', 'completed']] = "upcoming"
    game_type_id: int
    registration_open: Optional[bool] = True
    is_cup_league: Optional[bool] = False

    @model_validator(mode='after')
    def validate_unique_name_year(self):
        # Note: Actual DB-level uniqueness check needed in service layer
        return self

class Series(BaseModel):
    id: Optional[int]
    name: str
    season_type: str
    year: int
    status: str
    game_type_id: int
    registration_open: bool
    is_cup_league: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SeriesRegistrationBase(BaseModel):
    series_id: int
    lohko: Optional[str] = None
    team_name: Optional[str] = None
    team_abbreviation: Optional[str] = None
    contact_player_id: int

class SeriesRegistrationCreate(SeriesRegistrationBase):
    pass

class SeriesRegistration(SeriesRegistrationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SeriesParticipant(BaseModel):
    registration_id: int
    series_id: int
    participant_name: str
    participant_abbreviation: str
    participant_type: Literal['TEAM', 'PLAYER']
    group_name: Optional[str]
    contact_id: int

    model_config = ConfigDict(from_attributes=True)

class Team(BaseModel):
    id: Optional[int]
    name: str

    model_config = ConfigDict(from_attributes=True)

class TeamHistoryCreate(BaseModel):
    previous_registration_id: int
    next_registration_id: int
    relation_type: str
    notes: Optional[str]

class TeamHistory(BaseModel):
    id: int
    previous_registration_id: int
    next_registration_id: int
    relation_type: str
    notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SingleThrowCreate(BaseModel):
    throw_type: ThrowInput
    throw_score: int

    @field_validator('throw_score')
    def validate_throw_score(cls, v, values):

        throw_type = values.get('throw_type')
        if (throw_type == ThrowInput.VALID and not -80 <= v <= 80):
            raise ValueError("Valid throw score must be between -80 and 80")
        elif (throw_type != ThrowInput.VALID and v != 0):
            raise ValueError("Non-valid throws must have score 0")
        return v

class SingleThrow(BaseModel):
    id: int
    throw_type: ThrowInput
    throw_score: int

    model_config = ConfigDict(from_attributes=True)

class SingleRoundThrowCreate(BaseModel):
    game_id: int
    game_set_index: int = Field(ge=1, le=2)
    throw_position: int = Field(ge=1, le=5)
    home_team: bool
    player_id: int
    throw_1: int
    throw_2: int
    throw_3: int
    throw_4: int

class SingleRoundThrow(BaseModel):
    id: int
    game_id: int
    game_set_index: int
    throw_position: int
    home_team: bool
    player_id: int
    throw_1: int
    throw_2: int
    throw_3: int
    throw_4: int

    model_config = ConfigDict(from_attributes=True)

class GameCreate(BaseModel):
    round: Optional[str]
    is_playoff: Optional[bool] = False
    series_id: int
    game_date: date
    team_1_id: int  # Now references series_registrations.id
    team_2_id: int  # Now references series_registrations.id
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
    round: Optional[str]
    is_playoff: Optional[bool]
    game_date: date
    team_1: SeriesRegistration
    team_2: SeriesRegistration
    score_1_1: int
    score_1_2: int
    score_2_1: int
    score_2_2: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    hashed_password: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)