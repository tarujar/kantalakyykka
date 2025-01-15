from datetime import datetime, timezone

game_types_response = {
    "status_code": 200,
    "data": [
        {
            "id": 1,
            "name": "Henkkari",
            "max_players": 1,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": 2,
            "name": "Pari",
            "max_players": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
}

game_type_response = {
    "status_code": 200,
    "data": {
        "id": 1,
        "name": "Henkkari",
        "max_players": 1,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
}

error_responses = {
    "not_found": {
        "status_code": 404,
        "detail": "Item not found"
    },
    "validation_error": {
        "status_code": 422,
        "detail": "Validation error"
    }
}

new_game_type_response = {
    "status_code": 201,
    "data": {
        "name": "New Game Type",
        "max_players": 4
    }
}

updated_game_type_response = {
    "status_code": 200,
    "data": {
        "name": "Updated Game Type",
        "max_players": 5
    }
}

new_player_response = {
    "status_code": 201,
    "data": {
        "name": "New Player",
        "email": "newplayer@example.com"
    }
}

new_series_response = {
    "status_code": 201,
    "data": {
        "name": "New Series",
        "season_type": "winter",
        "year": 2024,
        "status": "upcoming",
        "registration_open": True,
        "game_type_id": 1
    }
}

new_game_response = {
    "status_code": 201,
    "data": {
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
}
