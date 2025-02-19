from .views.user_views import UserAdmin
from .views.game_views import GameTypeAdmin, GameAdmin, SingleThrowAdmin, SingleRoundThrowAdmin
from .views.team_views import SeriesRegistrationAdmin, TeamHistoryAdmin, PlayerAdmin
from .views.series_views import SeriesAdmin
from .views.roster_admin import RosterAdmin

__all__ = [
    'UserAdmin',
    'PlayerAdmin',
    'GameTypeAdmin',
    'SeriesAdmin',
    'GameAdmin',
    'SeriesRegistrationAdmin',
    'TeamHistoryAdmin',
    'SingleThrowAdmin',
    'SingleRoundThrowAdmin',
    'RosterAdmin'
]
