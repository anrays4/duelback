from django.urls import path
from .views import playing_game_page

from .views import (
    game_table_list, find_match, PlayerReadyAPIView, PollingTurnAPIView, ConfirmMoveAPIView,
)


urlpatterns = [
    path('playing-game/', playing_game_page, name="playing_backgammon_game"),

    # URLs برای GameTable
    path('gametables/', game_table_list, name='gametable_list'),
    path('find-match/', find_match, name='find_match'),
    path('i_am_ready/<uuid:room_id>/', PlayerReadyAPIView.as_view(), name='player_ready'),
    #path('polling/ready/<uuid:room_id>/', PollingReadyAPIView.as_view(), name='polling_ready'),
    path('check_my_turn/turn/<uuid:room_id>/', PollingTurnAPIView.as_view(), name='polling_turn'),
    path('confirm_my_move/<uuid:room_id>/', ConfirmMoveAPIView.as_view(), name='confirm_move'),
]