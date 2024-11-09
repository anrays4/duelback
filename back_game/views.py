from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
import json
import time
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from players.models import User, GameHistory
from .models import GameTable, WaitingRoom, GameRoom, PlayerWarning
from back_game.validator import validate_moves, win_check
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def find_match_page(request, table_id):
    my_user = get_object_or_404(User, username=request.user)
    qs_table = get_object_or_404(GameTable, id=table_id)

    if my_user.game_token < qs_table.fee:
        return redirect("game_table_page")

    GameRoom.objects.filter(is_player_1_offline=True, is_player_2_offline=True).delete()

    GameRoom.objects.filter(player_1=my_user, game_room_is_end=True).delete()
    GameRoom.objects.filter(player_2=my_user, game_room_is_end=True).delete()

    WaitingRoom.objects.filter(player_1=my_user).delete()
    WaitingRoom.objects.create(game_table=qs_table, player_1=my_user)

    for game in GameRoom.objects.filter(player_1=my_user):
        game.is_player_1_offline = True
        game.save()

    for game in GameRoom.objects.filter(player_2=my_user):
        game.is_player_2_offline = True
        game.save()

    context = {
        "table": qs_table,
        "my_user": my_user,
        "req_polling_time": random.randint(2, 6),
    }
    return render(request, "find_match.html", context)


