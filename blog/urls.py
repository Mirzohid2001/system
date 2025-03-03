from django.urls import path
from .views import CategoryView, CategoryDetailView, AnnouncementListCreateView, AnnouncementDetailView,PaymentListCreateView, FavoriteListCreateView, FavoriteDeleteView, CommentListCreateView, AnnouncementRecommendationView,GlobalSearchView

urlpatterns = [
    path('categories/',CategoryView.as_view(),name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorites-list-create'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('comments/', CommentListCreateView.as_view(), name='comments-list-create'),
    path('announcements/<int:pk>/recommendations/', AnnouncementRecommendationView.as_view(), name='recommendations'),
    path('search/', GlobalSearchView.as_view(), name='global-search'),
]
