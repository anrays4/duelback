from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import random

from .models import GameTable, WaitingRoom, GameRoom
from .serializers import (
    GameTableSerializer, WaitingRoomSerializer, GameRoomSerializer, PlayerWarningSerializer
)
from players.models import GameHistory


def game_table_list(request):
    game_tables = GameTable.objects.all()
    context = {'game_tables': game_tables}
    return render(request, '/game_table_list.html', context=context)


def find_match(request):
    if request.method == 'POST':
        player = request.user
        game_table_id = request.data.get('game_table_id')  # انتظار داریم game_table_id رو از کاربر بگیریم

        if not game_table_id:
            context = {'status': "Game table ID is required."}
            return render(request, '/aaa.html', context=context, status=status.HTTP_400_BAD_REQUEST)

        i = True
        while i:
            waiting_room = WaitingRoom.objects.filter(game_table__id=game_table_id).exclude(player_1=player).first()

            if waiting_room:
                # اگر اتاق انتظار پیدا شد، بررسی کنیم که آیا از ددلاین گذشته یا نه
                if waiting_room.is_expired():
                    waiting_room.delete()
                    context = {'message': "No valid waiting room found, deadline expired."}
                    return render(request, '/aab.html', context=context, status=status.HTTP_404_NOT_FOUND)

                else:
                    # اگر از ددلاین نگذشته و اتاق انتظار داریم، اتاق بازی ایجاد کنیم و اتاق انتظار رو پاک کنیم
                    game_room = GameRoom.objects.create(
                        waiting_room=waiting_room,
                        player_1=waiting_room.player_1,
                        player_2=player
                    )
                    waiting_room.delete()

                    context = {'message': "Game room created.", 'game_room_id': game_room.id, 'player_1': game_room.player_1.username,
                               'player_2': game_room.player_2.username}
                    return render(request, '/aac.html', context=context, status=status.HTTP_201_CREATED)

            else:
                # اگر اتاق انتظاری پیدا نشد یا ددلاین آن گذشته بود
                WaitingRoom.objects.filter(player_1=player).delete()  # هر اتاق انتظار قبلی بازیکن رو حذف می‌کنیم
                new_waiting_room = WaitingRoom.objects.create(
                    game_table=game_table_id,
                    player_1=player
                )
                i = False
                context = {'message': "New waiting room created.", 'waiting_room_id': new_waiting_room.id, 'player_1': new_waiting_room.player1.username,
                           'deadline': new_waiting_room.deadline}
                return render(request, '/aac.html', context=context, status=status.HTTP_201_CREATED)


