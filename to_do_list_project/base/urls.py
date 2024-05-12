from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/',views.Login,name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',views.Register,name='register'),
    path('',TaskList.as_view(), name='tasks'),
    path('task/<int:pk>',TaskDetail.as_view(), name='task'),
    path('task-create',TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>',TaskDelete.as_view(), name='task-delete'),
]