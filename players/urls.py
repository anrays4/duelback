from django.urls import path

from .views import UserAPIView, ReferralAPIView, GameHistoryAPIView, profile_page, referral_page

urlpatterns = [
    # URLs برای User
    path('', UserAPIView.as_view(), name='user-list'),
    path('referrals/', referral_page, name="referral_page"),

    # URLs برای GameHistory
    path('gamehistories/', GameHistoryAPIView.as_view(), name='gamehistory-list'),

    path('profile/', profile_page, name="profile_page")
]
