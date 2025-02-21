from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, Text, TIMESTAMP, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship, backref
import enum
from datetime import datetime, timezone

Base = declarative_base()

class ThrowType(enum.Enum):
    VALID = "VALID"
    HAUKI = "HAUKI"
    FAULT = "FAULT"
    E = "E"

class GameType(Base):
    __tablename__ = "game_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    team_player_amount = Column(Integer, nullable=False)
    game_player_amount = Column(Integer, nullable=False, default=4)
    team_throws_in_set = Column(Integer, nullable=False, default=16)
    throw_round_amount = Column(Integer, nullable=False, default=4)
    kyykka_amount = Column(Integer, nullable=False, default=40)
    series = relationship("Series", back_populates="game_type")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    gdpr_consent = Column(Boolean, default=False, nullable=False)  # Add this line
    roster_entries = relationship('RosterPlayersInSeries', back_populates='player')
    # The throws will be accessed through SingleThrow relationship
    throws = relationship("SingleThrow", back_populates="player")

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
    registrations = relationship("SeriesRegistration", back_populates="series")  # Keep this one
    games = relationship("Game", back_populates="series")

class SeriesRegistration(Base):
    __tablename__ = "series_registrations"
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
    lohko = Column(String(50))
    team_name = Column(String(100))
    team_abbreviation = Column(String(10))
    contact_player_id = Column(Integer, ForeignKey("players.id"))
    
    series = relationship("Series", back_populates="registrations")  # Changed from backref to back_populates
    contact_player = relationship("Player", backref="contact_for_registrations")
    roster_entries = relationship(
        'RosterPlayersInSeries',
        back_populates='registration',
        cascade="all, delete-orphan"
    )

class TeamHistory(Base):
    __tablename__ = "team_history"
    id = Column(Integer, primary_key=True, index=True)
    previous_registration_id = Column(Integer, ForeignKey("series_registrations.id"))  # Changed from teams_in_series
    next_registration_id = Column(Integer, ForeignKey("series_registrations.id"))  # Changed from teams_in_series
    relation_type = Column(String, nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
    series = relationship("Series", back_populates="games")
    round = Column(String)
    is_playoff = Column(Boolean, default=False)
    game_date = Column(Date, nullable=False)
    team_1_id = Column(Integer, ForeignKey("series_registrations.id"), nullable=False)
    team_2_id = Column(Integer, ForeignKey("series_registrations.id"), nullable=False)
    score_1_1 = Column(Integer, nullable=False)
    score_1_2 = Column(Integer, nullable=False)
    score_2_1 = Column(Integer, nullable=False)
    score_2_2 = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    __table_args__ = (
        UniqueConstraint('series_id', 'game_date', 'team_1_id', 'team_2_id', 'round'),
    )
    
    team_1 = relationship("SeriesRegistration", foreign_keys=[team_1_id])
    team_2 = relationship("SeriesRegistration", foreign_keys=[team_2_id])
    throw_rounds = relationship("SingleRoundThrow", back_populates="game")
    
    @property
    def round_count(self): #Fixme - this should be calculated based on game type
        if self.series.game_type.team_player_amount == 2:
            return 5
        elif self.series.game_type.team_player_amount == 4:
            return 4
        else:
            return 5

class SingleThrow(Base):
    __tablename__ = "single_throw"
    id = Column(Integer, primary_key=True, index=True)
    throw_type = Column(Enum(ThrowType), nullable=False)
    throw_score = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    throw_index = Column(Integer, nullable=False)
    
    # Add the back_populates reference to Player
    player = relationship("Player", back_populates="throws")
    
    __table_args__ = (
        CheckConstraint('throw_index > 0 AND throw_index <= 20', name='valid_throw_index'),
    )

class SingleRoundThrow(Base):
    __tablename__ = "single_round_throws"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game_set_index = Column(Integer, nullable=False)  # 1 or 2
    throw_position = Column(Integer, nullable=False)  # 1-5 within a set. could be renamed as round_index
    home_team = Column(Boolean, nullable=False)
    team_id = Column(Integer, ForeignKey("series_registrations.id"))
    throw_1 = Column(Integer, ForeignKey("single_throw.id"))
    throw_2 = Column(Integer, ForeignKey("single_throw.id"))
    throw_3 = Column(Integer, ForeignKey("single_throw.id"))
    throw_4 = Column(Integer, ForeignKey("single_throw.id"))

    game = relationship("Game", back_populates="throw_rounds")
    team = relationship("SeriesRegistration")
    throws_1 = relationship("SingleThrow", foreign_keys=[throw_1])
    throws_2 = relationship("SingleThrow", foreign_keys=[throw_2])
    throws_3 = relationship("SingleThrow", foreign_keys=[throw_3])
    throws_4 = relationship("SingleThrow", foreign_keys=[throw_4])

    # Add constraints for valid set and position indices
    __table_args__ = (
        CheckConstraint('game_set_index IN (1, 2)', name='valid_set_index'),
        CheckConstraint('throw_position >= 1 AND throw_position <= 5', name='valid_position'),
        UniqueConstraint('game_id', 'game_set_index', 'throw_position', 'home_team', name='unique_round_throw')
    )

class RosterPlayersInSeries(Base):
    __tablename__ = 'roster_players_in_series'
    registration_id = Column(Integer, ForeignKey('series_registrations.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    
    registration = relationship('SeriesRegistration', back_populates='roster_entries')
    player = relationship('Player', back_populates='roster_entries')
    
    def __str__(self):
        team_name = self.registration.team_name if self.registration else "Unknown team"
        player_name = self.player.name if self.player else "Unknown player"
        return f"{team_name} - {player_name}"
