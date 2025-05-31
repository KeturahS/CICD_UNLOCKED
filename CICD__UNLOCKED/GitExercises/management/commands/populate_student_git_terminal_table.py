from django.core.management.base import BaseCommand
from App_SetUp.models import StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress

class Command(BaseCommand):
    help = "Populate the StudentGitCommandProgress table with all students and commands"

    def handle(self, *args, **kwargs):
        students = StudentProfile.objects.all()
        commands = Terminal_Exercises_Git_Commands.objects.all()

        for student in students:
            for command in commands:
                # Check if the entry already exists
                if not StudentGitCommandProgress.objects.filter(student=student, command=command).exists():
                    StudentGitCommandProgress.objects.create(student=student, command=command)

        self.stdout.write(self.style.SUCCESS("Successfully populated StudentGitCommandProgress table."))