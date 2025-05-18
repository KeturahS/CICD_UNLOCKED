# GitExercises/views.py
from django.shortcuts import render, redirect

from GitExercises.models import StudentGitCommandProgress



from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

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

