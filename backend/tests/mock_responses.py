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
