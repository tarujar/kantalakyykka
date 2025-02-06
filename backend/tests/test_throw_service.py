import pytest
from app.services.throw_service import ThrowService
from app.models.models import ThrowType, SingleThrow
from unittest.mock import Mock, patch

@pytest.fixture
def throw_service():
    return ThrowService()

@pytest.fixture
def mock_session():
    session = Mock()
    session.add = Mock()
    session.flush = Mock()
    session.query = Mock()
    return session

def test_save_throw_valid_score(throw_service, mock_session):
    mock_throw = SingleThrow(id=1, throw_type=ThrowType.VALID, throw_score=10)
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    
    # Mock the internal methods
    with patch.object(throw_service, '_process_throw_data') as mock_process:
        mock_process.return_value = (ThrowType.VALID, 10)
        with patch.object(throw_service, '_get_or_create_throw') as mock_get_or_create:
            mock_get_or_create.return_value = mock_throw
            
            throw_id = throw_service.save_throw(mock_session, "10")
            
            assert throw_id == 1
            mock_session.add.assert_called_once_with(mock_throw)
            mock_session.flush.assert_called_once()

def test_save_throw_hauki(throw_service, mock_session):
    mock_throw = SingleThrow(id=1, throw_type=ThrowType.HAUKI, throw_score=0)
    mock_session.add.return_value = None
    mock_session.flush.return_value = None
    
    with patch.object(throw_service, '_process_throw_data') as mock_process:
        mock_process.return_value = (ThrowType.HAUKI, 0)
        with patch.object(throw_service, '_get_or_create_throw') as mock_get_or_create:
            mock_get_or_create.return_value = mock_throw
            
            throw_id = throw_service.save_throw(mock_session, "H")
            
            assert throw_id == 1
            mock_session.add.assert_called_once_with(mock_throw)
            mock_session.flush.assert_called_once()

def test_save_throw_update_existing(throw_service, mock_session):
    existing_throw = SingleThrow(id=1, throw_type=ThrowType.VALID, throw_score=5)
    updated_throw = SingleThrow(id=1, throw_type=ThrowType.VALID, throw_score=10)
    
    with patch.object(throw_service, '_process_throw_data') as mock_process:
        mock_process.return_value = (ThrowType.VALID, 10)
        with patch.object(throw_service, '_get_or_create_throw') as mock_get_or_create:
            mock_get_or_create.return_value = updated_throw
            
            throw_id = throw_service.save_throw(mock_session, "10", existing_throw_id=1)
            
            assert throw_id == 1
            mock_session.add.assert_called_once_with(updated_throw)

def test_save_round_throw(throw_service, mock_session):
    with patch.object(throw_service, 'save_throw') as mock_save_throw:
        mock_save_throw.side_effect = [1, 2, 3, 4]  # IDs for the four throws
        
        result = throw_service.save_round_throw(
            session=mock_session,
            game_id=1,
            round_num=1,
            position=1,
            is_home_team=True,
            player_id="1",
            throws=["10", "H", "5", "F"]
        )
        
        assert result is True
        assert mock_save_throw.call_count == 4
        mock_session.add.assert_called()
        mock_session.flush.assert_called()

def test_process_throw_data(throw_service):
    # Test numeric input
    throw_type, throw_score = throw_service._process_throw_data("10")
    assert throw_type == ThrowType.VALID.value
    assert throw_score == 10
    
    # Test special throws
    throw_type, throw_score = throw_service._process_throw_data("H")
    assert throw_type == ThrowType.HAUKI.value
    assert throw_score == 0
