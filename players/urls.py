from django.urls import path

from .views import UserAPIView, ReferralAPIView, GameHistoryAPIView


urlpatterns = [
    # URLs برای User
    path('', UserAPIView.as_view(), name='user-list'),
    path('<str:username>/', UserAPIView.as_view(), name='user-detail'),

    # URLs برای Referral
    path('referrals/', ReferralAPIView.as_view(), name='referral-list'),

    # URLs برای GameHistory
    path('gamehistories/', GameHistoryAPIView.as_view(), name='gamehistory-list')
]