from django.db import models
from django.conf import settings
from django.utils import timezone
import time
from datetime import timedelta
import uuid


class GameTable(models.Model):
    name = models.CharField(max_length=255)
    fee = models.IntegerField()
    image = models.ImageField(upload_to="table_images/")
    xp_for_winner = models.IntegerField()
    xp_for_loser = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    percent_for_winner = models.IntegerField(default=90)
    percent_for_left_user_winner = models.IntegerField(default=70)

    class Meta:
        verbose_name = "Game_Table"
        verbose_name_plural = "Game_Tables"

    def get_winner_prize(self):
        prize = (2 * self.fee) * (self.percent_for_winner / 100)
        return prize

    def get_winner_prize_user_left_the_game(self):
        prize = (2 * self.fee) * (self.percent_for_left_user_winner / 100)
        return prize

    def __str__(self):
        return self.name


class WaitingRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_table = models.ForeignKey(GameTable, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player1_waiting", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now() + timedelta(minutes=2))  # 2-minute deadline

    class Meta:
        db_table = "waiting_rooms"
        verbose_name = "Waiting_Room"
        verbose_name_plural = "Waiting_Rooms"

    def is_expired(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return f"WaitingRoom for {self.game_table.name} (Player1: {self.player_1.username})"


def get_default_board_state():
    board_state = {"p1": [1, 1], "p2": [], "p3": [], "p4": [], "p5": [], "p6": [2, 2, 2, 2, 2], "p7": [],
                   "p8": [2, 2, 2], "p9": [], "p10": [], "p11": [], "p12": [1, 1, 1, 1, 1], "p13": [2, 2, 2, 2, 2],
                   "p14": [], "p15": [], "p16": [], "p17": [1, 1, 1], "p18": [], "p19": [1, 1, 1, 1, 1], "p20": [],
                   "p21": [], "p22": [], "p23": [], "p24": [2, 2]}
    return board_state


def calculate_turn_polling_time(game_rome_count):
    poll_time = game_rome_count / 20
    if poll_time >= 5:
        poll_time = 5
    if poll_time <= 1:
        poll_time = 1
    return poll_time


class GameRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(GameTable, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="game_player_1", on_delete=models.CASCADE)
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="game_player_2", on_delete=models.CASCADE)
    is_ready1 = models.BooleanField(default=False)
    is_ready2 = models.BooleanField(default=False)
    dice1 = models.IntegerField(blank=True, null=True)  # مقدار تاس اول
    dice2 = models.IntegerField(blank=True, null=True)  # مقدار تاس دوم
    current_turn = models.IntegerField(null=True, blank=True)
    turn_tas_player_1 = models.IntegerField(null=True, blank=True)
    turn_tas_player_2 = models.IntegerField(null=True, blank=True)
    time_player_1 = models.IntegerField(default=int(time.time()), null=True, blank=True)
    time_player_2 = models.IntegerField(default=int(time.time()), null=True, blank=True)
    move_history = models.JSONField(default=dict, null=True, blank=True)
    place_status = models.JSONField(default=get_default_board_state, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    game_is_started = models.BooleanField(default=False)
    game_room_is_end = models.BooleanField(default=False)

    is_player_1_win = models.BooleanField(default=False)
    is_player_2_win = models.BooleanField(default=False)

    is_player_1_offline = models.BooleanField(default=False)
    is_player_2_offline = models.BooleanField(default=False)

    game_polling_time = models.FloatField(default=1, null=True, blank=True)
    game_turn_time = models.FloatField(default=45, null=True, blank=True)
    game_start_time = models.IntegerField(default=int(time.time()), null=True, blank=True)

    class Meta:
        db_table = "game_rooms"
        verbose_name = "Game_Room"
        verbose_name_plural = "Game_Rooms"

    def iam_lose_the_game(self, loser):
        if loser == self.player_1:
            self.is_player_1_offline = True
            self.is_player_2_win = True
            loser.create_lose_game_history(winner=self.player_2, game_table=self.table)
        else:
            self.is_player_2_offline = True
            self.is_player_1_win = True
            loser.create_lose_game_history(winner=self.player_1, game_table=self.table)

        loser.level_xp += self.table.xp_for_loser
        loser.save()
        self.save()

    def iam_win_the_game(self, winner, prize):
        if winner == self.player_1:
            self.is_player_1_win = True
            winner.create_win_game_history(loser=self.player_2, game_table=self.table)
        else:
            self.is_player_2_win = True
            winner.create_win_game_history(loser=self.player_1, game_table=self.table)

        winner.level_xp += self.table.xp_for_winner
        winner.game_token += prize
        winner.backgammon_game_wins += 1
        winner.save()
        self.save()

    def check_time_is_ok(self, user):
        if user == self.player_1:
            time_dif = int(time.time()) - self.time_player_1
            if time_dif >= 47:
                return False
            else:
                return True
        else:
            time_dif = int(time.time()) - self.time_player_2
            if time_dif >= 47:
                return False
            else:
                return True

    def get_enemy_user_qs(self, my_user):
        if self.player_1 == my_user:
            return self.player_2
        else:
            return self.player_1

    def get_player_turn_number(self, user):
        if user == self.player_1:
            return 1
        elif user == self.player_2:
            return 2
        else:
            return 0

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
            self.current_turn = 1
        elif self.dice2 > self.dice1:
            self.current_turn = 2
        else:
            self.roll_dice()
            self.set_turn()
        self.turn_tas_player_1 = self.dice1
        self.turn_tas_player_2 = self.dice2
        self.save()

    def switch_turn(self):
        """تغییر نوبت بین پلیر 1 و پلیر 2"""
        self.current_turn = 2 if self.current_turn == 1 else 1
        self.save()

    def update_board_state(self, new_state):
        """به‌روزرسانی وضعیت تخته"""
        self.place_status = new_state
        self.save()

    def __str__(self):
        return f"{self.player_1.username} VS {self.player_2.username}"


class PlayerWarning(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()

    class Meta:
        db_table = "player_warnings"
        verbose_name = "Player_Warning_backgammon"
        verbose_name_plural = "Player_Warnings_backgammon"
