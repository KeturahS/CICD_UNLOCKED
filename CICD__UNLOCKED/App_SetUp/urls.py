from django.urls import path
from django.contrib.auth import views as auth_views



from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('lecturer/', views.lecturer, name='lecturer'),
    path('student/', views.student, name='student'),
    path('student_extra/', views.student_extra, name='student_extra'),
    path('terms/', views.terms_view, name='terms'),
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
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('student/profile/', views.student_profile_view, name='student_profile'),
    path('lecturer/profile/', views.lecturer_profile_view, name='lecturer_profile'),
    path('student/profile/update/', views.update_student_profile, name='update_student_profile'),

    path('contact/', views.contact_us, name='contact_us'),
    path('my-messages/', views.student_messages_view, name='student_messages'),


    path('learning/', views.learning_home, name='learning_home'),
    path('modules/git/', views.git_module_view, name='git_module'),
    path('modules/jenkins/', views.jenkins_module_view, name='jenkins_module'),
    path('modules/docker/', views.docker_module_view, name='docker_module'),
    path('LecturerPages/LecturerTasksAndAssignments/manage_tasks_and_check_assignments.html', views.manage_tasks_and_check_assignments, name='manage_tasks_and_check_assignments'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_git.html', views.Lecturer_manage_git, name='Lecturer_manage_git'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_docker.html', views.Lecturer_manage_docker, name='Lecturer_manage_docker'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_jenkins.html', views.Lecturer_manage_jenkins, name='Lecturer_manage_jenkins'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection1.html', views.GitSection1, name='GitSection1'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection2.html', views.GitSection2, name='GitSection2'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection3.html', views.GitSection3, name='GitSection3'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection4.html', views.GitSection4, name='GitSection4'),
    path('student/rate_modules/', views.rate_learning_modules, name='rate_modules'),
    path('lecturer/view_ratings/', views.view_module_ratings, name='view_module_ratings'),

]
