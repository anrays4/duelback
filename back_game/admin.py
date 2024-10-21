from django.contrib import admin

from .models import GameTable, WaitingRoom, GameRoom, PlayerWarning


@admin.register(GameTable)
class GameTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'fee', 'image', 'xp_for_winner', 'xp_for_loser', 'is_active', 'created_time')
    search_fields = ('name',)
    list_filter = ('created_time',)
    ordering = ('-created_time',)


@admin.register(WaitingRoom)
class WaitingRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_table', 'player_1', 'deadline', 'created_time')
    list_filter = ('game_table', 'deadline')
    search_fields = ('player1__username', 'player2__username')


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'waiting_room', 'player_1', 'player_2')
    search_fields = ('player_1__username', 'player_2__username')

    fieldsets = (
        (None, {
            'fields': ('waiting_room', 'player1', 'player2', 'current_turn', 'board_state')
        }),
        ('Timestamps', {
            'fields': ('last_move_time', 'move_deadline')
        }),
    )


@admin.register(PlayerWarning)
class PlayerWarningAdmin(admin.ModelAdmin):
    list_display = ('player', 'reason', 'expiry_date')
    search_fields = ('player__username',)