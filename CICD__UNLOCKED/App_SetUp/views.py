import random

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required
from .models import User
from .forms import SignUpForm, LoginForm, TerminalExercisesGitCommandsForm, JenkinsConceptsQuizForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LecturerProfile, StudentProfile, AdminProfile, Presentation
from .forms import StudentProfileUpdateForm

from .forms import ContactMessageForm
from .models import ContactMessage, Podcast
from .models import LearningVideo
from .models import LearningModuleRating
from .models import LearningModuleRating
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LearningModuleRating
from django.contrib.auth.decorators import login_required
from .models import LearningModuleRating

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PrivateMessageForm

from .models import PrivateMessage, CourseContent
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.decorators import login_required


import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from GitExercises.models import StudentGitCommandProgress


from django.shortcuts import render, redirect
from GitExercises.models import GitSentence, GitHubSentence, Terminal_Exercises_Git_Commands, StudentGitCommandProgress, \
    StudentJenkinsQuizExercise, JenkinsConceptsQuiz
from .forms import GitSentenceForm, GitHubSentenceForm, TerminalExercisesGitCommandsForm

from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
# Create your views here.


def index(request):
    return render(request, 'index.html')


def terms_view(request):
    return render(request, 'RegisterAndLogin/terms.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = request.POST.get("role")

            if User.objects.filter(email=user.email).exists():
                msg = 'כתובת הדואר האלקטרוני כבר רשומה במערכת, אנא השתמש/י בכתובת אחרת'
                return render(request, 'RegisterAndLogin/register.html', {'form': form, 'msg': msg})

            if User.objects.filter(username=user.username).exists():
                msg = 'שם המשתמש כבר קיים במערכת, אנא בחר/י שם משתמש אחר'
                return render(request, 'RegisterAndLogin/register.html', {'form': form, 'msg': msg})

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
                request.session['username'] = user.username
                return redirect('student_extra')

            if role == "lecturer":
                user.is_lecturer = True
                user.is_active = False
                msg = 'בקשתך לחשבון מרצה התקבלה ונמצאת בתהליך אישור. עדכון בנוגע לסטטוס הבקשה יישלח לכתובת הדואר האלקטרוני שציינת'

            user.save()
        else:
            msg = 'אנא ודא/י כי כל השדות מולאו כראוי'
    else:
        form = SignUpForm()

    return render(request, 'RegisterAndLogin/register.html', {'form': form, 'msg': msg})


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

                    return render(request, 'RegisterAndLogin/login.html')
            else:
                msg = 'פרטים לא נכונים '

        else:
            msg = 'טופס לא תקין'
    return render(request, 'RegisterAndLogin/login.html', {'form': form, 'msg': msg})


def lecturer(request):
    show_filter = request.GET.get('show')
    if show_filter == 'open':
        contact_messages = ContactMessage.objects.filter(is_resolved=False, category='lecturer').order_by('-created_at')
    else:
        contact_messages = ContactMessage.objects.filter(category='lecturer').order_by('-created_at')

    return render(request, 'LecturerPages/lecturer.html', {'contact_messages': contact_messages, })


def student(request):
    return render(request, 'StudentPages/student.html')


@login_required
@csrf_protect
def admin(request):
    show_filter = request.GET.get('show')
    if show_filter == 'open':
        contact_messages = ContactMessage.objects.filter(is_resolved=False, category__in=['support', 'admin']).order_by(
            '-created_at')
    else:
        contact_messages = ContactMessage.objects.filter(category__in=['support', 'admin']).order_by('-created_at')
    lecturers_requests = User.objects.filter(is_lecturer=True, is_active=False)
    admins_requests = User.objects.filter(is_admin=True, is_active=False) if request.user.is_superuser else None

    context = {
        "lecturers_requests": lecturers_requests,
        "admins_requests": admins_requests,
        'contact_messages': contact_messages,

    }
    return render(request, "AdminPages/admin_page.html", context)


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
    return render(request, "AdminPages/admin_page_admins_section.html", context)


def manage_lecturers(request):
    active_lecturers = User.objects.filter(is_lecturer=True, is_active=True)

    context = {
        "active_lecturers": active_lecturers
    }
    return render(request, "AdminPages/admin_page_lecturers_section.html", context)


def manage_students(request):
    active_students = User.objects.filter(is_student=True, is_active=True)

    context = {
        "active_students": active_students
    }
    return render(request, "AdminPages/admin_page_students_section.html", context)


@login_required
def resolve_request(request, message_id):
    if not request.user.is_admin:
        return redirect('login_view')

    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_resolved = True
    message.save()
    send_mail(
        subject='הפנייה שלך טופלה',
        message=f'שלום {message.student.username}, הפנייה שלך בנושא "{message.subject}" טופלה בהצלחה. תוכל לצפות בעדכון באזור הפניות שלך באתר.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[message.student.email],
        fail_silently=False,
    )
    return redirect('admin')


@login_required
def resolve_lecturer_request(request, message_id):
    if not request.user.is_lecturer:
        return redirect('login_view')

    message = get_object_or_404(ContactMessage, id=message_id)
    if message.category == 'lecturer':  # רק אם הפנייה נשלחה למרצה
        message.is_resolved = True
        message.save()
        send_mail(
            subject='הפנייה שלך טופלה',
            message=f'שלום {message.student.username}, הפנייה שלך בנושא "{message.subject}" טופלה בהצלחה. תוכל לצפות בעדכון באזור הפניות שלך באתר.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message.student.email],
            fail_silently=False,
        )
    return redirect('lecturer')  # תחזיר את המרצה לעמוד שלו אחרי הטיפול


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
    return render(request, "PasswordReset/password_reset.html")


# User = get_user_model()

def student_extra(request):
    msg = None
    if request.method == 'POST':
        institution = request.POST.get("institution")
        target_completion_date = request.POST.get("target_completion_date")

        if not institution or not target_completion_date:
            msg = "יש למלא את כל השדות"
            return render(request, 'RegisterAndLogin/student_extra.html', {'msg': msg})

        username = request.session.get('username')
        if not username:
            msg = "שגיאה בזיהוי המשתמש, נסה להירשם מחדש"
            return render(request, 'RegisterAndLogin/student_extra.html', {'msg': msg})

        user = User.objects.get(username=username)

        profile, created = StudentProfile.objects.get_or_create(user=user)
        profile.institution = institution
        profile.target_completion_date = target_completion_date
        profile.save()

        del request.session['username']

        return redirect('login_view')

    return render(request, 'RegisterAndLogin/student_extra.html')


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

    return render(request, 'StudentPages/student_profile.html', {'profile': profile})


@login_required
def lecturer_profile_view(request):
    user = request.user

    # בדיקה האם המשתמש הוא מרצה
    if not user.is_lecturer:
        return redirect('login_view')

    try:
        profile = user.lecturer_profile
    except LecturerProfile.DoesNotExist:
        profile = None

    return render(request, 'LecturerPages/lecturer_profile.html', {'profile': profile})


@login_required
def update_student_profile(request):
    user = request.user
    if not user.is_student:
        return redirect('login_view')  # למניעת גישה ממי שאינו סטודנט

    profile = user.student_profile

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            return redirect('student_profile')
    else:
        form = StudentProfileUpdateForm(instance=profile, user=user)

    return render(request, 'StudentPages/update_student_profile.html', {'form': form})


@login_required
def contact_us(request):
    user = request.user
    if not user.is_student:
        return redirect('login_view')  # רק סטודנטים יכולים לשלוח פנייה

    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.student = user
            message.save()
            return redirect('student')  # דף הצלחה
    else:
        form = ContactMessageForm()

    return render(request, 'contact_us.html', {'form': form})


@login_required
def student_messages_view(request):
    student = request.user
    messages = ContactMessage.objects.filter(student=student).order_by('-created_at')
    return render(request, 'StudentPages/student_contact_messages.html', {'messages': messages})


@login_required
def learning_home(request):
    if not request.user.is_student:
        return redirect('login_view')
    visible_modules = []
    for content in CourseContent.objects.all():
        if content.visibility_mode == 'immediate':
            visible_modules.append(content.module)
    return render(request, 'learning_modules/learning_modules_homePage.html', {'visible_modules': visible_modules})


# @login_required
# def git_module_view(request):
#   git_sentences = list(GitSentence.objects.all())
#  github_sentences = list(GitHubSentence.objects.all())

# Combine and shuffle the sentences
# all_sentences = git_sentences + github_sentences
# random.shuffle(all_sentences)

# context = {
#   'all_sentences': all_sentences,
# }
# return render(request, 'learning_modules/git_module.html', context)

@login_required
def git_module_view(request):
    git_sentences = list(GitSentence.objects.all())
    github_sentences = list(GitHubSentence.objects.all())

    from django.db.models import Q
    try:
        CurrentStudentGitCommandProgress = StudentGitCommandProgress.objects.filter(
            student=request.user.student_profile)
        categorized_commands = {
            'basic': CurrentStudentGitCommandProgress.filter(command__level='basic'),
            'branches': CurrentStudentGitCommandProgress.filter(command__level='branches'),
            'advanced': CurrentStudentGitCommandProgress.filter(command__level='advanced'),

        }
    except StudentProfile.DoesNotExist:
        categorized_commands = {
            'basic': [],
            'branches': [],
            'advanced': [],
        }
    # Combine and shuffle the sentences
    all_sentences = git_sentences + github_sentences
    random.shuffle(all_sentences)

    CurrentStudentGitCommandProgress = StudentGitCommandProgress.objects.filter(
        student=request.user.student_profile)

    podcasts = []
    presentations = []
    # שילוב לתרגול
    all_sentences = git_sentences + github_sentences
    random.shuffle(all_sentences)

    # שליפת הסרטון לפי השלב, גם במצב נגיש
    step = request.GET.get('step')
    video = None
    if step in ['1', '2', '3', '4']:
        video = LearningVideo.objects.filter(module='Git', order=int(step)).first()
        podcasts = Podcast.objects.filter(module='Git', order=int(step))  # 🟢
        presentations = Presentation.objects.filter(module='Git', order=int(step))

    context = {
        'all_sentences': all_sentences,
        'basic_git_terminal_commands': categorized_commands['basic'],
        'branches_git_terminal_commands': categorized_commands['branches'],
        'advanced_git_terminal_commands': categorized_commands['advanced'],
        'git_terminal_commands': CurrentStudentGitCommandProgress,
        'video': video,
        'podcasts': podcasts,
        'presentations': presentations,
        'visible_modules': ['git', 'jenkins', 'docker'],
    }

    return render(request, 'learning_modules/git_module.html', context)


@login_required
def jenkins_module_view(request):
    student_jenkins_quiz_exercise = StudentJenkinsQuizExercise.objects.filter(student=request.user.student_profile)

    podcasts = []
    presentations = []
    # שליפת סרטון ופודקאסט לפי שלב (step)
    step = request.GET.get('step')
    video = None
    if step in ['1', '2', '3', '4']:
        video = LearningVideo.objects.filter(module='Jenkins', order=int(step)).first()
        podcasts = Podcast.objects.filter(module='Jenkins', order=int(step))
        presentations = Presentation.objects.filter(module='Jenkins', order=int(step))

    context = {
        'video': video,
        'podcasts': podcasts,
        'presentations': presentations,
        'visible_modules': ['git', 'jenkins', 'docker'],
        'student_jenkins_quiz_exercise': student_jenkins_quiz_exercise,
    }

    return render(request, 'learning_modules/jenkins_module.html', context)


@login_required
def docker_module_view(request):
    podcasts = []
    presentations = []

    # שליפת סרטון ופודקאסט לפי שלב (step)
    step = request.GET.get('step')
    video = None
    if step in ['1', '2', '3']:
        video = LearningVideo.objects.filter(module='Docker', order=int(step)).first()
        podcasts = Podcast.objects.filter(module='Docker', order=int(step))
        presentations = Presentation.objects.filter(module='Docker', order=int(step))

    context = {
        'video': video,
        'podcasts': podcasts,
        'presentations': presentations,
        'visible_modules': ['git', 'jenkins', 'docker'],
    }

    return render(request, 'learning_modules/docker_module.html', context)


def manage_tasks_and_check_assignments(request):
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/manage_tasks_and_check_assignments.html')


def Lecturer_manage_git(request):
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_git.html')


def Lecturer_manage_jenkins(request):
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_jenkins.html')


def Lecturer_manage_docker(request):
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/Lecturer_manage_docker.html')


def GitSection1(request):
    git_sentences = GitSentence.objects.all()
    github_sentences = GitHubSentence.objects.all()

    git_form = GitSentenceForm()
    github_form = GitHubSentenceForm()

    context = {
        'Git_sentences': git_sentences,
        'GitHub_sentences': github_sentences,
        'git_form': git_form,
        'github_form': github_form,
    }
    if request.method == 'POST':
        if 'add_git_sentence' in request.POST:
            new_sentence = request.POST.get('new_git_sentence')
            if new_sentence:  # Ensure the input is not empty
                GitSentence.objects.create(sentence=new_sentence)

        elif 'add_github_sentence' in request.POST:
            new_sentence = request.POST.get('new_github_sentence')
            if new_sentence:  # Ensure the input is not empty
                GitHubSentence.objects.create(sentence=new_sentence)

        elif 'update_git_sentence' in request.POST:
            sentence_id = request.POST.get('git_sentence_id')
            new_sentence = request.POST.get('updated_git_sentence')
            if new_sentence:
                GitSentence.objects.filter(id=sentence_id).update(sentence=new_sentence)

        elif 'update_github_sentence' in request.POST:
            sentence_id = request.POST.get('github_sentence_id')
            new_sentence = request.POST.get('updated_github_sentence')
            if new_sentence:
                GitHubSentence.objects.filter(id=sentence_id).update(sentence=new_sentence)

        elif 'delete_git_sentence' in request.POST:
            sentence_id = request.POST.get('git_sentence_id')
            GitSentence.objects.filter(id=sentence_id).delete()

        elif 'delete_github_sentence' in request.POST:
            sentence_id = request.POST.get('github_sentence_id')
            GitHubSentence.objects.filter(id=sentence_id).delete()

    return render(request, 'LecturerPages/LecturerTasksAndAssignments/GitSection1.html', context)


def GitSection2(request):
    Terminal_Exercises = Terminal_Exercises_Git_Commands.objects.all()

    Terminal_Exercises_form = TerminalExercisesGitCommandsForm()

    levels = Terminal_Exercises_Git_Commands.LEVELS

    context = {
        'Terminal_Exercises': Terminal_Exercises,
        'Terminal_Exercises_form': Terminal_Exercises_form,
        'levels': levels,
    }
    if request.method == 'POST':
        if 'add_terminal_exercise' in request.POST:
            exercise_id = request.POST.get('exercise_id')
            command = request.POST.get('command')
            description = request.POST.get('description_en')
            Hebrew_Command = request.POST.get('Hebrew_Command')
            git_feedback = request.POST.get('feedback')
            git_command_scenario = request.POST.get('scenario')
            Hebrew_Description = request.POST.get('description_he')
            level = request.POST.get('level')

            if command and description and Hebrew_Description and Hebrew_Command and git_feedback and git_command_scenario:  # Ensure the input is not empty
                Terminal_Exercises_Git_Commands.objects.create(
                    command=command,
                    Hebrew_Command=Hebrew_Command,
                    English_Description=description,
                    Hebrew_Description=Hebrew_Description,
                    git_feedback=git_feedback,
                    git_command_scenario=git_command_scenario,
                    level=level
                )

        elif 'update_terminal_exercise' in request.POST:
            exercise_id = request.POST.get('exercise_id')
            try:
                exercise = Terminal_Exercises_Git_Commands.objects.get(id=exercise_id)
                exercise.command = request.POST.get('command')
                exercise.Hebrew_Description = request.POST.get('description_he')
                exercise.English_Description = request.POST.get('description_en')
                exercise.git_feedback = request.POST.get('feedback')
                exercise.git_command_scenario = request.POST.get('scenario')
                exercise.level = request.POST.get('level')
                exercise.save()
            except Terminal_Exercises_Git_Commands.DoesNotExist:
                pass  # Handle the case where the exercise does not exist

    elif 'delete_terminal_exercise' in request.POST:
        exercise_id = request.POST.get('exercise_id')
        Terminal_Exercises_Git_Commands.objects.filter(id=exercise_id).delete()

    return render(request, 'LecturerPages/LecturerTasksAndAssignments/GitSection2.html', context)


def JenkinsSection(request):
    JenkinsConceptsQuizs = JenkinsConceptsQuiz.objects.all()
    JenkinsConceptsQuizs_form = JenkinsConceptsQuizForm()

    if request.method == 'POST':
        if 'add_question' in request.POST:
            question = request.POST.get('question')
            answer1 = request.POST.get('answer1')
            answer2 = request.POST.get('answer2')
            answer3 = request.POST.get('answer3')
            answer4 = request.POST.get('answer4')
            correct_answer = request.POST.get('correct_answer')

            if question and answer1 and answer2 and answer3 and answer4 and correct_answer:  # Ensure the input is not empty
                JenkinsConceptsQuiz.objects.create(
                    question=question,
                    option1=answer1,
                    option2=answer2,
                    option3=answer3,
                    option4=answer4,
                    answer=correct_answer
                )
        elif 'update_question' in request.POST:
            question_id = request.POST.get('question_id')
            try:
                question = JenkinsConceptsQuiz.objects.get(id=question_id)
                question.question = request.POST.get('question')
                question.option1 = request.POST.get('answer1')
                question.option2 = request.POST.get('answer2')
                question.option3 = request.POST.get('answer3')
                question.option4 = request.POST.get('answer4')
                question.answer = request.POST.get('correct_answer')
                question.save()
            except JenkinsConceptsQuiz.DoesNotExist:
                pass
        elif 'delete_question' in request.POST:
            question_id = request.POST.get('question_id')
            JenkinsConceptsQuiz.objects.filter(id=question_id).delete()
    context = {
        'JenkinsConceptsQuiz': JenkinsConceptsQuizs,
        'JenkinsConceptsQuizs_form': JenkinsConceptsQuizs_form,

    }
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/JenkinsSection.html', context)


def DockerSection(request):
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/DockerSection.html')


@login_required
def git_section1(request):
    video = LearningVideo.objects.filter(module='Git', order=1).first()
    return render(request, 'learning_modules/git/section1.html', {'video': video})


@login_required
def git_section2(request):
    video = LearningVideo.objects.filter(module='Git', order=2).first()
    return render(request, 'learning_modules/git/section2.html', {'video': video})


@login_required
def git_section3(request):
    video = LearningVideo.objects.filter(module='Git', order=3).first()
    return render(request, 'learning_modules/git/section3.html', {'video': video})


@login_required
def git_section4(request):
    video = LearningVideo.objects.filter(module='Git', order=4).first()
    return render(request, 'learning_modules/git/section4.html', {'video': video})


@login_required
def jenkins_section1(request):
    video = LearningVideo.objects.filter(module='Jenkins', order=1).first()
    return render(request, 'learning_modules/jenkins/section1.html', {'video': video})


@login_required
def jenkins_section2(request):
    video = LearningVideo.objects.filter(module='Jenkins', order=2).first()
    return render(request, 'learning_modules/jenkins/section2.html', {'video': video})


@login_required
def jenkins_section3(request):
    video = LearningVideo.objects.filter(module='Jenkins', order=3).first()
    return render(request, 'learning_modules/jenkins/section3.html', {'video': video})


@login_required
def jenkins_section4(request):
    video = LearningVideo.objects.filter(module='Jenkins', order=4).first()
    return render(request, 'learning_modules/jenkins/section4.html', {'video': video})


@login_required
def docker_section1(request):
    video = LearningVideo.objects.filter(module='Docker', order=1).first()
    return render(request, 'learning_modules/docker/section1.html', {'video': video})


@login_required
def docker_section2(request):
    video = LearningVideo.objects.filter(module='Docker', order=2).first()
    return render(request, 'learning_modules/docker/section2.html', {'video': video})


@login_required
def docker_section3(request):
    video = LearningVideo.objects.filter(module='Docker', order=3).first()
    return render(request, 'learning_modules/docker/section3.html', {'video': video})


#
# @login_required
# def rate_learning_modules(request):
#     if not request.user.is_student:
#         return redirect('login_view')
#
#     all_modules = ['Git', 'Jenkins', 'Docker']
#     existing_ratings = LearningModuleRating.objects.filter(student=request.user)
#
#     if request.method == 'POST':
#         for module in all_modules:
#             rating_value = request.POST.get(f'rating_{module}')
#             if rating_value:
#                 LearningModuleRating.objects.update_or_create(
#                     student=request.user,
#                     module_title=module,
#                     defaults={'rating': rating_value}
#                 )
#         return render(request, 'learning_modules/thank_you.html')
#
#     return render(request, 'learning_modules/rate_learning_modules.html', {
#         'existing_ratings': existing_ratings,
#         'all_modules': all_modules,
#     })


@login_required
def rate_learning_modules(request):
    if not request.user.is_student:
        return redirect('login_view')

    if request.method == 'POST':
        git_rating = request.POST.get('git_rating')
        git_comment = request.POST.get('git_comment')

        jenkins_rating = request.POST.get('jenkins_rating')
        jenkins_comment = request.POST.get('jenkins_comment')

        docker_rating = request.POST.get('docker_rating')
        docker_comment = request.POST.get('docker_comment')

        # יצירת מופעים רק אם המשתמש דירג משהו בפועל
        if git_rating:
            LearningModuleRating.objects.create(
                student=request.user,
                module_name='Git',
                rating=int(git_rating),
                comment=git_comment,
                submitted_at=timezone.now()
            )

        if jenkins_rating:
            LearningModuleRating.objects.create(
                student=request.user,
                module_name='Jenkins',
                rating=int(jenkins_rating),
                comment=jenkins_comment,
                submitted_at=timezone.now()
            )

        if docker_rating:
            LearningModuleRating.objects.create(
                student=request.user,
                module_name='Docker',
                rating=int(docker_rating),
                comment=docker_comment,
                submitted_at=timezone.now()
            )

        return render(request, 'thank_you.html')  # עמוד תודה פשוט

    return render(request, 'learning_modules/rate_learning_modules.html')


def is_lecturer(user):
    return user.is_authenticated and hasattr(user, 'lecturer_profile')


@login_required
@user_passes_test(is_lecturer)
def view_module_ratings(request):
    ratings = LearningModuleRating.objects.select_related('student').all().order_by('-submitted_at')
    return render(request, 'view_module_ratings.html', {'ratings': ratings})


# @login_required
# def view_module_ratings(request):
#   ratings = LearningModuleRating.objects.all()
#  return render(request, 'view_module_ratings.html', {'ratings': ratings})


# @login_required
# def view_module_ratings(request):
#   ratings = LearningModuleRating.objects.all()
#  return render(request, 'view_module_ratings.html', {'ratings': ratings})


def is_lecturer(user):
    return user.is_authenticated and user.is_lecturer


@login_required
@user_passes_test(is_lecturer)
def send_private_message(request):
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return render(request, 'messages/success.html', {'student_name': message.recipient.get_full_name()})
    else:
        form = PrivateMessageForm()

    return render(request, 'messages/send_message.html', {'form': form})


@login_required
def view_my_messages(request):
    messages = PrivateMessage.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'messages/view_messages.html', {'messages': messages})