class FindMatch(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_user = get_object_or_404(User, username=request.user)

        if WaitingRoom.objects.filter(player_1=my_user).exists() and not (
                GameRoom.objects.filter(player_1=my_user, game_room_is_end=False, is_ready1=False,
                                        is_ready2=False).exists()
                or GameRoom.objects.filter(player_2=my_user, game_room_is_end=False, is_ready1=False,
                                           is_ready2=False).exists()):

            wait_room = WaitingRoom.objects.get(player_1=my_user)
            table = wait_room.game_table
            if WaitingRoom.objects.filter(game_table=table).count() > 1:
                all_game_rome = GameRoom.objects.all().count()

                if all_game_rome < 25:
                    poll_time = 5
                elif all_game_rome >= 25:
                    poll_time = 7

                wait_room.delete()
                wait_room_player_2 = WaitingRoom.objects.filter(game_table=table).first()
                player_2 = get_object_or_404(User, username=wait_room_player_2.player_1)
                game_room = GameRoom.objects.create(table=table, player_1=my_user,
                                                    player_2=player_2,
                                                    game_polling_time=poll_time, game_start_time=int(time.time()))
                enemy_name = player_2.name
                enemy_avatar = player_2.avatar
                enemy_level = player_2.level
                wait_room_player_2.delete()
                res = {"status": "go_to_play", "game_room_id": game_room.id, "enemy_name": enemy_name,
                       "enemy_avatar": enemy_avatar, "enemy_level": enemy_level}

                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response({"status": "wait_more"}, status=status.HTTP_200_OK)
        else:
            if GameRoom.objects.filter(player_1=my_user, game_room_is_end=False).exists():
                game_room = GameRoom.objects.get(player_1=my_user)
                game_rome_id = game_room.id
                enemy_name = game_room.player_2.name
                enemy_avatar = game_room.player_2.avatar
                enemy_level = game_room.player_2.level
                res = {"status": "your_match_ready", "game_room_id": game_rome_id, "enemy_name": enemy_name,
                       "enemy_avatar": enemy_avatar, "enemy_level": enemy_level}
                return Response(res, status=status.HTTP_200_OK)

            elif GameRoom.objects.filter(player_2=my_user, game_room_is_end=False).exists():
                game_room = GameRoom.objects.get(player_2=my_user)
                game_rome_id = game_room.id
                enemy_name = game_room.player_1.name
                enemy_avatar = game_room.player_1.avatar
                enemy_level = game_room.player_1.level
                res = {"status": "your_match_ready", "game_room_id": game_rome_id, "enemy_name": enemy_name,
                       "enemy_avatar": enemy_avatar, "enemy_level": enemy_level}
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response({"status": "wait_more"}, status=status.HTTP_200_OK)


class CancelFindMatch(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_user = get_object_or_404(User, username=request.user)

        WaitingRoom.objects.filter(player_1=my_user).delete()
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


def playing_game_page(request, game_room_id):
    if not request.user.is_authenticated:
        return redirect("home_page")

    qs_game_room = get_object_or_404(GameRoom, id=game_room_id)
    my_user = get_object_or_404(User, username=request.user)
    enemy_user = get_object_or_404(User, username=qs_game_room.get_enemy_user_qs(my_user))

    my_game_history_matches = GameHistory.objects.filter(user1=my_user).count()
    my_game_history_wins = GameHistory.objects.filter(user1=my_user, status="win").count()
    enemy_game_history_matches = GameHistory.objects.filter(user1=enemy_user).count()
    enemy_game_history_wins = GameHistory.objects.filter(user1=enemy_user, status="win").count()

    if qs_game_room.game_is_started:
        qs_game_room.iam_lose_the_game(loser=my_user)
        qs_game_room.save()
        return redirect("home_page")

    context = {
        "game_room_id": game_room_id,
        "game_room": qs_game_room,
        "my_user": my_user,
        "enemy_user": enemy_user,
        "enemy_matches": enemy_game_history_matches,
        "enemy_wins": enemy_game_history_wins,
        "my_matches": my_game_history_matches,
        "my_wins": my_game_history_wins,
        "turn_time": qs_game_room.game_turn_time,
    }
    return render(request, "playing_game.html", context=context)


def game_table_page(request):
    game_tables = GameTable.objects.all().order_by("fee")
    my_user = get_object_or_404(User, username=request.user)

    WaitingRoom.objects.filter(player_1=my_user).delete()

    context = {
        'game_tables': game_tables,
        "my_user": my_user,
    }
    return render(request, 'game_tables.html', context)


def backgammon_leaderboard(request):
    top_back_players = User.objects.order_by("backgammon_game_wins").reverse()

    context = {'top_player': top_back_players}
    return render(request, 'leaderboard.html', context)


class PlayerReadyAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        player = request.user
        my_user = get_object_or_404(User, username=request.user)
        try:
            # آماده شدن بازیکن
            game_room.mark_ready(player)
        except:
            return Response({"status": 'you are not in this room'}, status=status.HTTP_400_BAD_REQUEST)

        delta_time = int(time.time()) - int(game_room.game_start_time)
        if delta_time > 45:
            game_room.delete()
            return Response({"status": "game_cancel"}, status=status.HTTP_200_OK)

        # چک کردن وضعیت آماده بودن هر دو بازیکن
        if game_room.has_both_ready() and not game_room.game_is_started:
            my_user.decrease_my_token(game_room.table.fee)
            game_room.get_enemy_user_qs(my_user).decrease_my_token(game_room.table.fee)
            game_room.roll_dice()
            game_room.set_turn()
            game_room.roll_dice()
            game_room.game_is_started = True
            game_room.time_player_1 = int(time.time())
            game_room.time_player_2 = int(time.time())
            game_room.save()
            return Response({
                "status": "start_game",
                "my_turn_num": game_room.get_player_turn_number(player),
                "turn": game_room.current_turn,
                "turn_tas_player_1": game_room.turn_tas_player_1,
                "turn_tas_player_2": game_room.turn_tas_player_2,
                "main_tas_1": game_room.dice1,
                "main_tas_2": game_room.dice2,
                "waiting_poll_time": game_room.game_polling_time,
            }, status=status.HTTP_200_OK)
        elif game_room.game_is_started:
            return Response({
                "status": "start_game",
                "my_turn_num": game_room.get_player_turn_number(player),
                "turn": game_room.current_turn,
                "turn_tas_player_1": game_room.turn_tas_player_1,
                "turn_tas_player_2": game_room.turn_tas_player_2,
                "main_tas_1": game_room.dice1,
                "main_tas_2": game_room.dice2,
                "waiting_poll_time": game_room.game_polling_time,
            }, status=status.HTTP_200_OK)
        return Response({"status": "please_wait"}, status=status.HTTP_200_OK)


class PollingTurnAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        player = request.user
        my_turn_num = game_room.get_player_turn_number(player)

        if not game_room.is_player_1_win and not game_room.is_player_2_win and game_room.game_room_is_end:
            return Response({"status": "game_cancel"}, status=status.HTTP_200_OK)

        if my_turn_num == 1:
            if game_room.game_room_is_end and game_room.is_player_2_win:
                game_room.iam_lose_the_game(loser=game_room.player_1)
                game_room.delete()
                return Response({"status": "you_lose"}, status=status.HTTP_200_OK)

            if game_room.is_player_1_win and not game_room.game_room_is_end and not game_room.is_player_1_offline:
                game_room.iam_win_the_game(winner=game_room.player_1,
                                           prize=game_room.table.get_winner_prize_user_left_the_game())
                game_room.game_room_is_end = True
                game_room.save()
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)

            if game_room.is_player_1_win and game_room.game_room_is_end and not game_room.is_player_2_offline:
                game_room.iam_win_the_game(winner=game_room.player_1,
                                           prize=game_room.table.get_winner_prize_user_left_the_game())
                game_room.game_room_is_end = True
                game_room.save()
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)

            elif game_room.is_player_2_win and not game_room.is_player_1_offline:
                game_room.iam_lose_the_game(loser=game_room.player_1)
                return Response({"status": "you_lose"}, status=status.HTTP_200_OK)

        else:
            if game_room.game_room_is_end and game_room.is_player_1_win:
                game_room.iam_lose_the_game(loser=game_room.player_2)
                game_room.game_room_is_end = True
                game_room.save()
                return Response({"status": "you_lose"}, status=status.HTTP_200_OK)

            if game_room.is_player_1_win and not game_room.is_player_2_offline:
                game_room.iam_lose_the_game(loser=game_room.player_2)
                return Response({"status": "you_lose"}, status=status.HTTP_200_OK)

            if game_room.is_player_2_win and game_room.game_room_is_end and not game_room.is_player_1_offline:
                game_room.iam_win_the_game(winner=game_room.player_2,
                                           prize=game_room.table.get_winner_prize_user_left_the_game())
                game_room.game_room_is_end = True
                game_room.save()
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)

            elif game_room.is_player_2_win and not game_room.game_room_is_end and not game_room.is_player_2_offline:
                game_room.iam_win_the_game(winner=game_room.player_2,
                                           prize=game_room.table.get_winner_prize_user_left_the_game())
                game_room.game_room_is_end = True
                game_room.save()
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)

        if game_room.current_turn == my_turn_num:
            if my_turn_num == 1:
                game_room.time_player_1 = int(time.time())
            else:
                game_room.time_player_2 = int(time.time())
            game_room.save()
            return Response({
                "status": "you_can_play",
                "my_turn_num": game_room.get_player_turn_number(player),
                "turn": game_room.current_turn,
                "main_tas_1": game_room.dice1,
                "main_tas_2": game_room.dice2,
                "move_history": game_room.move_history,
                "place_status": {}
            }, status=status.HTTP_200_OK)

        return Response({"status": "wait_more"}, status=status.HTTP_200_OK)


