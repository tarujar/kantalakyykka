from app.models.schemas import GameType, SeriesCreate, TeamInSeries, RosterPlayer

mock_game_types = [
    {"id": 1, "name": "Henkkari", "max_players": 1},
    {"id": 2, "name": "Pari", "max_players": 2},
    {"id": 3, "name": "WCOK", "max_players": 4},
    {"id": 4, "name": "Joukkue", "max_players": 8}
]

mock_players = [
    {"id": 1, "name": "Matti Meikalainen", "email": "matti@example.com"},
    {"id": 2, "name": "Teppo Testaaja", "email": "teppo@example.com"},
    {"id": 3, "name": "Liisa Pelaaja", "email": "liisa@example.com"},
    {"id": 4, "name": "Anna Heittaja", "email": "anna@example.com"}
]

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
    TeamInSeries(
        series_id=1,
        team_name="Team A",
        team_abbreviation="TA",
        contact_player_id=1
    )
]

mock_roster_players = [
    RosterPlayer(
        registration_id=1,
        player_id=1
    )
]