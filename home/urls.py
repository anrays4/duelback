from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from takhte_nard import settings
from django.conf.urls.static import static
from home.views import home_page, sidebar, top_bar, enter_name_page

urlpatterns = [
    path('', home_page, name="home_page"),
    path('enter-name/', enter_name_page, name="enter_name_page"),
    path('footer', sidebar, name='sidebar'),
    path('topbar', top_bar, name='topbar'),
]
