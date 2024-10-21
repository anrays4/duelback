from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

import uuid
import random


class GameTable(models.Model):
    name = models.CharField(max_length=255)
    fee = models.IntegerField()
    image = models.ImageField(upload_to='table_images/', blank=True, null=True)
    xp_for_winner = models.IntegerField()
    xp_for_loser = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Game_Table'
        verbose_name_plural = 'Game_Tables'

    def __str__(self):
        return self.name


class WaitingRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_table = models.ForeignKey(GameTable, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1_waiting', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now() + timedelta(minutes=2))  # 2-minute deadline


    class Meta:
        db_table = 'waiting_rooms'
        verbose_name = 'Waiting_Room'
        verbose_name_plural = 'Waiting_Rooms'

    def is_expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return f"WaitingRoom for {self.game_table.name} (Player1: {self.player_1.username})"


class GameRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    waiting_room = models.OneToOneField(WaitingRoom, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='game_player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='game_player_2', on_delete=models.CASCADE)
    is_ready1 = models.BooleanField(default=False)
    is_ready2 = models.BooleanField(default=False)
    dice1 = models.IntegerField(blank=True, null=True)  # مقدار تاس اول
    dice2 = models.IntegerField(blank=True, null=True)  # مقدار تاس دوم
    current_turn = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='current_turn', null=True, blank=True, on_delete=models.SET_NULL)
    last_move_time = models.DateTimeField(null=True, blank=True)
    move_deadline = models.DateTimeField(null=True, blank=True)
    move_history = models.JSONField(default=dict)
    place_status = models.JSONField(default=dict)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'game_rooms'
        verbose_name = 'Game_Room'
        verbose_name_plural = 'Game_Rooms'

    def has_both_ready(self):
        return self.is_ready1 and self.is_ready2

    def mark_ready(self, player):
        if player == self.player_1:
            self.is_ready1 = True
        elif player == self.player_2:
            self.is_ready2 = True
        self.save()

    def roll_dice(self):
        """تولید مقدار جدید برای دو تاس"""
        import random
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.save()

    def set_turn(self):
        """تعیین بازیکنی که بازی را شروع می‌کند بر اساس نتیجه تاس‌ها"""
        if self.dice1 > self.dice2:
            self.current_turn = self.player_1
        elif self.dice2 > self.dice1:
            self.current_turn = self.player_2
        else:
            # اگر مقدار تاس‌ها برابر باشد، دوباره تاس می‌ریزیم تا برنده مشخص شود
            self.roll_dice()
            self.set_turn()
        self.save()

    def switch_turn(self):
        """تغییر نوبت بین پلیر 1 و پلیر 2"""
        self.current_turn = self.player_2 if self.current_turn == self.player_1 else self.player_1
        self.save()

    def update_board_state(self, new_state):
        """به‌روزرسانی وضعیت تخته"""
        self.place_status = new_state
        self.save()

    def __str__(self):
        return f"GameRoom between {self.player_1.username} and {self.player_2.username}"


class PlayerWarning(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()

    class Meta:
        db_table = 'player_warnings'
        verbose_name = 'Player_Warning'
        verbose_name_plural = 'Player_Warnings'


# class GameTable(models.Model):
#     name = models.CharField(max_length=255)  # اسم میز بازی
#     fee = models.IntegerField()  # هزینه ورود به بازی در این میز
#     image = models.ImageField(upload_to='table_images/', blank=True, null=True)  # تصویر میز (آپلود تصاویر)
#     xp_for_winner = models.IntegerField()  # مقدار XP برای برنده
#     xp_for_loser = models.IntegerField()  # مقدار XP برای بازنده
#     created_time = models.DateTimeField(auto_now_add=True)  # زمان ایجاد میز
#     updated_time = models.DateTimeField(auto_now=True)  # زمان بروزرسانی اطلاعات میز
#
#     class Meta:
#         db_table = 'game_tables'
#         verbose_name = 'Game_Table'
#         verbose_name_plural = 'Game_Tables'
#
#     def __str__(self):
#         return self.name
#
#
# # Waiting Room Model
# class WaitingRoom(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     game_table = models.ForeignKey('GameTable', on_delete=models.CASCADE)
#     player1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player1_waiting', on_delete=models.CASCADE)
#     player2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player2_waiting', null=True, blank=True, on_delete=models.SET_NULL)
#     created_time = models.DateTimeField(auto_now_add=True)
#     deadline = models.DateTimeField()  # 2-minute deadline
#
#     class Meta:
#         db_table = 'waiting_rooms'
#         verbose_name = 'waiting_room'
#         verbose_name_plural = 'Waiting_Rooms'
#
#     def is_full(self):
#         return self.player2 is not None
#
#
# # Game Room Model
# class GameRoom(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     waiting_room = models.OneToOneField(WaitingRoom, on_delete=models.CASCADE)
#     player_white = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player_white', on_delete=models.CASCADE)
#     player_black = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='player_black', on_delete=models.CASCADE)
#     current_turn = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='current_turn', null=True, blank=True, on_delete=models.SET_NULL)
#     created_time = models.DateTimeField(auto_now_add=True)
#     board_state = models.JSONField(default=dict)  # Initial board state placeholder
#
#     class Meta:
#         db_table = 'game_rooms'
#         verbose_name = 'Game_Room'
#         verbose_name_plural = 'Game_Rooms'
#
#     def assign_colors(self):
#         if random.choice([True, False]):
#             self.player_white = self.waiting_room.player1
#             self.player_black = self.waiting_room.player2
#         else:
#             self.player_white = self.waiting_room.player2
#             self.player_black = self.waiting_room.player1
#
#     def set_turn(self):
#         # Dice roll for turn
#         player1_roll = random.randint(1, 6)
#         player2_roll = random.randint(1, 6)
#         while player1_roll == player2_roll:
#             player1_roll = random.randint(1, 6)
#             player2_roll = random.randint(1, 6)
#
#         if player1_roll > player2_roll:
#             self.current_turn = self.player_white
#         else:
#             self.current_turn = self.player_black
#
#
# # Dice Roll Model
# class DiceRoll(models.Model):
#     game_room = models.ForeignKey(GameRoom, on_delete=models.CASCADE)
#     player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     dice1 = models.PositiveIntegerField()
#     dice2 = models.PositiveIntegerField()
#     created_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'dice_roll'
#         verbose_name = 'Dice_Roll'
#         verbose_name_plural = 'Dice_Rolls'
#
#     def roll(self):
#         self.dice1 = random.randint(1, 6)
#         self.dice2 = random.randint(1, 6)
#
#
# # Board Moves (Basic Structure)
# class BoardMove(models.Model):
#     game_room = models.ForeignKey(GameRoom, on_delete=models.CASCADE)
#     player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     move_data = models.JSONField()  # Placeholder for moves (later can be detailed)
#     created_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'board_moves'
#         verbose_name = 'Board_Move'
#         verbose_name_plural = 'Board_Moves'