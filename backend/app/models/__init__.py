from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import (
    GameType,
    Player,
    User,
    Series,
    SeriesRegistration,  # Changed from SeriesRegistration
    TeamHistory,
    Game,
    SingleThrow,
    SingleRoundThrow,
    RosterPlayersInSeries
)

from .schemas import (
    GameTypeCreate,
    GameType as GameTypeSchema,
    PlayerBase,
    PlayerCreate,
    Player as PlayerSchema,
    SeriesCreate,
    Series as SeriesSchema,
    SeriesRegistrationBase,  
    SeriesRegistrationCreate,  
    SeriesRegistration as SeriesRegistrationSchema,
    SeriesParticipant, 
    TeamHistoryCreate,
    TeamHistory as TeamHistorySchema,
    SingleThrowCreate,
    SingleThrow as SingleThrowSchema,
    SingleRoundThrowCreate,
    SingleRoundThrow as SingleRoundThrowSchema,
    GameCreate,
    Game as GameSchema,
    UserBase,
    UserCreate,
    User as UserSchema
)
