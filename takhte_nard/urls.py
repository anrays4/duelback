"""
URL configuration for takhte_nard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from about.views import about_page
from home.views import sign_in_page
from players.views import RegisterPlayer

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('contact-us/', about_page, name="about_page"),
    path('<init_data>', sign_in_page, name="sign_in_page"),

    path('register/player', RegisterPlayer.as_view(), name="register_api"),

    path('admin/', admin.site.urls),

    # URLs برای اپ players
    path('users/', include('players.urls')),

    # URLs برای اپ back_game
    path('backgammon/', include('back_game.urls')),

    # URLs برای اپ home
    path('home/', include('home.urls')),

    path('payments/', include('payments.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
