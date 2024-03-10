from django.urls import path
from .views import register_service, get_service_info, add_version, update_service, get_services

urlpatterns = [
    path('register-service/', register_service, name='register-service'),
    path('get-service-info/<str:service_name>/', get_service_info, name='get-service-info'),
    path('get-all-services/', get_services, name='get-all-services'),
    path('add-version/<int:service_id>/', add_version, name='add-version'),
    path('update-service/<int:service_id>/', update_service, name='update-service'),
]
