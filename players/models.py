from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import random
import string

from back_game.models import GameTable


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=150, unique=True)
    password = models.CharField(verbose_name="password", max_length=128)
    name = models.CharField(verbose_name="name", max_length=100, blank=True, null=True)
    avatar = models.URLField(verbose_name="avatar", blank=True, null=True, default="default_avatar_url")  # URL پیش‌فرض برای آواتار دیفالت
    level = models.IntegerField(verbose_name="level", default=1)
    level_xp = models.IntegerField(verbose_name="level xp", default=0)
    game_token = models.IntegerField(verbose_name="game token", default=0)  # مقدار ثابت اولیه توکن
    referral_code = models.CharField(verbose_name="referral code", max_length=10, unique=True, blank=True)

    is_staff = models.BooleanField(verbose_name='staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(verbose_name='active', default=True,
                                    help_text='Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    last_seen = models.DateTimeField(verbose_name='last seen date', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # فیلدی که برای ورود استفاده می‌شود
    REQUIRED_FIELDS = []  # فیلدهای دیگری که هنگام ساخت سوپر یوزر نیاز است

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # ساختن referral_code به صورت یونیک رندوم در اولین ذخیره
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()

        # به روزرسانی level بر اساس level_xp
        self.level = (self.level_xp // 1000) + 1

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