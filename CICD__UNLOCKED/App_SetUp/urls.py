from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import send_private_message
from .views import view_my_messages
from . import views
from .views import add_student_note
from .views import view_student_notes
from django.urls import path
from . import views
from .views import send_message_to_admin
from .views import view_lecturer_messages







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
    path('admin_page/resolve_request/<int:message_id>/', views.resolve_request, name='resolve_request'),
    path('lecturer/resolve_request/<int:message_id>/', views.resolve_lecturer_request, name='resolve_lecturer_request'),

    path('progress/', views.student_progress, name='student_progress'),
    path('learning/', views.learning_home, name='learning_home'),
    path('modules/git/', views.git_module_view, name='git_module'),
    path('modules/jenkins/', views.jenkins_module_view, name='jenkins_module'),
    path('modules/docker/', views.docker_module_view, name='docker_module'),

    path('lecturer/manage-content/', views.lecturer_manage_content, name='lecturer_manage_content'),
    path('lecturer/update-content/<int:content_id>/', views.update_module_visibility, name='update_module_visibility'),

    path('LecturerPages/LecturerTasksAndAssignments/manage_tasks_and_check_assignments.html', views.manage_tasks_and_check_assignments, name='manage_tasks_and_check_assignments'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_git.html', views.Lecturer_manage_git, name='Lecturer_manage_git'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_docker.html', views.Lecturer_manage_docker, name='Lecturer_manage_docker'),
    path('LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_jenkins.html', views.Lecturer_manage_jenkins, name='Lecturer_manage_jenkins'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection1.html', views.GitSection1, name='GitSection1'),
    path('LecturerPages/LecturerTasksAndAssignments/GitSection2.html', views.GitSection2, name='GitSection2'),
    path('LecturerPages/LecturerTasksAndAssignments/JenkinsSection.html', views.JenkinsSection, name='JenkinsSection'),
    path('LecturerPages/LecturerTasksAndAssignments/DockerSection.html', views.DockerSection, name='DockerSection'),

    path('student/rate_modules/', views.rate_learning_modules, name='rate_modules'),
    path('lecturer/view_ratings/', views.view_module_ratings, name='view_module_ratings'),
    path('learning/git/section1/', views.git_section1, name='git_section1'),
    path('learning/git/section2/', views.git_section2, name='git_section2'),
    path('learning/git/section3/', views.git_section3, name='git_section3'),
    path('learning/git/section4/', views.git_section4, name='git_section4'),

    path('learning/jenkins/section1/', views.jenkins_section1, name='jenkins_section1'),
    path('learning/jenkins/section2/', views.jenkins_section2, name='jenkins_section2'),
    path('learning/jenkins/section3/', views.jenkins_section3, name='jenkins_section3'),
    path('learning/jenkins/section4/', views.jenkins_section4, name='jenkins_section4'),

    path('learning/docker/section1/', views.docker_section1, name='docker_section1'),
    path('learning/docker/section2/', views.docker_section2, name='docker_section2'),
    path('learning/docker/section3/', views.docker_section3, name='docker_section3'),


    path('lecturer/send-message/', send_private_message, name='send_private_message'),
    path('student/my-messages/', view_my_messages, name='view_my_messages'),

    path('lecturer/monitor-progress/', views.monitor_student_git_progress, name='monitor_student_git_progress'),
    path('lecturer/monitor-progress/download/', views.download_student_report, name='download_student_report'),
    path('student/add-note/', add_student_note, name='add_student_note'),
    path('student/notes/', view_student_notes, name='view_student_notes'),



    path('learning/git/git_rating', views.git_rating, name='git_rating'),
    path('learning/jenkins/jenkins_rating', views.jenkins_rating, name='jenkins_rating'),
    path('learning/docker/docker_rating', views.docker_rating, name='docker_rating'),
    path('run_tests/', views.run_tests, name='run_tests'),
    path('lecturer/message-to-admin/', send_message_to_admin, name='send_message_to_admin'),
    path('admin_page/lecturer-messages/', view_lecturer_messages, name='view_lecturer_messages'),



]
