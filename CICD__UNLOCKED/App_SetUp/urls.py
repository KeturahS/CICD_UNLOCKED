from django.urls import path
from django.contrib.auth import views as auth_views
import App_SetUp.views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
]
