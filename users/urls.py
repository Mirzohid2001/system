from django.urls import path
from .views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    # path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # path('password-reset-confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

]