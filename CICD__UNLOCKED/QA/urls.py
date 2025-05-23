
from django.urls import path
from . import views


app_name = 'qa'

urlpatterns = [
    path('QA_Page', views.QA_Page, name='QA_Page'),
    path('handle_faq/', views.handle_faq, name='handle_faq'),


]
