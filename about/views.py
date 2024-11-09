from django.shortcuts import render
from .models import SocialForWebsite


def about_page(request):
    all_social_media = SocialForWebsite.objects.all()
    context = {
        "socials": all_social_media,
    }
    return render(request, "about_page.html", context)


