from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('lecturer/', views.lecturer, name='lecturer'),
    path('admin_page/', views.admin, name='admin'),
    path('admin_page_students_section/', views.manage_students, name='manage_students'),
    path('admin_page_lecturers_section/', views.manage_lecturers, name='manage_lecturers'),
    path('admin_page_admins_section/', views.manage_admins, name='manage_admins'),
    path('handle_lecturer_request/', views.handle_lecturer_request, name='handle_lecturer_request'),
    path('handle_admin_request/', views.handle_admin_request, name='handle_admin_request'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('delete_lecturer/', views.delete_lecturer, name='delete_lecturer'),
    path('delete_admin/', views.delete_admin, name='delete_admin'),
    path('upgrade_admin/', views.upgrade_admin, name='upgrade_admin'),


]
