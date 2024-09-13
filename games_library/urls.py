from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    
]