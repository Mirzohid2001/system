from django.contrib import admin
from .models import User, Token , UserProfile
# Register your models here.

admin.site.site_header = "system|Admin"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')
    search_fields = ('user__username', 'token')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','avatar', 'bio', 'telegram_link', 'instagram_link')
    search_fields = ('user__username', 'avatar', 'bio', 'telegram_link', 'instagram_link')
