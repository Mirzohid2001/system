from django.shortcuts import render
from .serializers import CategorySerializer
from .models import Category
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer,PaymentSerializer,FavoriteSerializer,CommentSerializer
from .models import Announcement, Payment,Favorite,Comment
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
import random
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all().order_by('-priority', '-created_at')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'condition', 'status', 'plan']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at','price']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnnouncementCreateSerializer
        return AnnouncementSerializer

    def perform_create(self, serializer):
        if not getattr(self.request, 'user', None) or not self.request.user.id:
            raise PermissionDenied("Войдите, чтобы разместить объявление.")
        serializer.save(user=self.request.user)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all().order_by('-priority', '-created_at')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'condition', 'status', 'plan']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at']

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AnnouncementCreateSerializer
        return AnnouncementSerializer

    def perform_update(self, serializer):
        announcement = self.get_object()
        if announcement.user != self.request.user:
            raise PermissionDenied("Вы можете только редактировать свое объявление.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы можете только удалить свое объявление.")
        instance.delete()


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(user=user)

    def perform_create(self, serializer):
        if not getattr(self.request, 'user', None) or not self.request.user.id:
            raise PermissionDenied("Войдите, чтобы оплатить объявление.")
        serializer.save()

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Войдите, чтобы добавить объявление в избранное.")
        serializer.save(user=self.request.user)

class FavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        announcement_id = self.request.query_params.get('announcement')
        if announcement_id:
            queryset = queryset.filter(announcement_id=announcement_id)
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Войдите, чтобы оставить комментарий.")
        serializer.save()

class AnnouncementRecommendationView(APIView):
    def get(self, request, pk):
        try:
            current_announcement = Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return Response({"detail": "Объявление не найдено"}, status=404)

        cat = current_announcement.category
        queryset = Announcement.objects.filter(
            category=cat, status='published'
        ).exclude(id=pk)

        all_ids = list(queryset.values_list('id', flat=True))
        random_ids = random.sample(all_ids, min(len(all_ids), 5))
        recommended = Announcement.objects.filter(pk__in=random_ids)

        serializer = AnnouncementSerializer(recommended, many=True)
        return Response(serializer.data, status=200)
    
class GlobalSearchView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()

        announcements = Announcement.objects.none()
        if query:
            announcements = Announcement.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        categories = Category.objects.none()
        if query:
            categories = Category.objects.filter(name__icontains=query)
        ann_serializer = AnnouncementSerializer(announcements, many=True)
        cat_serializer = CategorySerializer(categories, many=True)

        data = {
            "query": query,
            "announcements": ann_serializer.data,
            "categories": cat_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
