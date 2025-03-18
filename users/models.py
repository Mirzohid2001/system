from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import secrets
from datetime import timedelta
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):

        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username
    

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token
    
    class Meta:
        db_table = "tokens"
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "user_profiles"
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

# class ResetPasswordToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=64, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.token:
#             self.token = secrets.token_hex(32)
#         super().save(*args, **kwargs)

#     def is_expired(self):
#         expiration_time = self.created_at + timedelta(hours=1)
#         return timezone.now() > expiration_time

#     def __str__(self):
#         return f"ResetToken for {self.user.email} - used={self.is_used}"

