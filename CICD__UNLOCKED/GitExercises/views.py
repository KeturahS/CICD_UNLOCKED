# GitExercises/views.py
from django.shortcuts import render, redirect

from GitExercises.models import StudentGitCommandProgress

from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from .models import PipelineTemplate, StudentPipelineAttempt

logger = logging.getLogger(__name__)
from App_SetUp.models import User


@login_required
def update_command_status(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        if command:
            try:
                # Log the user object for debugging
                logger.debug(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

                # Check if the user has a student_profile
                if not hasattr(request.user, 'student_profile'):
                    messages.error(request, "You do not have a student profile.")
                    return redirect('GitScenarioExercise')

                # Update the completed status for the command
                progress = StudentGitCommandProgress.objects.get(
                    command__command=command,
                    student=request.user.student_profile
                )
                progress.completed = True
                progress.attempts += 1
                progress.save()
                messages.success(request, "Command status updated successfully.")
                return redirect('GitScenarioExercise')
            except StudentGitCommandProgress.DoesNotExist:
                messages.error(request, "Command not found.")
                return redirect('GitScenarioExercise')
    messages.error(request, "Invalid request.")
    return redirect('GitScenarioExercise')


@login_required
def update_command_attempts_status(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        if command:
            try:
                # Check if the user has a student_profile
                if not hasattr(request.user, 'student_profile'):
                    return redirect('GitScenarioExercise')

                # Update the attempts for the command
                progress = StudentGitCommandProgress.objects.get(
                    command__command=command,
                    student=request.user.student_profile
                )
                progress.attempts += 1
                progress.save()
                return redirect('GitScenarioExercise')
            except StudentGitCommandProgress.DoesNotExist:
                return redirect('GitScenarioExercise')
    return redirect('GitScenarioExercise')


def GitExercise1_view(request):
    return render(request, 'GitExercises/section1_questions.html')


# Create your views here.
def GitExercise2_view(request):
    return render(request, 'GitExercises/section2_questions.html')


def GitScenarioExercise(request):
    PersonalGitScenarioExercise = StudentGitCommandProgress.objects.filter(student=request.user.student_profile,
                                                                           completed=False)
    context = {
        'PersonalGitScenarioExercise': PersonalGitScenarioExercise,
    }
    return render(request, 'GitExercises/GitScenarioExercise.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import StudentJenkinsQuizExercise

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import StudentJenkinsQuizExercise


@csrf_exempt  # במידת הצורך בלבד
@login_required
def update_jenkins_quiz_completion(request):
    if request.method == 'POST':
        question_ids = request.POST.get('correct_question_ids', '')
        id_list = [int(qid) for qid in question_ids.split(',') if qid.isdigit()]
        print("DEBUG question_ids:", question_ids)
        print("DEBUG id_list:", id_list)

        StudentJenkinsQuizExercise.objects.filter(student=request.user.student_profile).update(
            completed=False)

        for qid in id_list:
            quiz_status = StudentJenkinsQuizExercise.objects.filter(
                student=request.user.student_profile,
                quiz_id=qid
            ).first()

            if quiz_status:
                print(f"✅ FOUND: Question ID {qid}, marking completed")
                quiz_status.completed = True
                quiz_status.save()
            else:
                print(
                    f"❌ NOT FOUND: No StudentJenkinsQuizExercise for student={request.user.student_profile} and quiz_id={qid}")
        # חזרה לדף ממנו הגיע המשתמש
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')


from App_SetUp.models import StudentProfile
from django.shortcuts import render


def jenkins_questions_view(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        first_name = student_profile.user.first_name
    except StudentProfile.DoesNotExist:
        first_name = request.user.first_name or request.user.username

    pipeline = get_random_unsolved_pipeline(request.user)
    has_more_pipelines = pipeline is not None

    return render(request, 'JenkinsExercises/jenkins_questions.html', {
        'student_name': first_name,
        'pipeline': pipeline,
        'has_more_pipelines': has_more_pipelines
    })


import re


def validate_pipeline(code):
    if not code:
        return False

    normalized = " ".join(code.lower().split())

    patterns = [
        r'pipeline\s*{',
        r'stages\s*{',
        r'stage\s*\(\s*[\'"]build[\'"]\s*\)\s*{[^}]*steps\s*{',
        r'stage\s*\(\s*[\'"]test[\'"]\s*\)\s*{[^}]*steps\s*{',
    ]
    wrong_keywords = [r'\b(step|stjeps|stepp|speps|sreps)\s*{']

    if not all(re.search(p, normalized) for p in patterns):
        return False
    if any(re.search(wk, normalized) for wk in wrong_keywords):
        return False

    if code.count("{") != code.count("}"):
        return False

    return True


def get_random_unsolved_pipeline(user):
    solved_ids = StudentPipelineAttempt.objects.filter(
        student=user, is_solved=True
    ).values_list('pipeline_id', flat=True)

    available = PipelineTemplate.objects.exclude(id__in=solved_ids)

    if available.exists():
        return available.order_by('?').first()  # פייפ רנדומלי
    return None


def handle_pipeline_submission(request):
    if request.method == 'POST':
        pipeline_id = request.POST.get('pipeline_id')
        code = request.POST.get('code')
        is_valid = validate_pipeline(code)

        attempt, created = StudentPipelineAttempt.objects.get_or_create(
            student=request.user,
            pipeline_id=pipeline_id,
            defaults={'attempts': 0}
        )
        attempt.attempts += 1
        attempt.last_submitted_code = code
        if is_valid:
            attempt.is_solved = True
        attempt.save()

        # 🔁 לאחר ההגשה – מפנה חזרה לעמוד התרגול
        return redirect('jenkins_questions')
