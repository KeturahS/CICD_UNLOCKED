import random

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import SignUpForm,LoginForm


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

            if role == "admin":
                user.is_admin = True
                user.is_active = False
                msg = 'נא להמתין לבדיקת מנהל בכיר, תשובה בעניין הסטטוס תישלח במייל שהוזן על ידך'
                SuperUserEmail = get_superuser_email()
                if SuperUserEmail:
                    send_mail(
                        'בקשת מנהל חדשה במערכת CiCd_Unlocked - נדרש אישור',  # נושא המייל
                        '''  
                        שלום מנהל בכיר יקר,

                        הוגשה בקשת קבלת סטטוס מנהל חדשה במערכת CiCd_Unlocked.

                        אנא היכנס לעמוד הדשבורד כדי לאשר או לסרב לבקשה.

                        חשוב לטפל בבקשה בהקדם האפשרי כדי להבטיח ניהול תקין של המערכת.

                        אם אתה זקוק לעזרה נוספת או שיש לך שאלות, אל תהסס לפנות אלינו.

                        בברכה,  
                        צוות CiCd_Unlocked  
                        ''',
                        settings.EMAIL_HOST_USER,
                        [SuperUserEmail],
                        fail_silently=False,
                    )


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

@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.is_admin:
                        login(request, user)
                        return redirect('admin')

                    if user.is_lecturer:
                        login(request, user)
                        return redirect('lecturer')
                else:
                    if user.is_lecturer:
                        msg = 'בקשתך להירשם כמרצה טרם אושרה, אנא המתן בסבלנות לתשובה מצוות האתר'
                    if user.is_admin:
                        msg = 'בקשתך להירשם כמנהל טרם אושרה, אנא המתן בסבלנות לתשובת המנהל הבכיר'

                    return render(request, 'login.html')
            else:
                msg = 'פרטים לא נכונים'
        else:
            msg = 'טופס לא תקין'
    return render(request, 'login.html', {'form': form, 'msg': msg})




def lecturer(request):
    return render(request, 'lecturer.html')

@login_required
@csrf_protect
def admin(request):
    lecturers_requests = User.objects.filter(is_lecturer=True, is_active=False)
    students = User.objects.filter(is_student=True, is_active=True)
    admins_requests = User.objects.filter(is_admin=True, is_active=False) if request.user.is_superuser else None
    active_lecturers = User.objects.filter(is_lecturer=True, is_active=True)
    active_admins = User.objects.filter(is_admin=True, is_active=True)

    context = {
        "lecturers_requests": lecturers_requests,
        "students": students,
        "admins_requests": admins_requests,
        "active_lecturers": active_lecturers,
        "active_admins": active_admins
    }
    return render(request, "admin_page.html",context)



def manage_admins(request):
    return render(request, "admin_page_admins_section.html")


def manage_lecturers(request):
    return render(request, "admin_page_lecturers_section.html")


def manage_students(request):
    return render(request, "admin_page_students_section.html")


def get_superuser_email():
    # Retrieve the first superuser
    superuser = User.objects.filter(is_superuser=True).first()

    return superuser.email if superuser else None




