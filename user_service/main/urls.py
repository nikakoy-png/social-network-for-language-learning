from django.urls import path
from main import views

urlpatterns = [
    path('api/v1/login/', views.login_user, name='login'),
    path('api/v1/register/', views.create_user, name='register'),
    path('api/v1/languages/', views.get_languages, name='get_list_languages'),
    path('api/v1/user/add_language/', views.add_language, name='add_language_to_user'),
    path('api/v1/user/delete_language/', views.delete_language, name='delete_languages_from_user'),
    path('api/v1/user/update_profile/', views.update_profile, name='update_profile'),
    path('api/v1/user/profile/', views.get_profile, name='get_self_user_profile'),
    path('api/v1/get_user_by_id/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('api/v1/get_suitable_users/', views.get_suitable_users, name='get_suitable_users'),
]
