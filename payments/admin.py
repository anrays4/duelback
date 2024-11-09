from django.contrib import admin

from .models import Withdraw, Deposit


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'crypto_name', 'amount_game_token', 'status', 'created_time')
    search_fields = ('user__username', 'crypto_name')
    ordering = ('-created_time',)


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'crypto_name', 'amount_game_token', 'status', 'created_time')
    search_fields = ('user__username', 'crypto_name')
    ordering = ('-created_time',)
