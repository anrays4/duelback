from django.contrib import admin

from .models import User, Referral, GameHistory


# ثبت مدل User در پنل ادمین
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'level', 'game_token', 'referral_code')
    search_fields = ('username', 'name', 'referral_code')
    list_filter = ('level',)
    ordering = ('-level',)


# ثبت مدل Referral در پنل ادمین
@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invited_user', 'invited_at')
    search_fields = ('inviter__username', 'invited_user__username')
    list_filter = ('invited_at',)
    ordering = ('-invited_at',)


# ثبت مدل GameHistory در پنل ادمین
@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'status', 'table', 'created_time')
    search_fields = ('user1__username', 'user2__username', 'table__name')
    list_filter = ('status', 'created_time')
    ordering = ('-created_time',)
