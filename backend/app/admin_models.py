from fastapi_admin.resources import Model, Link
from fastapi_admin.widgets import displays, inputs
from app.models import User, GameType, Player, Series, TeamInSeries, TeamHistory, Game, SingleThrow, SingleRoundThrow
from fastapi_admin.models import AbstractAdmin

class Home(Link):
    label = "Home"
    icon = "fas fa-home"
    url = "/admin"

class GithubLink(Link):
    label = "Github"
    url = "https://github.com/fastapi-admin/fastapi-admin"
    icon = "fab fa-github"
    target = "_blank"

class UserAdmin(AbstractAdmin):
    label = "User"
    model = User
    icon = "fas fa-user"
    page_pre_title = "User Management"
    page_title = "Users"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("username", label="Username", display=displays.Display()),
        inputs.Input("email", label="Email", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class GameTypeAdmin(Model):
    label = "Game Type"
    model = GameType
    icon = "fas fa-gamepad"
    page_pre_title = "Game Type Management"
    page_title = "Game Types"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("name", label="Name", display=displays.Display()),
        inputs.Input("max_players", label="Max Players", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class PlayerAdmin(Model):
    label = "Player"
    model = Player
    icon = "fas fa-user"
    page_pre_title = "Player Management"
    page_title = "Players"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("name", label="Name", display=displays.Display()),
        inputs.Input("email", label="Email", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class SeriesAdmin(Model):
    label = "Series"
    model = Series
    icon = "fas fa-trophy"
    page_pre_title = "Series Management"
    page_title = "Series"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("name", label="Name", display=displays.Display()),
        inputs.Input("season_type", label="Season Type", display=displays.Display()),
        inputs.Input("year", label="Year", display=displays.Display()),
        inputs.Input("status", label="Status", display=displays.Display()),
        inputs.Input("game_type_id", label="Game Type ID", display=displays.Display()),
        inputs.Input("registration_open", label="Registration Open", display=displays.Display()),
        inputs.Input("is_cup_league", label="Is Cup League", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class TeamInSeriesAdmin(Model):
    label = "Team In Series"
    model = TeamInSeries
    icon = "fas fa-users"
    page_pre_title = "Team In Series Management"
    page_title = "Teams In Series"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("series_id", label="Series ID", display=displays.Display()),
        inputs.Input("team_name", label="Team Name", display=displays.Display()),
        inputs.Input("team_abbreviation", label="Team Abbreviation", display=displays.Display()),
        inputs.Input("group", label="Group", display=displays.Display()),
        inputs.Input("contact_player_id", label="Contact Player ID", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class TeamHistoryAdmin(Model):
    label = "Team History"
    model = TeamHistory
    icon = "fas fa-history"
    page_pre_title = "Team History Management"
    page_title = "Team Histories"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("previous_registration_id", label="Previous Registration ID", display=displays.Display()),
        inputs.Input("next_registration_id", label="Next Registration ID", display=displays.Display()),
        inputs.Input("relation_type", label="Relation Type", display=displays.Display()),
        inputs.Input("notes", label="Notes", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class GameAdmin(Model):
    label = "Game"
    model = Game
    icon = "fas fa-gamepad"
    page_pre_title = "Game Management"
    page_title = "Games"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("round", label="Round", display=displays.Display()),
        inputs.Input("is_playoff", label="Is Playoff", display=displays.Display()),
        inputs.Input("series_id", label="Series ID", display=displays.Display()),
        inputs.Input("game_date", label="Game Date", display=displays.Display()),
        inputs.Input("team_1_id", label="Team 1 ID", display=displays.Display()),
        inputs.Input("team_2_id", label="Team 2 ID", display=displays.Display()),
        inputs.Input("score_1_1", label="Score 1-1", display=displays.Display()),
        inputs.Input("score_1_2", label="Score 1-2", display=displays.Display()),
        inputs.Input("score_2_1", label="Score 2-1", display=displays.Display()),
        inputs.Input("score_2_2", label="Score 2-2", display=displays.Display()),
        inputs.Input("created_at", label="Created At", display=displays.Display()),
    ]

class SingleThrowAdmin(Model):
    label = "Single Throw"
    model = SingleThrow
    icon = "fas fa-archery"
    page_pre_title = "Single Throw Management"
    page_title = "Single Throws"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("throw_type", label="Throw Type", display=displays.Display()),
        inputs.Input("throw_score", label="Throw Score", display=displays.Display()),
    ]

class SingleRoundThrowAdmin(Model):
    label = "Single Round Throw"
    model = SingleRoundThrow
    icon = "fas fa-archery"
    page_pre_title = "Single Round Throw Management"
    page_title = "Single Round Throws"
    fields = [
        inputs.Input("id", label="ID", display=displays.Display()),
        inputs.Input("game_id", label="Game ID", display=displays.Display()),
        inputs.Input("game_set_index", label="Game Set Index", display=displays.Display()),
        inputs.Input("throw_position", label="Throw Position", display=displays.Display()),
        inputs.Input("home_team", label="Home Team", display=displays.Display()),
        inputs.Input("player_id", label="Player ID", display=displays.Display()),
        inputs.Input("throw_1", label="Throw 1", display=displays.Display()),
        inputs.Input("throw_2", label="Throw 2", display=displays.Display()),
        inputs.Input("throw_3", label="Throw 3", display=displays.Display()),
        inputs.Input("throw_4", label="Throw 4", display=displays.Display()),
    ]