import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from App_SetUp.models import User
from .forms import SignUpForm

from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = request.POST.get("role")

            if User.objects.filter(email=user.email).exists():
                msg = 'כתובת הדואר האלקטרוני כבר רשומה במערכת, אנא השתמש/י בכתובת אחרת'
                return render(request, 'register.html', {'form': form, 'msg': msg})

            if User.objects.filter(username=user.username).exists():
                msg = 'שם המשתמש כבר קיים במערכת, אנא בחר/י שם משתמש אחר'
                return render(request, 'register.html', {'form': form, 'msg': msg})

            user.is_admin = user.is_student = user.is_lecturer = False


            if role == "lecturer":
                user.is_lecturer = True
                user.is_active = False
                msg = 'בקשתך לחשבון מרצה התקבלה ונמצאת בתהליך אישור. עדכון בנוגע לסטטוס הבקשה יישלח לכתובת הדואר האלקטרוני שציינת'

            user.save()
        else:
            msg = 'אנא ודא/י כי כל השדות מולאו כראוי'
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form, 'msg': msg})

def login_view(request):
    return render(request, 'login.html')

# Create your views here.
