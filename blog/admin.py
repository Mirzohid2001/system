from django.contrib import admin
from .models import Category, Announcement, AnnouncementImage, Payment, Favorite, Comment,AnalyticsDummy
from mptt.admin import DraggableMPTTAdmin
from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from django.db.models import Sum
from users.models import User
from django.utils import timezone
from datetime import timedelta
# Register your models here.

class AnnouncementImageInline(admin.TabularInline):
    model = AnnouncementImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'id', 'image', 'created_at')
    list_display_links = ('indented_title',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    inlines = [AnnouncementImageInline] 
    list_display = (
        'id', 'title', 'user', 'category', 
        'plan', 'price', 'status', 'created_at'
    )
    list_filter = ('plan', 'status', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'plan', 'amount', 'created_at')
    list_filter = ('plan', 'created_at')
    search_fields = ('user__username', 'announcement__title')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'announcement__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'announcement', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'announcement__title', 'text')



@admin.register(AnalyticsDummy)
class AnalyticsAdminView(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        now = timezone.now()

        one_day_ago = now - timedelta(days=1)
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)
        one_year_ago = now - timedelta(days=365)

        daily_users = User.objects.filter(created_at__gte=one_day_ago).count()
        weekly_users = User.objects.filter(created_at__gte=one_week_ago).count()
        monthly_users = User.objects.filter(created_at__gte=one_month_ago).count()
        yearly_users = User.objects.filter(created_at__gte=one_year_ago).count()

        daily_ann = Announcement.objects.filter(created_at__gte=one_day_ago).count()
        weekly_ann = Announcement.objects.filter(created_at__gte=one_week_ago).count()
        monthly_ann = Announcement.objects.filter(created_at__gte=one_month_ago).count()
        yearly_ann = Announcement.objects.filter(created_at__gte=one_year_ago).count()

        daily_pay = Payment.objects.filter(created_at__gte=one_day_ago).aggregate(total=Sum('amount'))['total'] or 0
        weekly_pay = Payment.objects.filter(created_at__gte=one_week_ago).aggregate(total=Sum('amount'))['total'] or 0
        monthly_pay = Payment.objects.filter(created_at__gte=one_month_ago).aggregate(total=Sum('amount'))['total'] or 0
        yearly_pay = Payment.objects.filter(created_at__gte=one_year_ago).aggregate(total=Sum('amount'))['total'] or 0

        total_users = User.objects.count()
        total_announcements = Announcement.objects.count()
        total_payments = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

        context = {
            'title': "Analytics Dashboard",

            'total_users': total_users,
            'total_announcements': total_announcements,
            'total_payments': total_payments,
            'daily_users': daily_users,
            'weekly_users': weekly_users,
            'monthly_users': monthly_users,
            'yearly_users': yearly_users,

            'daily_ann': daily_ann,
            'weekly_ann': weekly_ann,
            'monthly_ann': monthly_ann,
            'yearly_ann': yearly_ann,

            'daily_pay': daily_pay,
            'weekly_pay': weekly_pay,
            'monthly_pay': monthly_pay,
            'yearly_pay': yearly_pay,
        }

        return render(request, 'admin/analytics.html', context)