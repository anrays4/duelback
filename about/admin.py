from django.contrib import admin
from .models import SocialForWebsite


# Register your models here.

@admin.register(SocialForWebsite)
class SocialForWebsiteAdmin(admin.ModelAdmin):
    list_display = ('social_name', 'link')
