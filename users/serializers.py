from rest_framework import serializers
import secrets
from .models import User, Token ,UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos emas!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        token_str = secrets.token_hex(32)
        Token.objects.create(user=user, token=token_str)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "такого пользователя не существует"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "неверный пароль"})

        attrs['user'] = user
        return attrs
    
class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = UserProfile
        fields = ['user_id', 'avatar', 'bio', 'telegram_link', 'instagram_link']
        read_only_fields = ['user_id']
    
# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Bunday email ro‘yxatdan o‘tmagan.")
#         attrs['user'] = user
#         return attrs

#     def create(self, validated_data):
#         user = validated_data['user']
#         # Yangi token yaratamiz
#         token_obj = ResetPasswordToken.objects.create(user=user)
#         # Email yoki SMS yuborish
#         reset_link = f"https://example.com/reset-password/{token_obj.token}/"
#         send_mail(
#             subject="Parolni tiklash",
#             message=f"Parolni tiklash uchun link: {reset_link}",
#             from_email="noreply@example.com",
#             recipient_list=[user.email],
#             fail_silently=False
#         )
#         return token_obj


# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     new_password = serializers.CharField()

#     def validate(self, attrs):
#         token = attrs['token']
#         try:
#             token_obj = ResetPasswordToken.objects.get(token=token, is_used=False)
#         except ResetPasswordToken.DoesNotExist:
#             raise serializers.ValidationError("Token noto‘g‘ri yoki ishlatilgan.")
#         if token_obj.is_expired():
#             raise serializers.ValidationError("Token eskirgan. Yangi token so‘rang.")
#         attrs['token_obj'] = token_obj
#         return attrs

#     def save(self, **kwargs):
#         token_obj = self.validated_data['token_obj']
#         new_password = self.validated_data['new_password']
#         user = token_obj.user
#         user.password = new_password
#         user.save()

#         token_obj.is_used = True
#         token_obj.save()
#         return user
