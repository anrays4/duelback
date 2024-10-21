from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from takhte_nard import settings
from django.conf.urls.static import static
from home.views import home_page, sidebar, game_page

urlpatterns = [
    path('game/', game_page),

    path('admin', admin.site.urls),

    path('', home_page, name="home_page"),
    path('footer', sidebar, name='sidebar'),
]
