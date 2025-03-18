from django.urls import path
from .views import CategoryView, CategoryDetailView, AnnouncementListCreateView, AnnouncementDetailView, FavoriteListCreateView, FavoriteDeleteView, CommentListCreateView, AnnouncementRecommendationView,GlobalSearchView,CreatePaymentAPIView,CheckPaymentStatusAPIView,NewsListView,UserChatsAPIView,ChatCreateOrGetAPIView,MessageCreateAPIView

urlpatterns = [
    path('categories/',CategoryView.as_view(),name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('announcements/', AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('payments/create/', CreatePaymentAPIView.as_view(), name='payment-create'),
    path('payments/status/<str:payment_id>/', CheckPaymentStatusAPIView.as_view(), name='payment-status'),
    path('favorites/', FavoriteListCreateView.as_view(), name='favorites-list-create'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('comments/', CommentListCreateView.as_view(), name='comments-list-create'),
    path('announcements/<int:pk>/recommendations/', AnnouncementRecommendationView.as_view(), name='recommendations'),
    path('search/', GlobalSearchView.as_view(), name='global-search'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('chats/', UserChatsAPIView.as_view(), name='user-chats'),
    path('chats/create/', ChatCreateOrGetAPIView.as_view(), name='chat-create-or-get'),
    path('chats/<int:chat_id>/messages/', MessageCreateAPIView.as_view(), name='message-create'),
]
