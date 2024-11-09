from django.shortcuts import render, redirect
from players.models import User
from django.shortcuts import get_object_or_404
from back_game.models import WaitingRoom, GameRoom
from .validate_init_data import validate_init_data
from django.contrib.auth import login


def calculate_level(level_xp):
    level = 1
    xp_threshold = 1000  # شروع از لول 2
    while level_xp >= xp_threshold:
        level += 1
        xp_threshold += 1000 * level
    return level


def sign_in_page(request, init_data):
    try:
        is_valid, user_data = validate_init_data(init_data)
        if is_valid:
            telegram_user_id = str(user_data['id'])
            user = User.objects.get(password=telegram_user_id)
            login(request, user)
            return redirect("home_page")
    except:
        pass
    return render(request, "sign_in_page.html", context={})


def home_page(request):
    my_user = get_object_or_404(User, username=request.user)
    WaitingRoom.objects.filter(player_1=my_user).delete()
    my_user.level = calculate_level(my_user.level_xp)
    my_user.save()

    all_game_count = GameRoom.objects.all().count()

    if my_user.name is None:
        return redirect("enter_name_page")

    context = {
        "total_backgammon_game": all_game_count * 2,
    }
    return render(request, "home_page.html", context)


def enter_name_page(request):
    my_user = get_object_or_404(User, username=request.user)
    if my_user.name is not None:
        return redirect("home_page")

    if request.method == "POST":
        nickname = request.POST["name"]
        if len(nickname) >= 4 and len(nickname) <= 12:
            my_user.name = nickname
            my_user.save()
            return redirect("home_page")

    return render(request, "enter_name_page.html", context={})


def sidebar(request):
    return render(request, "sidebar.html", context={})


def top_bar(request):
    my_user = get_object_or_404(User, username=request.user)
    context = {
        "my_user": my_user,
    }
    return render(request, "top-bar.html", context)
