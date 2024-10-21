from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Referral, GameHistory
from .serializers import UserSerializer, ReferralSerializer, GameHistorySerializer


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
