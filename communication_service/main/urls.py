from django.conf.urls.static import static
from django.urls import path
from main import views

urlpatterns = [
    path('api/v1/create_dialog/', views.create_dialog, name='create_dialog'),
    path('api/v1/create_complaint/', views.create_complaint, name='create_complaint'),
    path('api/v1/delete_dialog/<int:dialog_id>/<int:user_id>/', views.delete_dialog, name='delete_dialog'),
    path('api/v1/get_user_statistic/<int:user_id>/', views.get_statistic_users, name='get_statistic_users'),
    path('api/v1/get_complaints/<int:page_number>/<int:page_size>/<str:is_answer>/', views.get_complaints, name='get_complaints'),
    path('api/v1/get_complaints_by_user_id/<int:user_id>/<str:is_answer>/', views.get_complaints_by_user_id, name='get_complaints_by_user_id'),
    path('api/v1/set_resolution_on_complaint/<int:complaint_id>/', views.set_resolution_on_complaint, name='set_resolution_on_complaint'),
    path('api/v1/get_details_dialogs/<int:dialog_id>/', views.get_details_dialogs, name='get_details_dialogs'),
    path('api/v1/get_list_dialogs_for_admin/<int:user_id>/', views.get_list_dialogs_for_admin, name='get_dialogs_admin'),
    path('api/v1/get_list_messages_for_admin/<int:dialog_id>/', views.get_list_messages_for_admin, name='get_list_messages_for_admin'),
]
