from datetime import datetime, timezone
from app.models.models import GameType, Player, Game, Series, SeriesRegistration
from app.models import GameTypeCreate, SeriesCreate, SeriesRegistration

mock_game_types = [
    {
        "id": 1,
        "name": "Henkkari",
        "team_player_amount": 1,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": 2,
        "name": "Pari",
        "team_player_amount": 2,
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {"id": 3, "name": "WCOK", "team_player_amount": 4},
    {"id": 4, "name": "Joukkue", "team_player_amount": 8}
]

mock_game_type_single = {"id": 1, "name": "Henkkari", "team_player_amount": 1}

mock_players = [
    {"id": 1, "name": "Matti Meikalainen", "email": "matti@example.com"},
    {"id": 2, "name": "Teppo Testaaja", "email": "teppo@example.com"},
    {"id": 3, "name": "Liisa Pelaaja", "email": "liisa@example.com"},
    {"id": 4, "name": "Anna Heittaja", "email": "anna@example.com"}
]

mock_player_1 = {"id": 1, "name": "Matti Meikalainen", "email": "matti@example.com"}
mock_player_2 = {"id": 2, "name": "Teppo Testaaja", "email": "teppo@example.com"}

mock_games = [
    {
        "id": 1,
        "game_type": 1,
        "players": [mock_players[0]],
        "points_multiplier": 1,
        "score_1_1": -23,
        "score_1_2": -25,
        "score_2_1": 2,
        "score_2_2": -15
    },
    {
        "id": 2,
        "game_type": 2,
        "players": [mock_players[0], mock_players[1]],
        "points_multiplier": 2,
        "score_1_1": 10,
        "score_1_2": 5,
        "score_2_1": 15,
        "score_2_2": 10
    }
]

mock_series = [
    SeriesCreate(
        name="OKL-A-2024",
        season_type="winter",
        year=2024,
        status="upcoming",
        registration_open=True,
        game_type_id=4
    )
]

mock_teams_in_series = [
    SeriesRegistration(
        series_id=1,
        team_name="Team A",
        team_abbreviation="TA",
        contact_player_id=1
    )
]

mock_new_game_type = {"name": "New Game Type", "team_player_amount": 4}
mock_invalid_game_type = {"name": "", "team_player_amount": -1}
mock_updated_game_type = {"name": "Updated Game Type", "team_player_amount": 5}

mock_new_player = {"name": "New Player", "email": "newplayer@example.com"}
mock_invalid_player = {"name": "", "email": "invalid-email"}

mock_new_series = {
    "name": "New Series",
    "season_type": "winter",
    "year": 2024,
    "status": "upcoming",
    "registration_open": True,
    "game_type_id": 1
}
mock_invalid_series = {
    "name": "",
    "season_type": "invalid",
    "year": 2024,
    "status": "upcoming",
    "registration_open": True,
    "game_type_id": 1
}

mock_new_game = {
    "round": "1",
    "is_playoff": False,
    "series_id": 1,
    "game_date": "2024-01-01",
    "team_1_id": 1,
    "team_2_id": 2,
    "score_1_1": 10,
    "score_1_2": 5,
    "score_2_1": 15,
    "score_2_2": 10
}
mock_invalid_game = {
    "round": "1",
    "is_playoff": False,
    "series_id": 1,
    "game_date": "2024-01-01",
    "team_1_id": 1,  # Invalid: same team
    "team_2_id": 1,
    "score_1_1": 10,
    "score_1_2": 5,
    "score_2_1": 15,
    "score_2_2": 10
}

mock_game_data = {
    "round": "1",
    "is_playoff": False,
    "series_id": 1,
    "game_date": "2024-01-01",
    "team_1_id": 1,
    "team_2_id": 2,
    "score_1_1": 10,
    "score_1_2": 5,
    "score_2_1": 15,
    "score_2_2": 10
}

mock_invalid_game_data = {
    "round": "1",
    "is_playoff": False,
    "series_id": 1,
    "game_date": "2024-01-01",
    "team_1_id": 1,
    "team_2_id": 1,  # Invalid: same team
    "score_1_1": 10,
    "score_1_2": 5,
    "score_2_1": 15,
    "score_2_2": 10
}

mock_game_response = {
    "id": 1,
    "round": "1",
    "is_playoff": False,
    "series_id": 1,
    "game_date": "2024-01-01",
    "team_1_id": 1,
    "team_2_id": 2,
    "score_1_1": 10,
    "score_1_2": 5,
    "score_2_1": 15,
    "score_2_2": 10
}

mock_games_list_response = [
    {"id": 1, "round": "1", "is_playoff": False, "series_id": 1, "game_date": "2024-01-01", "team_1_id": 1, "team_2_id": 2, "score_1_1": 10, "score_1_2": 5, "score_2_1": 15, "score_2_2": 10},
    {"id": 2, "round": "2", "is_playoff": False, "series_id": 1, "game_date": "2024-01-02", "team_1_id": 3, "team_2_id": 4, "score_1_1": 20, "score_1_2": 10, "score_2_1": 25, "score_2_2": 20}
]
