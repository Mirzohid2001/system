from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import PermissionDenied
from .models import Category, Announcement, AnnouncementImage, Payment, Plan, Favorite, Comment, AnalyticsDummy,News,Chat,Message,Banner,GalleryImage,OtherAnnouncement
from mptt.admin import DraggableMPTTAdmin

User = get_user_model()

admin.site.register(Banner)

class AnnouncementImageInline(admin.TabularInline):
    model = AnnouncementImage
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'priority']
    list_editable = ['amount', 'priority']

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'id', 'created_at')
    list_display_links = ('indented_title',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [AnnouncementImageInline]
    list_display = ('id', 'title', 'user', 'category', 'plan', 'priority', 'created_at')
    list_filter = ('plan', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'plan', 'amount', 'paid', 'created_at')
    list_filter = ('plan', 'paid', 'created_at')
    search_fields = ('user__username', 'announcement__title', 'payment_id')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'created_at')
    search_fields = ('user__username', 'announcement__title')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'announcement__title', 'text')

@admin.register(AnalyticsDummy)
class AnalyticsAdminView(admin.ModelAdmin):
    change_list_template = 'admin/analytics.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        today = timezone.now()
        extra_context = extra_context or {}

        periods = {
            'daily': today - timedelta(days=1),
            'weekly': today - timedelta(weeks=1),
            'monthly': today - timedelta(days=30),
            'yearly': today - timedelta(days=365),
        }

        stats = {}

        for period_name, period_start in periods.items():
            stats[f'{period_name}_users'] = User.objects.filter(date_joined__gte=period_start).count()
            stats[f'{period_name}_announcements'] = Announcement.objects.filter(created_at__gte=period_start).count()
            stats[f'{period_name}_payments'] = Payment.objects.filter(
                created_at__gte=period_start, paid=True
            ).aggregate(total=Sum('amount'))['total'] or 0

        extra_context.update(stats)

        extra_context.update({
            'total_users': User.objects.count(),
            'total_announcements': Announcement.objects.count(),
            'total_payments': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
        })

        return super().changelist_view(request, extra_context=extra_context)
    
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'announcement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('id', 'participants__username')
    filter_horizontal = ('participants',) 
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text', 'created_at')
    list_filter = ('created_at', 'chat')
    search_fields = ('sender__username', 'text')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(OtherAnnouncement)
class OtherAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


