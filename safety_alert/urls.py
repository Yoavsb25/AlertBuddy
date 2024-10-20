from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='safety_alert/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/upload/', views.upload_profile_image, name='upload_profile_image'),
    path('update-status/', views.update_safety_status, name='update_safety_status'),
    path('search/', views.search_users, name='search_users'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('pending-requests/', views.pending_friend_requests, name='pending_friend_requests'),
    path('approve-request/<int:request_id>/', views.approve_friend_request, name='approve_friend_request'),
    path('decline-request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)