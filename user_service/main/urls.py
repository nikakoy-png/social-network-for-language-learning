from django.urls import path
from main import views

urlpatterns = [
    path('api/v1/login/', views.login_user, name='login'),
    path('api/v1/register/', views.create_user, name='register'),
    path('api/v1/languages/', views.get_languages, name='languages'),
    path('api/v1/user/add_language/', views.add_language, name='add_languages'),
    path('api/v1/user/delete_language/', views.delete_language, name='del_languages'),
    path('api/v1/get_suitable_users/', views.get_suitable_users, name='get_suitable_users'),
]
