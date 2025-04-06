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
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LecturerProfile, StudentProfile, AdminProfile
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

            elif role == "student":
                user.is_student = True
                user.is_active = True

                send_mail(
                    'החשבון נוצר בהצלחה',  # The subject of the email
                    '''  
                    שלום סטודנט יקר,

                    מזל טוב! יצרת חשבון בהצלחה במערכת CiCd_Unlocked. 🎉

                    אנחנו שמחים לקבל אותך במערכת ומאחלים לך המון הצלחה במהלך הלמידה. 
                    אנו בטוחים שהמערכת תעזור לך להשיג את מטרותיך האקדמיות, ואנחנו כאן כדי לתמוך בך בכל שלב בדרך.

                    בהצלחה,  
                    צוות CiCd_Unlocked  
                    ''',  # The body of the email
                    settings.EMAIL_HOST_USER,  # Your email address
                    [user.email],  # The recipient's email address
                    fail_silently=False,
                )
                user.save()
                return render(request, 'index.html')

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
            print(user)
            if user is not None:
                if user.is_active:
                    if user.is_lecturer:
                        login(request, user)
                        return redirect('lecturer')

                    if user.is_admin:
                        login(request, user)
                        return redirect('admin')

                    if user.is_student:
                        login(request, user)
                        return redirect('student')


                if not user.is_active:
                    if user.is_lecturer:
                        msg = 'בקשתך להירשם כמרצה טרם אושרה, אנא המתן בסבלנות לתשובה מצוות האתר'

                    if user.is_admin:
                        msg = 'בקשתך להירשם כמנהל טרם אושרה, אנא המתן בסבלנות לתשובת המנהל הבכיר'

                    return render(request, 'login.html')
            else:
               msg = 'פרטים לא נכונים '

        else:
            msg = 'טופס לא תקין'
    return render(request, 'login.html', {'form': form, 'msg': msg})




def lecturer(request):
    return render(request, 'lecturer.html')

def student(request):
    return render(request, 'student.html')

@login_required
@csrf_protect
def admin(request):
    lecturers_requests = User.objects.filter(is_lecturer=True, is_active=False)
    admins_requests = User.objects.filter(is_admin=True, is_active=False) if request.user.is_superuser else None


    context = {
        "lecturers_requests": lecturers_requests,
        "admins_requests": admins_requests,

    }
    return render(request, "admin_page.html",context)



@login_required
def handle_admin_request(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        action = request.POST.get("action")

        if action == "approve":
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()
            send_mail(
                ' חשבון המנהל שלך אושר על ידי המנהל הבכיר',  # The subject of the email
                '''
               החשבון שלך נוצר בהצלחה במערכת CiCd_Unlocked. 🎉

               אנחנו שמחים לקבל אותך במערכת הניהול ומאחלים לך המון הצלחה בעבודה.
               ''',  # The message of the email
                settings.EMAIL_HOST_USER,  # Your email address
                [user.email],  # List of recipients
                fail_silently=False, )


        elif action == "reject":
            user = User.objects.get(email=user_email)
            send_mail(
                'בקשתך להירשם כמנהל סורבה על ידי המנהל הבכיר',  # The subject of the email
                'פרטי ההרשמה שלך יימחקו',  # The message of the email
                settings.EMAIL_HOST_USER,  # Your email address
                [user.email],  # List of recipients
                fail_silently=False, )
            user.is_admin = False
            user.delete()
        return redirect("admin")

    return redirect("admin")

@login_required
def handle_lecturer_request(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        action = request.POST.get("action")

        if action == "approve":
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()
            send_mail(
                ' חשבון המרצה שלך אושר על ידי מנהל המערכת',  # The subject of the email
                ''' 
                החשבון שלך נוצר בהצלחה במערכת CiCd_Unlocked. 🎉

                אנחנו שמחים לקבל אותך במערכת הניהול ומאחלים לך המון הצלחה בעבודה.
                ''',  # The message of the email
                settings.EMAIL_HOST_USER,  # Your email address
                [user.email],  # List of recipients
                fail_silently=False, )


        elif action == "reject":
            user = User.objects.get(email=user_email)
            send_mail(
                'בקשתך להירשם כמרצה סורבה על ידי מנהל המערכת',  # The subject of the email
                'פרטי ההרשמה שלך יימחקו',  # The message of the email
                settings.EMAIL_HOST_USER,  # Your email address
                [user.email],  # List of recipients
                fail_silently=False, )
            user.is_lecturer = False
            user.delete()
        return redirect("admin")

    return redirect("admin")


def manage_admins(request):
    active_admins = User.objects.filter(is_admin=True, is_active=True)

    context = {
             "active_admins": active_admins
    }
    return render(request, "admin_page_admins_section.html", context)


def manage_lecturers(request):
    active_lecturers = User.objects.filter(is_lecturer=True, is_active=True)

    context = {
        "active_lecturers": active_lecturers
    }
    return render(request, "admin_page_lecturers_section.html", context)


def manage_students(request):
    active_students = User.objects.filter(is_student=True, is_active=True)

    context = {
        "active_students": active_students
    }
    return render(request, "admin_page_students_section.html", context)


def get_superuser_email():
    # Retrieve the first superuser
    superuser = User.objects.filter(is_superuser=True).first()

    return superuser.email if superuser else None

def delete_student(request):
    if request.method == "POST":
        user_email = request.POST.get("student_email")
        user = User.objects.get(email=user_email)
        user.delete()
    return redirect("manage_students")


def delete_lecturer(request):
    if request.method == "POST":
        user_email = request.POST.get("lecturer_email")
        user = User.objects.get(email=user_email)
        user.delete()
    return redirect("manage_lecturers")


def delete_admin(request):
    if request.method == "POST":
        user_email = request.POST.get("admin_email")
        user = User.objects.get(email=user_email)
        user.delete()
    return redirect("manage_admins")

def upgrade_admin(request):
    if request.method == "POST":
        user_email = request.POST.get("admin_email")
        user = User.objects.get(email=user_email)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
    return redirect("manage_admins")

def password_reset(request):
    return render(request, "password_reset.html")


@login_required
def student_profile_view(request):
    user = request.user

    # בדיקה האם המשתמש הוא סטודנט
    if not user.is_student:
        return redirect('login_view')

    try:
        profile = user.student_profile
    except StudentProfile.DoesNotExist:
        profile = None

    return render(request, 'student_profile.html', {'profile': profile})
