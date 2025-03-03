# main/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from .models import Token, UserProfile
import secrets

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Вы успешно зарегистрировались!",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            Token.objects.filter(user=user).delete()

            new_token_value = secrets.token_hex(32)
            token_obj = Token.objects.create(user=user, token=new_token_value)

            return Response({
                "message": "Вы успешно вошли в систему!",
                "token": token_obj.token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    def get(self, request):
        # Faqat o‘z profilini ko‘rish
        if not request.user.is_authenticated:
            return Response({"detail": "Tizimga kiring."}, status=401)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Tizimga kiring."}, status=401)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# from .serializers import (
#     PasswordResetRequestSerializer,
#     PasswordResetConfirmSerializer
# )

# class PasswordResetRequestView(APIView):
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # token yaratish, email yuborish
#             return Response({"detail": "Parolni tiklash linki emailga yuborildi."}, status=200)
#         return Response(serializer.errors, status=400)

# class PasswordResetConfirmView(APIView):
#     def post(self, request, token):
#         data = request.data.copy()
#         data['token'] = token
#         serializer = PasswordResetConfirmSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"detail": "Parol yangilandi."}, status=200)
#         return Response(serializer.errors, status=400)