from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, Text, TIMESTAMP, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
import enum
from datetime import datetime, timezone

Base = declarative_base()

# Create a simple Table for the many-to-many relationship instead of a model
roster_players_in_series = Table(
    'roster_players_in_series',
    Base.metadata,
    Column('registration_id', Integer, ForeignKey('teams_in_series.id'), primary_key=True),
    Column('player_id', Integer, ForeignKey('players.id'), primary_key=True)
)

class ThrowResult(enum.Enum):
    VALID = "valid"
    HAUKI = "hauki"
    FAULT = "fault"

class GameType(Base):
    __tablename__ = "game_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    max_players = Column(Integer, nullable=False)

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    email = Column(String, unique=True, nullable=False)

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    season_type = Column(String, nullable=False, default="winter")
    year = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="upcoming")
    registration_open = Column(Boolean, default=True)
    game_type_id = Column(Integer, ForeignKey("game_types.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

class TeamInSeries(Base):
    __tablename__ = "teams_in_series"
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    team_name = Column(String, nullable=False)
    team_abbreviation = Column(String, nullable=False)
    contact_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

class TeamHistory(Base):
    __tablename__ = "team_history"
    id = Column(Integer, primary_key=True, index=True)
    previous_registration_id = Column(Integer, ForeignKey("teams_in_series.id"))
    next_registration_id = Column(Integer, ForeignKey("teams_in_series.id"))
    relation_type = Column(String, nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    round = Column(String)
    is_playoff = Column(Boolean, default=False)
    series_id = Column(Integer, ForeignKey("series.id"))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    game_date = Column(Date, nullable=False)
    team_1_id = Column(Integer, ForeignKey("teams_in_series.id"), nullable=False)
    team_2_id = Column(Integer, ForeignKey("teams_in_series.id"), nullable=False)
    score_1_1 = Column(Integer, nullable=False)
    score_1_2 = Column(Integer, nullable=False)
    score_2_1 = Column(Integer, nullable=False)
    score_2_2 = Column(Integer, nullable=False)

class SingleThrow(Base):
    __tablename__ = "single_throw"
    id = Column(Integer, primary_key=True, index=True)
    throw_type = Column(Enum(ThrowResult), nullable=False)
    throw_score = Column(Integer, nullable=False)

class SingleRoundThrow(Base):
    __tablename__ = "single_round_throws"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game_set_index = Column(Integer, nullable=False)
    throw_position = Column(Integer, nullable=False)
    home_team = Column(Boolean, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    throw_1 = Column(Integer, ForeignKey("single_throw.id"))
    throw_2 = Column(Integer, ForeignKey("single_throw.id"))
    throw_3 = Column(Integer, ForeignKey("single_throw.id"))
    throw_4 = Column(Integer, ForeignKey("single_throw.id"))
