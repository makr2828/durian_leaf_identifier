from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('chat/', views.chat_api, name='chat_api'),
    path('identify-leaf/', views.identify_leaf_view, name='identify_leaf'),
    path('submit-query/', views.submit_query, name='submit_query'),
    path('clear-chat/', views.clear_chat_history, name='clear_chat_history'),
    path('get-chats/', views.get_chat_history, name='get_chats'),
]