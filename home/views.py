from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, "home_page.html", context={})


def sidebar(request):
    return render(request, "sidebar.html", context={})