from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, backref
import enum
from datetime import datetime, timezone

Base = declarative_base()

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
    series = relationship("Series", back_populates="game_type")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    gdpr_consent = Column(Boolean, default=False, nullable=False)  # Add this line
    teams = relationship(
        'TeamInSeries',
        secondary='roster_players_in_series',
        back_populates='players',
        overlaps="team_rosters,roster_entries"
    )

    def __repr__(self):
        return f'<Player {self.name}>'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    season_type = Column(String, nullable=False, default="winter")
    year = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="upcoming")
    game_type_id = Column(Integer, ForeignKey("game_types.id"), nullable=False)
    game_type = relationship("GameType", back_populates="series")
    registration_open = Column(Boolean, default=True)
    is_cup_league = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    teams = relationship("TeamInSeries", back_populates="series")

class TeamInSeries(Base):
    __tablename__ = "teams_in_series"
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    team_name = Column(String, nullable=False)
    team_abbreviation = Column(String, nullable=False)
    contact_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    group = Column(String)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    players = relationship(
        'Player',
        secondary='roster_players_in_series',
        back_populates='teams',
        overlaps="team_rosters,roster_entries"
    )
    series = relationship("Series", back_populates="teams")

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
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    round = Column(String)
    is_playoff = Column(Boolean, default=False)
    game_date = Column(Date, nullable=False)
    team_1_id = Column(Integer, ForeignKey("teams_in_series.id"), nullable=False)
    team_2_id = Column(Integer, ForeignKey("teams_in_series.id"), nullable=False)
    score_1_1 = Column(Integer, nullable=False)
    score_1_2 = Column(Integer, nullable=False)
    score_2_1 = Column(Integer, nullable=False)
    score_2_2 = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    __table_args__ = (
        UniqueConstraint('series_id', 'game_date', 'team_1_id', 'team_2_id', 'round'),
    )

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

class RosterPlayersInSeries(Base):
    __tablename__ = 'roster_players_in_series'
    
    registration_id = Column(Integer, ForeignKey('teams_in_series.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    
    team = relationship(
        'TeamInSeries',
        back_populates='roster_entries',
        overlaps="players,teams",
        foreign_keys=[registration_id]
    )
    player = relationship(
        'Player',
        back_populates='team_rosters',
        overlaps="players,teams",
        foreign_keys=[player_id]
    )
    
    def __str__(self):
        return f"{self.team.team_name} - {self.player.name}"

# Add relationship properties to TeamInSeries
TeamInSeries.roster_entries = relationship(
    'RosterPlayersInSeries',
    back_populates='team',
    overlaps="players,teams"
)

# Add relationship properties to Player
Player.team_rosters = relationship(
    'RosterPlayersInSeries',
    back_populates='player',
    overlaps="players,teams"
)
