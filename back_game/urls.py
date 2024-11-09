from django.urls import path
from .views import playing_game_page, CheckTimePlease, IWantLeave, find_match_page, FindMatch, CancelFindMatch, \
    backgammon_leaderboard

from .views import (
    game_table_page, PlayerReadyAPIView, PollingTurnAPIView, ConfirmMoveAPIView,
)

urlpatterns = [
    # GameTable view
    path('game-table/', game_table_page, name='game_table_page'),

    # playing game view
    path('playing-game/<game_room_id>/', playing_game_page, name="playing_backgammon_game"),

    # playing game api
    path('check_my_turn/turn/<uuid:room_id>/', PollingTurnAPIView.as_view(), name='polling_turn'),
    path('confirm_my_move/<uuid:room_id>/', ConfirmMoveAPIView.as_view(), name='confirm_move'),
    path('check_time/<uuid:room_id>/', CheckTimePlease.as_view(), name='check_time'),
    path('i_want_leave/<uuid:room_id>/', IWantLeave.as_view(), name='i_want_leave'),
    path('i_am_ready/<uuid:room_id>/', PlayerReadyAPIView.as_view(), name='player_ready'),

    # find match view
    path('find-match/<table_id>/', find_match_page, name="find_match"),

    # find match api
    path('find-match-is-ready/', FindMatch.as_view(), name="find_match_is_ready"),
    path('cancel-find-match/', CancelFindMatch.as_view(), name="cancel_find_match"),

    # backgammon leaderboard view
    path('leaderboard/', backgammon_leaderboard, name="backgammon_leaderboard"),


]