def student_modules_view(request):
    visible_modules = []
    for content in CourseContent.objects.all():
        if content.visibility_mode == 'immediate':
            visible_modules.append(content.module)
    return render(request, 'learning_modules/learning_modules_homePage.html', {'visible_modules': visible_modules})


@login_required
def lecturer_manage_content(request):
    contents = CourseContent.objects.all()
    return render(request, 'LecturerPages/LecturerTasksAndAssignments/lecturer_content_manage.html',
                  {'contents': contents})


@login_required
def update_module_visibility(request, content_id):
    if request.method == 'POST':
        content = get_object_or_404(CourseContent, id=content_id)
        visibility_mode = request.POST.get('visibility_mode')
        if visibility_mode in ['immediate', 'hidden']:
            content.visibility_mode = visibility_mode
            content.save()
    return redirect('lecturer_manage_content')


@login_required
@user_passes_test(is_lecturer)
def monitor_student_git_progress(request):
    data = StudentGitCommandProgress.objects.select_related('student__user', 'command').values(
        'student__user__username', 'command__command', 'completed', 'attempts'
    )

    df = pd.DataFrame(data)
    student_list = df['student__user__username'].unique().tolist() if not df.empty else []
    selected_student = request.GET.get('student') or (student_list[0] if student_list else None)
    filter_option = request.GET.get('table_filter')  # Use distinct filter name for table only

    pie_chart = bar_graph = None
    summary_data = []

    if not df.empty:
        df_grouped = df.groupby(['student__user__username']).agg(
            total_attempts=('attempts', 'sum'),
            total_completed=('completed', 'sum'),
        )
        df_grouped['avg_attempts'] = df_grouped['total_attempts'] / df_grouped['total_completed'].replace(0, 1)
        df_grouped = df_grouped.reset_index()

        # Filtering table data only
        if filter_option == 'best':
            df_grouped = df_grouped[(df_grouped['avg_attempts'] <= 2.5) & (df_grouped['avg_attempts'] != 0)]
        elif filter_option == 'struggle':
            df_grouped = df_grouped[(df_grouped['avg_attempts'] >= 2.5) | (df_grouped['avg_attempts'] == 0)]

        summary_data = df_grouped.to_dict('records')

        # Bar Graph for selected student
        if selected_student:
            student_df = df[df['student__user__username'] == selected_student]
            plt.figure(figsize=(8, 4))
            plt.bar(student_df['command__command'], student_df['attempts'], color='steelblue')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('attempts')
            plt.title(f'progress of {selected_student}')
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            bar_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # Pie Chart
            completed = student_df['completed'].sum()
            total = len(student_df)
            not_completed = total - completed
            plt.figure()
            plt.pie([completed, not_completed], labels=['completed', 'not completed'], autopct='%1.1f%%', colors=['green', 'red'])
            plt.title(f'complete commands of {selected_student}')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            pie_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

    context = {
        'student_list': student_list,
        'selected_student': selected_student,
        'filter': filter_option,
        'pie_chart': pie_chart,
        'bar_graph': bar_graph,
        'summary': summary_data
    }
    return render(request, 'LecturerPages/monitor_student_progress.html', context)


@login_required
@user_passes_test(is_lecturer)
def download_student_report(request):
    filter_option = request.POST.get('filter')  # Make sure to get from POST

    data = StudentGitCommandProgress.objects.select_related('student__user', 'command').values(
        'student__user__username', 'command__command', 'completed', 'attempts'
    )
    df = pd.DataFrame(data)
    df_grouped = df.groupby(['student__user__username']).agg(
        total_attempts=('attempts', 'sum'),
        total_completed=('completed', 'sum')
    )
    df_grouped['avg_attempts'] = df_grouped['total_attempts'] / df_grouped['total_completed'].replace(0, 1)
    df_grouped = df_grouped.reset_index()

    if filter_option == 'best':
        df_grouped = df_grouped[df_grouped['avg_attempts'] <= 2.5]
    elif filter_option == 'struggle':
        df_grouped = df_grouped[df_grouped['avg_attempts'] > 2.5]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_git_progress_report.csv"'
    df_grouped.to_csv(path_or_buf=response, index=False)
    return response



