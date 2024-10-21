from rest_framework import serializers
from .models import GameTable, WaitingRoom, GameRoom, PlayerWarning


# سریالایزر برای مدل GameTable
class GameTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTable
        fields = ['name', 'fee', 'image', 'xp_for_winner', 'xp_for_loser', 'is_active']


# Waiting Room Serializer
class WaitingRoomSerializer(serializers.ModelSerializer):
    player1 = serializers.StringRelatedField()

    class Meta:
        model = WaitingRoom
        fields = ['id', 'game_table', 'player_1', 'deadline']


# Game Room Serializer
class GameRoomSerializer(serializers.ModelSerializer):
    player1 = serializers.StringRelatedField()
    player2 = serializers.StringRelatedField()
    current_turn = serializers.StringRelatedField()

    class Meta:
        model = GameRoom
        fields = [
            'id',
            'player_1',
            'player_2',
            'is_ready1',
            'is_ready2',
            'dice1',
            'dice2',
            'current_turn',
            'last_move_time',
            'move_deadline',
            'board_state'
        ]

    def validate(self, data):
        # اعتبارسنجی deadline برای اطمینان از اینکه تغییرات نادرست وارد نشوند
        if 'move_deadline' in data and data['move_deadline'] < data['last_move_time']:
            raise serializers.ValidationError("Move deadline cannot be before the last move time.")
        return data


# Player Warning Serializer
class PlayerWarningSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()

    class Meta:
        model = PlayerWarning
        fields = ['player', 'reason', 'expiry_date']