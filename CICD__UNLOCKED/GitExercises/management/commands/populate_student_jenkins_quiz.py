from django.core.management.base import BaseCommand
from App_SetUp.models import StudentProfile
from GitExercises.models import JenkinsConceptsQuiz, StudentJenkinsQuizExercise

class Command(BaseCommand):
    help = "Populate StudentJenkinsQuizExercise for all students and quizzes"

    def handle(self, *args, **kwargs):
        students = StudentProfile.objects.all()
        quizzes = JenkinsConceptsQuiz.objects.all()
        for student in students:
            for quiz in quizzes:
                StudentJenkinsQuizExercise.objects.get_or_create(student=student, quiz=quiz)
        self.stdout.write(self.style.SUCCESS("Successfully populated StudentJenkinsQuizExercise for all students and quizzes."))