from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import custom_logout

urlpatterns = [
    # --- Main Views ---
    path('', views.post_list, name='post_list'),
    path('home/', views.home, name='home'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # frontend view
    path('post/<int:pk>/like/', views.post_like, name='post_like'),

    path('post/<int:id>/', views.post_detail, name='post_detail'),


    path('create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # --- User Authentication ---
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # --- Password Reset ---
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # --- API ---
    path('api/posts/', views.PostListCreate.as_view(), name='api_post_list_create'),
    path('api/posts/<int:pk>/', views.PostDetail.as_view(), name='api_post_detail'),
    path('api/posts/<int:post_pk>/comments/', views.CommentListCreate.as_view(), name='api_comment_list_create'),
    path('api/comments/<int:pk>/', views.CommentDetail.as_view(), name='api_comment_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
