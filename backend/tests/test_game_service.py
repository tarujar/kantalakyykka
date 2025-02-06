import pytest
from app.services.game_service import GameService
from unittest.mock import Mock, patch, call

@pytest.fixture
def game_service():
    return GameService()

@pytest.fixture
def mock_session():
    session = Mock()
    session.query = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    return session

@pytest.fixture
def mock_form():
    form = Mock()
    # Create mock team throws
    team1_throws = Mock()
    team2_throws = Mock()
    
    # Make form.team_X_round_throws iterable
    form.team_1_round_throws = [team1_throws]
    form.team_2_round_throws = [team2_throws]
    
    # Create mock round data
    round_data = Mock()
    round_data.throw_1 = Mock(data="10")
    round_data.throw_2 = Mock(data="H")
    round_data.throw_3 = Mock(data="5")
    round_data.throw_4 = Mock(data="F")
    round_data.player_id = Mock(data="1")
    
    # Make entries accessible by f'round_{num}'
    team1_throws.round_1 = [round_data]
    team1_throws.round_2 = [round_data]
    team2_throws.round_1 = [round_data]
    team2_throws.round_2 = [round_data]
    
    return form

def test_process_game_throws(game_service, mock_session, mock_form):
    # Setup mock for existing throws query
    mock_session.query().filter_by().all.return_value = []
    
    with patch.object(game_service.throw_service, 'save_round_throw') as mock_save:
        mock_save.return_value = True
        
        result = game_service.process_game_throws(1, mock_form, mock_session)
        
        assert result is True
        assert mock_save.call_count == 4  # 2 teams × 2 rounds
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_called_once()  # Initial rollback

def test_process_game_throws_error(game_service, mock_session, mock_form):
    # Setup mock for existing throws query
    mock_session.query().filter_by().all.return_value = []
    
    # Mock commit to raise an exception
    mock_session.commit.side_effect = Exception("Test error")

    # Track rollback calls
    initial_rollback_call = call()
    error_rollback_call = call()
    expected_calls = [initial_rollback_call, error_rollback_call]
    
    with pytest.raises(Exception) as exc_info:
        game_service.process_game_throws(1, mock_form, mock_session)

    assert str(exc_info.value) == "Test error"
    assert mock_session.rollback.call_count == 2
    mock_session.rollback.assert_has_calls(expected_calls)