# API برای تایید آماده بودن بازیکن
class PlayerReadyAPIView(APIView):
    def post(self, request, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        player = request.user

        try:
            # آماده شدن بازیکن
            game_room.mark_ready(player)
        except:
            return Response({"status": 'you are not in this room'}, status=status.HTTP_400_BAD_REQUEST)

        # چک کردن وضعیت آماده بودن هر دو بازیکن
        if game_room.has_both_ready():
            game_room.roll_dice()
            game_room.set_turn()
            turn_dice1 = game_room.dice1
            turn_dice2 = game_room.dice2
            game_room.roll_dice()
            return Response({
                "status": "start_game",
                "turn": game_room.current_turn.username,
                "turn_tas_player_1": turn_dice1,
                "turn_tas_player_2": turn_dice2,
                "main_tas_1": game_room.dice1,
                "main_tas_2": game_room.dice2,
            }, status=status.HTTP_200_OK)
        return Response({"status": "please_wait"}, status=status.HTTP_200_OK)


# API پولینگ برای چک کردن آماده بودن بازیکن مقابل و ارسال اطلاعات بازی
# class PollingReadyAPIView(APIView):
#     def get(self, request, room_id):
#         game_room = get_object_or_404(GameRoom, waiting_room__id=room_id)
#         player = request.user
#
#         # بررسی آماده بودن دو بازیکن
#         if game_room.has_both_ready():
#             return Response({
#                 "message": "Both players are ready",
#                 "dice1": game_room.dice1,
#                 "dice2": game_room.dice2,
#                 "current_turn": game_room.current_turn.username
#             })
#         return Response({"message": "Waiting for players to be ready."})


# API پولینگ برای چک کردن نوبت بازیکن مقابل
class PollingTurnAPIView(APIView):
    def get(self, request, room_id):
        game_room = get_object_or_404(GameRoom, waiting_room__id=room_id)
        player = request.user

        # اگر نوبت بازیکن فعلی است
        if game_room.current_turn == player:
            game_room.roll_dice()
            return Response({
                "status": "you_can_play",
                "turn": game_room.current_turn,
                "main_tas_1": game_room.dice1,
                "main_tas_2": game_room.dice2,
                # "last_moves": game_room.board_state.get('last_moves', [])
                "move_history": {},
                "place_status": {}
            }, status=status.HTTP_200_OK)
        return Response({"status": "wait_more"}, status=status.HTTP_200_OK)


# API تایید حرکت بازیکن و تغییر نوبت
class ConfirmMoveAPIView(APIView):
    def post(self, request, room_id):
        game_room = get_object_or_404(GameRoom, waiting_room__id=room_id)
        player = request.user

        # بررسی اینکه آیا نوبت بازیکن فعلی است یا نه
        if game_room.current_turn != player:
            return Response({"error": "It's not your turn."}, status=status.HTTP_400_BAD_REQUEST)
        game_room.move_history = request.data.get('move_history', {})
        game_room.save()
        game_room.update_board_state(request.data.get('place_status', {}))

        # به‌روزرسانی وضعیت بازی و سوئیچ نوبت
        game_room.switch_turn()

        return Response({
            "status": "wait_for_turn",
            "waiting_poll_time": 5,
        },status=status.HTTP_200_OK)


# # ویو برای GameTable
# class GameTableAPIView(APIView):
#     def get(self, request, pk=None):
#         if pk:
#             game_table = get_object_or_404(GameTable, pk=pk)
#             serializer = GameTableSerializer(game_table)
#         else:
#             game_tables = GameTable.objects.all()
#             serializer = GameTableSerializer(game_tables, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = GameTableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         game_table = get_object_or_404(GameTable, pk=pk)
#         serializer = GameTableSerializer(game_table, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         game_table = get_object_or_404(GameTable, pk=pk)
#         game_table.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # Create or find a match in Waiting Room
# class FindMatchAPIView(APIView):
#     def post(self, request):
#         player = request.user
#         game_table_id = request.data.get('game_table')
#
#         # Try to find an available waiting room for this game table
#         waiting_room = WaitingRoom.objects.filter(game_table_id=game_table_id, player2__isnull=True).first()
#
#         if waiting_room:
#             # Assign player2 to the found waiting room
#             waiting_room.player2 = player
#             waiting_room.save()
#
#             # Create a game room
#             game_room = GameRoom.objects.create(
#                 waiting_room=waiting_room,
#                 player_white=waiting_room.player1 if random.choice([True, False]) else player,
#                 player_black=player if waiting_room.player1 != player else waiting_room.player1,
#             )
#
#             serializer = GameRoomSerializer(game_room)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         # If no waiting room is found, create a new one
#         new_waiting_room = WaitingRoom.objects.create(
#             game_table_id=game_table_id,
#             player1=player,
#             deadline=timezone.now() + timezone.timedelta(minutes=2)  # 2 minutes deadline
#         )
#         serializer = WaitingRoomSerializer(new_waiting_room)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# # Roll dice for turn decision
# class RollDiceForTurnAPIView(APIView):
#     def post(self, request, game_room_id):
#         game_room = get_object_or_404(GameRoom, id=game_room_id)
#         player = request.user
#
#         # Check if it's this player's turn to roll the dice for turn
#         if game_room.current_turn != player:
#             return Response({"error": "Not your turn."}, status=status.HTTP_400_BAD_REQUEST)
#
#         dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
#
#         # Ensure the two dice rolls are not equal for determining the first turn
#         while dice1 == dice2:
#             dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
#
#         # Update GameRoom with the dice roll
#         if dice1 > dice2:
#             game_room.current_turn = game_room.player_white
#         else:
#             game_room.current_turn = game_room.player_black
#
#         game_room.save()
#
#         # Return the dice results
#         return Response({
#             "dice1": dice1,
#             "dice2": dice2,
#             "current_turn": "player_white" if dice1 > dice2 else "player_black"
#         }, status=status.HTTP_200_OK)
#
#
# # Roll dice for current player's turn
# class RollDiceAPIView(APIView):
#     def post(self, request, game_room_id):
#         game_room = get_object_or_404(GameRoom, id=game_room_id)
#         player = request.user
#
#         # Check if it's this player's turn
#         if game_room.current_turn != player:
#             return Response({"error": "Not your turn."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Roll two dice
#         dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
#
#         # Create a new DiceRoll record
#         dice_roll = DiceRoll.objects.create(
#             game_room=game_room,
#             player=player,
#             dice1=dice1,
#             dice2=dice2
#         )
#
#         serializer = DiceRollSerializer(dice_roll)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# # Submit a player's board move
# class SubmitBoardMoveAPIView(APIView):
#     def post(self, request, game_room_id):
#         game_room = get_object_or_404(GameRoom, id=game_room_id)
#         player = request.user
#
#         # Check if it's this player's turn
#         if game_room.current_turn != player:
#             return Response({"error": "Not your turn."}, status=status.HTTP_400_BAD_REQUEST)
#
#         move_data = request.data.get('move_data')
#
#         # Create a new BoardMove record
#         board_move = BoardMove.objects.create(
#             game_room=game_room,
#             player=player,
#             move_data=move_data
#         )
#
#         # Update turn to the other player
#         game_room.current_turn = game_room.player_white if game_room.current_turn == game_room.player_black else game_room.player_black
#         game_room.save()
#
#         serializer = BoardMoveSerializer(board_move)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# # Game history after game finishes
# class SaveGameHistoryAPIView(APIView):
#     def post(self, request, game_room_id):
#         game_room = get_object_or_404(GameRoom, id=game_room_id)
#         player = request.user
#         status = request.data.get('status')
#
#         # Save game history for both players
#         GameHistory.objects.create(
#             user1=game_room.player_white,
#             user2=game_room.player_black,
#             status='win' if status == 'win' else 'lose',
#             table=game_room.waiting_room.game_table
#         )
#
#         # Clean up the game room
#         game_room.delete()
#
#         return Response({"message": "Game finished and saved."}, status=status.HTTP_201_CREATED)