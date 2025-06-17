from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppViewSet, TaskViewSet,
    home, admin_page, user_page,
    profile, points, task_list, task_detail, app_detail,
    upload_screenshot, logout_view, add_app,
)
from . import views

from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register('apps', AppViewSet)
#router.register('tasks-api', TaskViewSet)  # Changed to avoid conflict with /tasks/ UI route

urlpatterns = [
    # Main UI Routes
    path('', home, name='home'),
    path('admin-page/', views.admin_dashboard, name='admin-page'),
    path('dashboard/', user_page, name='user-page'),
    path('profile/', profile, name='profile'),
    path('points/', views.points_view, name='points'),
    path('tasks/', task_list, name='task-list'),
    path('task/<int:pk>/', task_detail, name='task-detail'),
    path('app/<int:pk>/', views.app_detail, name='app-detail'),
    path('upload/', upload_screenshot, name='upload-screenshot'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add-app/', views.add_app, name='add-app'),
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
    path('assigned-tasks/', views.assigned_tasks, name='assigned-tasks'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('upload-screenshot/<int:app_id>/', views.upload_screenshot, name='upload_screenshot'),

    # API Routes
    path('api/', include(router.urls)),
]
