from rest_framework import serializers

from .models import User, Referral, GameHistory


# سریالایزر برای مدل User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'user_id', 'level', 'backgammon_game_wins']


# سریالایزر برای مدل Referral
class ReferralSerializer(serializers.ModelSerializer):
    inviter = serializers.StringRelatedField()  # نمایش اطلاعات دعوت‌کننده
    invited = serializers.StringRelatedField()  # نمایش اطلاعات دعوت‌شده

    class Meta:
        model = Referral
        fields = ['inviter', 'invited', 'created_time']


# سریالایزر برای مدل GameHistory
class GameHistorySerializer(serializers.ModelSerializer):
    user1 = serializers.StringRelatedField()  # نمایش اطلاعات بازیکن اصلی
    user2 = serializers.StringRelatedField()  # نمایش اطلاعات حریف
    table = serializers.StringRelatedField()  # نمایش اطلاعات میز بازی

    class Meta:
        model = GameHistory
        fields = ['user1', 'user2', 'status', 'table', 'created_time']
