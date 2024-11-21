from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from about.views import about_page
from home.views import sign_in_page, login_windows_page, LoginCodeCreate, VerifyLoginCode, log_out
from players.views import RegisterPlayer, LoginPlayer

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('', login_windows_page, name="login_window"),
    path('login-with-user-id', LoginCodeCreate.as_view(), name="login_code_api"),
    path('login-with-user-id-verify', VerifyLoginCode.as_view(), name="login_code_api"),
    path('log-out', log_out, name="log_out"),

    path('contact-us/', about_page, name="about_page"),
    path('<init_data>', sign_in_page, name="sign_in_page"),

    path('register/player', RegisterPlayer.as_view(), name="register_api"),
    path('login/player', LoginPlayer.as_view(), name="login_api"),

    path('admin/aliarya/duelback', admin.site.urls),

    # URLs برای اپ players
    path('users/', include('players.urls')),

    # URLs برای اپ back_game
    path('backgammon/', include('back_game.urls')),

    # URLs برای اپ home
    path('home/', include('home.urls')),

    path('payments/', include('payments.urls')),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
