# ...existing code...

## Running the Application

To run the Flask application with Gunicorn, use the following command:

```sh
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

**Note:** Do not use Uvicorn to run the Flask application as it is not compatible with Flask's WSGI interface.

# data flow from form.html to db

1. Form Submission (in game_score_sheet.html):

`User Input → HTML Form → POST request with form data`

2. View Processing (game_score_sheet_view.py):

```
1. Request received in edit_form_view()
2. Form data parsed into GameScoreSheetForm instance
3. Form validation
4. If valid → game_service.process_game_throws()
```

3. Game Service (game_service.py):

```
process_game_throws()
├── Get existing throws from DB
├── For each team (1 & 2):
│   └── For each round (1 & 2):
│       └── _process_round_throws() → throw_service.save_round_throw()
```

4. Throw Service (throw_service.py):

```
save_round_throw()
├── For each throw (1-4):
│   └── save_throw()
│       ├── _process_throw_data() → Convert input to throw_type and score
│       └── _get_or_create_throw() → Create/Update SingleThrow record
└── Create/Update SingleRoundThrow record
```

5. Database Schema:

```
SingleThrow
├── id
├── throw_type (VALID/HAUKI/FAULT/E)
└── throw_score

SingleRoundThrow
├── id
├── game_id
├── game_set_index (round number)
├── throw_position (1-4)
├── home_team (boolean)
├── player_id
└── throw_1/2/3/4 (foreign keys to SingleThrow)
```

6. Example data flow for one throw:

```
Form Input: "10"
↓
GameScoreSheetForm
└── team_1_round_throws[0].round_1[0].throw_1 = "10"
↓
ThrowService._process_throw_data()
└── Returns (ThrowType.VALID, 10)
↓
Database:
1. SingleThrow record created: {throw_type: VALID, throw_score: 10}
2. SingleRoundThrow record links to this throw via throw_1/2/3/4
```

This structure allows for:

- Individual throw tracking
- Round-based organization
- Player attribution
- Team association
- Game context
