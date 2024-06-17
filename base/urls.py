from django.urls import path 
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustomLoginView,profile_view,RegisterPage,custom_logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/',RegisterPage.as_view(),name = 'register'),
    path('logout/',custom_logout_view,name='logout'),
    path('login/',CustomLoginView.as_view(),name='Login'),
    path('accounts/profile/',profile_view,name='profile'),
    path('',TaskList.as_view(),name='task_list'),
    path('create-task/',TaskCreate.as_view(),name='task-create'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
    path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),


    

]