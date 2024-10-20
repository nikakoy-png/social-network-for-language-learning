from django.urls import path
from main import views

urlpatterns = [
    path('api/v1/login/', views.login_admin, name='login'),
    path('api/v1/is_admin/', views.is_admin, name='is_admin'),
    path('api/v1/get_list_users/<int:page_number>/<int:page_size>/', views.get_list_users, name='get_list_users'),
    path('api/v1/get_perfomances/<int:user_id>/', views.get_performances, name='get_performances'),
    path('api/v1/get_count_perfomances/<int:user_id>/', views.get_count_performances, name='get_count_performances'),
    path('api/v1/add_performances/', views.add_performance, name='add_performance'),
    path('api/v1/get_admin_data/<int:admin_id>/', views.get_admin_data, name='get_admin_data'),
]