# API تایید حرکت بازیکن و تغییر نوبت
class ConfirmMoveAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        player = request.user
        my_turn_num = game_room.get_player_turn_number(player)
        my_user = get_object_or_404(User, username=player)

        move_history = json.loads(request.data.get('move_history', {}))
        first_scan = json.loads(request.data.get('first_scan', {}))
        second_scan = json.loads(request.data.get('second_scan', {}))
        if game_room.current_turn != my_turn_num:
            PlayerWarning.objects.create(player=player, reason="i send request at not my turn",
                                         expiry_date=timezone.now())
            return Response({"error": "It's not your turn."}, status=status.HTTP_400_BAD_REQUEST)

        move_is_valid = validate_moves(game_room.dice1, game_room.dice2, move_history)
        if move_is_valid:
            if game_room.place_status == first_scan:
                time_is_ok = game_room.check_time_is_ok(player)
                if time_is_ok and not game_room.game_room_is_end:
                    if win_check(second_scan) == my_turn_num:
                        game_room.iam_win_the_game(winner=my_user, prize=game_room.table.get_winner_prize())

                        game_room.game_room_is_end = True
                        game_room.save()

                        return Response({"status": "you_win"}, status=status.HTTP_200_OK)

                    game_room.move_history = move_history
                    game_room.update_board_state(second_scan)

                    game_room.switch_turn()
                    game_room.roll_dice()

                    game_room.time_player_1 = int(time.time())
                    game_room.time_player_2 = int(time.time())

                    game_room.save()
                    return Response({
                        "status": "wait_for_turn",
                        "waiting_poll_time": game_room.game_polling_time,
                        "main_tas_1": game_room.dice1,
                        "main_tas_2": game_room.dice2,
                    }, status=status.HTTP_200_OK)
                elif time_is_ok and game_room.game_room_is_end:
                    game_room.iam_win_the_game(winner=my_user, prize=game_room.table.get_winner_prize())
                    return Response({
                        "status": "you_win",
                    }, status=status.HTTP_200_OK)
                elif not time_is_ok:
                    return Response({
                        "status": "you_lose",
                    }, status=status.HTTP_200_OK)
            else:
                my_user = get_object_or_404(User, username=player)
                enemy_user = get_object_or_404(User, username=game_room.get_enemy_user_qs(my_user))

                fee = game_room.table.fee
                my_user.game_token += fee
                enemy_user.game_token += fee
                game_room.game_room_is_end = True
                my_user.save()
                enemy_user.save()
                game_room.save()
                PlayerWarning.objects.create(player=game_room.player_1, reason="this game changed place scans",
                                             expiry_date=timezone.now())
                PlayerWarning.objects.create(player=game_room.player_2, reason="this game changed place scans",
                                             expiry_date=timezone.now())
                return Response({
                    "status": "game_cancel",
                }, status=status.HTTP_200_OK)
        else:
            my_user = get_object_or_404(User, username=player)
            enemy_user = get_object_or_404(User, username=game_room.get_enemy_user_qs(my_user))

            fee = game_room.table.fee
            my_user.game_token += fee
            enemy_user.game_token += fee
            game_room.game_room_is_end = True
            my_user.save()
            enemy_user.save()
            game_room.save()
            PlayerWarning.objects.create(player=game_room.player_1, reason="my move is not valid with my tas",
                                         expiry_date=timezone.now())
            PlayerWarning.objects.create(player=game_room.player_2, reason="my move is not valid with my tas",
                                         expiry_date=timezone.now())
            return Response({
                "status": "game_cancel",
            }, status=status.HTTP_200_OK)


