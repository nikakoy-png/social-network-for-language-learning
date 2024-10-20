from django.conf.urls.static import static
from django.urls import path
from main import views
from user_service import settings
from django.urls import path

urlpatterns = [
    path('api/v1/login/', views.login_user, name='login'),
    path('api/v1/register/', views.create_user, name='register'),
    path('api/v1/languages/', views.get_languages, name='get_list_languages'),
    path('api/v1/user/add_language/', views.add_language, name='add_language_to_user'),
    path('api/v1/user/delete_language/<int:language_id>/', views.delete_language, name='delete_languages_from_user'),
    path('api/v1/user/update_profile/', views.update_profile, name='update_profile'),
    path('api/v1/user/profile/', views.get_profile, name='get_self_user_profile'),
    path('api/v1/get_user_by_id/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('api/v1/get_suitable_users/', views.get_suitable_users, name='get_suitable_users'),
    path('api/v1/get_list_users/<int:page_number>/<int:page_size>/', views.get_list_users_for_admin, name='get_list_users_for_admin'),
    path('api/v1/get_user_for_admin/<str:username>/', views.get_user_for_admin, name='get_user_for_admin'),
    path('api/v1/update_user_status_for_admin/<int:user_id>/', views.update_user_status_for_admin, name='update_user_status_for_admin'),
] + static('/api/v1/media/', document_root=settings.MEDIA_ROOT)

