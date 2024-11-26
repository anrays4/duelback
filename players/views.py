from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.views import calculate_level
from .models import User, Referral, GameHistory, TakeReferralsProfitHistory
from .serializers import UserSerializer, ReferralSerializer, GameHistorySerializer
from takhte_nard.settings import TELEGRAM_BOT_ID
import requests
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from home.validate_init_data import validate_init_data
from django.contrib.auth.decorators import login_required


@login_required
def profile_page(request):
    my_user = get_object_or_404(User, username=request.user)
    back_game = GameHistory.objects.filter(user1=my_user).reverse()
    total_back_matches = back_game.count()

    current_lvl = calculate_level(my_user.level_xp)
    next_lvl = current_lvl + 1
    my_user.level = current_lvl
    my_user.save()

    pool_lvl = current_lvl * 1000
    pool_fill = my_user.level_xp
    for i in range(current_lvl):
        x = i
        pool_fill -= (x * 1000)
    bar_percent = int((pool_fill * 100) / pool_lvl)

    context = {
        "back_game_history": back_game,
        "total_back_matches": total_back_matches,
        "total_back_wins": my_user.backgammon_game_wins,
        "current_lvl": current_lvl,
        "next_lvl": next_lvl,
        "pool_lvl": pool_lvl,
        "pool_fill": pool_fill,
        "bar_percent": bar_percent
    }
    return render(request, "profile_page.html", context=context)


@login_required
def referral_page(request):
    my_user = get_object_or_404(User, username=request.user)
    referrals = Referral.objects.filter(inviter=my_user)
    referral_link = f"https://t.me/{TELEGRAM_BOT_ID}?start={my_user.referral_code}"

    if request.method == "POST" and my_user.referral_profit > 0:
        TakeReferralsProfitHistory.objects.create(for_user=my_user, amount=my_user.referral_profit)
        reward = my_user.referral_profit
        my_user.game_token += reward
        my_user.referral_profit = 0
        my_user.save()

    my_claim_history = TakeReferralsProfitHistory.objects.filter(for_user=my_user)

    context = {
        "my_user": my_user,
        'referrals': referrals,
        'referral_count': referrals.count(),
        'ref_link': referral_link,
        'claim_history': my_claim_history,
    }
    return render(request, 'referral_page.html', context=context)


class LoginPlayer(APIView):
    def post(self, request):
        init_data = request.POST['init_data']
        is_valid, user_data = validate_init_data(init_data)
        if is_valid:
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "no"}, status=status.HTTP_403_FORBIDDEN)


class RegisterPlayer(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            username = request.data.get('username')
            avatar = request.data.get('avatar')
            referral_code = request.data.get('ref_code')

            if len(username) == 0:
                username = user_id

            if len(avatar) < 5:
                avatar_default = True
            else:
                avatar_default = False

            try:
                user = User.objects.get(user_id=user_id)
                return Response({'status': 'you_already_signed_up'}, status=status.HTTP_200_OK)
            except:
                invited = User.objects.create(user_id=user_id, username=username, password=user_id)
                if not avatar_default:
                    response = requests.get(avatar)
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()

                    invited.avatar.save(f"{user_id}.jpg", File(img_temp))
                    invited.save()

                if referral_code == "":
                    return Response({'status': 'you_signed_up'}, status=status.HTTP_200_OK)
                else:
                    try:
                        inviter = User.objects.get(referral_code=referral_code)
                        Referral.objects.create(inviter=inviter, invited_user=invited)
                        return Response({'status': f'you_signed_up_and_ref_of_{inviter}'}, status=status.HTTP_200_OK)
                    except:
                        return Response({'status': 'referral_code_is_invalid'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'status': 'args not valid'}, status=status.HTTP_400_BAD_REQUEST)


class ResetBackgammonRank(APIView):
    def post(self, request):
        if request.POST["password"] == "Arya_13811218":
            all_players = User.objects.all()
            top_players = all_players.order_by("backgammon_game_wins").reverse()
            serializer = UserSerializer(top_players, many=True)
            old_data = serializer.data
            for player in all_players:
                player.backgammon_game_wins = 0
                player.save()

            return Response(old_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# ویو برای User
class UserAPIView(APIView):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
            serializer = UserSerializer(user)

        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ویو برای Referral
class ReferralAPIView(APIView):
    def get(self, request):
        referrals = Referral.objects.all()
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReferralSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ویو برای GameHistory
class GameHistoryAPIView(APIView):
    def get(self, request):
        game_histories = GameHistory.objects.all()
        serializer = GameHistorySerializer(game_histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GameHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