class CheckTimePlease(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            game_room = get_object_or_404(GameRoom, id=room_id)
            player = request.user
            my_turn_num = game_room.get_player_turn_number(player)
            my_user = get_object_or_404(User, username=player)
        except:
            return Response({"status": "you_lose"}, status=status.HTTP_200_OK)

        if not game_room.is_player_1_win and not game_room.is_player_2_win:
            time_is_ok = game_room.check_time_is_ok(player)
            if game_room.current_turn == my_turn_num and not time_is_ok:
                game_room.iam_lose_the_game(loser=my_user)
                return Response({"status": "you_lose"}, status=status.HTTP_200_OK)
            elif not time_is_ok:
                if not game_room.check_time_is_ok(game_room.get_enemy_user_qs(my_user)):
                    game_room.iam_win_the_game(winner=my_user,
                                               prize=game_room.table.get_winner_prize_user_left_the_game())
                    game_room.iam_lose_the_game(loser=game_room.get_enemy_user_qs(my_user))
                    game_room.delete()
                    print("hello ")
                    return Response({"status": "you_win"}, status=status.HTTP_200_OK)

        if game_room.game_room_is_end:
            if my_turn_num == 1 and game_room.is_player_1_win:
                game_room.iam_win_the_game(winner=my_user, prize=game_room.table.get_winner_prize_user_left_the_game())
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)
            elif my_turn_num == 2 and game_room.is_player_2_win:
                game_room.iam_win_the_game(winner=my_user, prize=game_room.table.get_winner_prize_user_left_the_game())
                return Response({"status": "you_win"}, status=status.HTTP_200_OK)

        return Response({"status": "wait_for_turn"}, status=status.HTTP_200_OK)


class IWantLeave(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        try:
            game_room = get_object_or_404(GameRoom, id=room_id)
            player = request.user
            my_user = get_object_or_404(User, username=player)

            if not game_room.is_player_1_win and not game_room.is_player_2_win:
                game_room.iam_lose_the_game(my_user)
                game_room.game_room_is_end = True
                game_room.save()

            return Response({"status": "thanks"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "thanks"}, status=status.HTTP_200_OK)
