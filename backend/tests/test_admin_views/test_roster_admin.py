import pytest
import pytest_asyncio
from unittest.mock import Mock, patch
from datetime import datetime
from app.models import SeriesRegistration, Player, Series, GameType, RosterPlayersInSeries, Base
from sqlalchemy import select
from app.admin_views.views.roster_admin import RosterAdmin

@pytest_asyncio.fixture(autouse=True)
async def setup_database(async_session):
    async with async_session as session:
        await session.run_sync(Base.metadata.create_all)
    yield
    async with async_session as session:
        await session.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def test_game_type(async_session):
    game_type = GameType(
        name="Test Type",
        team_player_amount=4,
        game_player_amount=4,
        team_throws_in_set=16
    )
    async_session.add(game_type)
    await async_session.commit()
    await async_session.refresh(game_type)
    return game_type

@pytest_asyncio.fixture
async def test_series(async_session, test_game_type):
    series = Series(
        name="Test Series",
        year=2024,
        game_type_id=test_game_type.id,
        season_type="winter"
    )
    async_session.add(series)
    await async_session.commit()
    await async_session.refresh(series)
    return series

@pytest_asyncio.fixture
async def test_player(async_session):
    player = Player(
        name="Test Player",
        email="test@example.com",
        gdpr_consent=True
    )
    async_session.add(player)
    await async_session.commit()
    await async_session.refresh(player)
    return player

@pytest_asyncio.fixture
async def test_registration(async_session, test_series, test_player):
    registration = SeriesRegistration(
        series_id=test_series.id,
        team_name="Test Team",
        team_abbreviation="TT",
        contact_player_id=test_player.id
    )
    async_session.add(registration)
    await async_session.commit()
    await async_session.refresh(registration)
    return registration

@pytest.fixture
def mock_db_session():
    session = Mock()
    session.commit = Mock()
    session.add = Mock()
    session.query = Mock()
    return session

@pytest.fixture
def mock_series():
    series = Mock(spec=Series)
    series.id = 1
    series.name = "Test Series"
    series.year = 2024
    return series

@pytest.fixture
def mock_game_type():
    game_type = Mock(spec=GameType)
    game_type.id = 1
    game_type.team_player_amount = 4
    return game_type

@pytest.fixture
def mock_player():
    player = Mock(spec=Player)
    player.id = 1
    player.name = "Test Player"
    player.email = "test@example.com"
    return player

@pytest.fixture
def mock_registration(mock_series, mock_player, mock_game_type):
    registration = Mock(spec=SeriesRegistration)
    registration.id = 1
    registration.series = mock_series
    registration.contact_player = mock_player
    registration.team_name = "Test Team"
    registration.team_abbreviation = "TT"
    mock_series.game_type = mock_game_type
    return registration

def test_roster_create(mock_db_session, mock_registration, mock_player):
    """Test creating a new roster entry"""
    roster_admin = RosterAdmin(RosterPlayersInSeries, mock_db_session)
    
    # Mock form data
    form = Mock()
    form.registration_id.data = str(mock_registration.id)
    form.player_id.data = str(mock_player.id)
    
    # Mock query to check for existing roster entry
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    
    # Call the model change method
    model = RosterPlayersInSeries()
    roster_admin.on_model_change(form, model, is_created=True)
    
    # Verify
    assert model.registration_id == mock_registration.id
    assert model.player_id == mock_player.id
    mock_db_session.add.assert_called_once()

def test_roster_duplicate_player(mock_db_session, mock_registration, mock_player):
    """Test that adding the same player twice fails"""
    roster_admin = RosterAdmin(RosterPlayersInSeries, mock_db_session)
    
    # Mock existing roster entry
    existing_roster = RosterPlayersInSeries()
    existing_roster.registration_id = mock_registration.id
    existing_roster.player_id = mock_player.id
    
    # Mock query to find existing roster entry
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = existing_roster
    
    # Mock form data
    form = Mock()
    form.registration_id.data = str(mock_registration.id)
    form.player_id.data = str(mock_player.id)
    
    # Call and verify it raises an error
    with pytest.raises(ValueError, match="Player already exists in roster"):
        roster_admin.on_model_change(form, RosterPlayersInSeries(), is_created=True)

def test_roster_player_limit(mock_db_session, mock_registration):
    """Test that roster respects team player limit"""
    roster_admin = RosterAdmin(RosterPlayersInSeries, mock_db_session)
    
    # Mock that team already has max players
    mock_db_session.query.return_value.filter_by.return_value.count.return_value = 4
    
    # Mock form data
    form = Mock()
    form.registration_id.data = str(mock_registration.id)
    form.player_id.data = "5"  # New player
    
    # Call and verify it raises an error
    with pytest.raises(ValueError, match="Player limit exceeded"):
        roster_admin.on_model_change(form, RosterPlayersInSeries(), is_created=True)
