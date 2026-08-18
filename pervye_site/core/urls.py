from django.urls import path
from . import views

urlpatterns = [
    # Главная страница и каталог программ
    path('', views.catalog_view, name='catalog'),
    
    # Страница курса и конкретного урока
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_view, name='lesson'),
    
    # Личный кабинет и UGC-блог
    path('profile/', views.profile_view, name='profile'),
    path('profile/create/', views.create_material_view, name='create_material'),
    
    # Авторизация пользователей
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
