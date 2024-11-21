from django.shortcuts import render, redirect
from players.models import User, LoginCode
from django.shortcuts import get_object_or_404
from back_game.models import WaitingRoom, GameRoom
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from takhte_nard.settings import TELEGRAM_BOT_ID, TELEGRAM_BOT_TOKEN
import time


def calculate_level(level_xp):
    level = 1
    xp_threshold = 1000  # شروع از لول 2
    while level_xp >= xp_threshold:
        level += 1
        xp_threshold += 1000 * level
    return level


def sign_in_page(request, init_data):
    try:
        telegram_user_id = str(init_data)
        user = User.objects.get(password=telegram_user_id)
        login(request, user)
        return redirect("home_page")
    except:
        pass
    return render(request, "sign_in_page.html", context={})


@login_required
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

@login_required
def enter_name_page(request):
    my_user = get_object_or_404(User, username=request.user)
    if my_user.name is not None:
        return redirect("home_page")

    if request.method == "POST":
        nickname = request.POST["name"]
        if 4 <= len(nickname) <= 12:
            my_user.name = nickname
            my_user.save()
            return redirect("home_page")

    return render(request, "enter_name_page.html", context={})


def login_windows_page(request):
    if not "Window" in request.headers["User-Agent"]:
        return redirect("sign_in_page")

    if request.user.is_authenticated:
        return redirect("home_page")

    telegram_bot = f"https://t.me/{TELEGRAM_BOT_ID}"

    context = {
        "telegram_bot": telegram_bot,
    }
    return render(request, "login_windows.html", context)


class LoginCodeCreate(APIView):
    def post(self, request):
        user_id = request.POST["user_id"]
        try:
            user = User.objects.get(user_id=user_id)
        except:
            return Response({"status": "need_sign_up"}, status=status.HTTP_200_OK)
        if not LoginCode.objects.filter(user=user).exists():
            import telebot
            try:
                code = LoginCode.objects.create(user=user)
                bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

                bot.send_message(str(user_id), f"Login Code is {code.code}")

                return Response({"status": "code_is_ready"}, status=status.HTTP_200_OK)
            except:
                code.delete()
                return Response({"status": "need_sign_up"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "code_is_ready"}, status=status.HTTP_200_OK)


class VerifyLoginCode(APIView):
    def post(self, request):
        user_id = request.POST["user_id"]
        code = request.POST["code"]
        try:
            user = User.objects.get(user_id=user_id)
        except:
            return Response({"status": "user_not_exist"}, status=status.HTTP_200_OK)
        if LoginCode.objects.filter(user=user).exists():
            main_code = LoginCode.objects.get(user=user)
            if time.time() - int(main_code.time_st) >= 120:
                main_code.delete()
                return Response({"status": "user_not_exist"}, status=status.HTTP_200_OK)

            if main_code.code == code:
                login(request, user)
                main_code.delete()
                return Response({"status": "code_is_true"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "code_is_wrong"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "user_not_exist"}, status=status.HTTP_200_OK)


def sidebar(request):
    return render(request, "sidebar.html", context={})


def top_bar(request):
    my_user = get_object_or_404(User, username=request.user)
    context = {
        "my_user": my_user,
    }
    return render(request, "top-bar.html", context)


def log_out(request):
    logout(request)
    return redirect("login_window")
