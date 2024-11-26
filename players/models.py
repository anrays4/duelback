import time
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
import random
import string
from back_game.models import GameTable
import os


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


def get_filename_deposit(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def profile_images(instance, filename):
    name, ext = get_filename_deposit(filename)
    random_id = random.randint(1, 100000)
    final_name = f'{random_id}-{instance}'
    return f"profile_pic/{final_name}"


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(verbose_name="username", max_length=150, unique=True)
    password = models.CharField(verbose_name="password", max_length=128)
    user_id = models.CharField(verbose_name="Tel_ID", max_length=128, unique=True)
    name = models.CharField(verbose_name="name", max_length=100, blank=True, null=True)
    avatar = models.ImageField(default="profile-default.jpg", upload_to=profile_images, blank=True, null=True)
    level = models.IntegerField(verbose_name="level", default=1)
    level_xp = models.IntegerField(verbose_name="level xp", default=0)
    game_token = models.FloatField(verbose_name="game token", default=0)  # مقدار ثابت اولیه توکن
    referral_code = models.CharField(verbose_name="referral code", max_length=10, unique=True, blank=True)
    referral_profit = models.FloatField(verbose_name="referral profit token", default=0)

    is_staff = models.BooleanField(verbose_name='staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(verbose_name='active', default=True,
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_seen = models.DateTimeField(verbose_name='last seen date', null=True)

    backgammon_game_wins = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # فیلدی که برای ورود استفاده می‌شود
    REQUIRED_FIELDS = []  # فیلدهای دیگری که هنگام ساخت سوپر یوزر نیاز است

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def create_lose_game_history(self, winner, game_table):
        GameHistory.objects.create(user1=self, user2=winner, status="lose", table=game_table)

        if Referral.objects.filter(invited_user=self).exists():
            my_inviter = Referral.objects.get(invited_user=self).inviter
            my_inviter.referral_profit += game_table.fee * (1 / 100)
            my_inviter.save()

    def create_win_game_history(self, loser, game_table):
        GameHistory.objects.create(user1=self, user2=loser, status="win", table=game_table)

        if Referral.objects.filter(invited_user=self).exists():
            my_inviter = Referral.objects.get(invited_user=self).inviter
            my_inviter.referral_profit += game_table.fee * (1 / 100)
            my_inviter.save()

    def decrease_my_token(self, fee):
        self.game_token -= fee
        self.save()

    def deposit_token(self, amount):
        self.game_token += amount
        self.save()

    def deposit_token_offer(self, amount, offer):
        new_amount = amount + (amount*offer/100)
        self.game_token += new_amount
        self.save()

    def get_rank(self):
        # تعداد مواردی را که امتیاز بیشتری دارند دریافت می کند
        higher_ranking = User.objects.filter(backgammon_game_wins__gt=self.backgammon_game_wins).count()
        # رتبه فعلی برابر با تعداد آیتم‌های با رتبه بالاتر + 1
        return higher_ranking + 1

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # ساختن referral_code به صورت یونیک رندوم در اولین ذخیره
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()

        super().save(*args, **kwargs)

    def generate_unique_referral_code(self):
        # تولید کد یونیک رندوم 10 کاراکتری
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not User.objects.filter(referral_code=code).exists():
                return code


class Referral(models.Model):
    inviter = models.ForeignKey(User, related_name='referrals_sent', on_delete=models.CASCADE)
    invited_user = models.OneToOneField(User, related_name='invited_by', on_delete=models.CASCADE)
    invited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'referrals'
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'

    def __str__(self):
        return f"{self.invited_user} invited by {self.inviter} on {self.invited_at}"

    def get_invited_user_level(self):
        return self.invited_user.level


class GameHistory(models.Model):
    STATUS_CHOICES = (
        ('win', 'Win'),
        ('lose', 'Lose'),
    )

    user1 = models.ForeignKey(User, related_name='games_as_user1', on_delete=models.CASCADE)  # بازیکن اصلی
    user2 = models.ForeignKey(User, related_name='games_as_user2', on_delete=models.CASCADE)  # حریف
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)  # وضعیت بازی (Win یا Lose)
    table = models.ForeignKey(GameTable, on_delete=models.CASCADE)  # لینک به یکی از objectهای GameTable
    created_time = models.DateTimeField(auto_now_add=True)  # زمان اتمام بازی

    class Meta:
        db_table = "game_history's"
        verbose_name = 'Game_History'
        verbose_name_plural = "Game_History's"

    def __str__(self):
        return f"Game between {self.user1.name} and {self.user2.name} on {self.table.name}"


class TakeReferralsProfitHistory(models.Model):
    for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    claim_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.for_user.username


class LoginCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(default=random.randint(111111, 999999), max_length=20)
    time_st = models.CharField(default=int(time.time()), max_length=120)

    def __str__(self):
        return self.user.username
