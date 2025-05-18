from django.db.models.signals import post_save
from django.dispatch import receiver
from App_SetUp.models import StudentProfile
from GitExercises.models import Terminal_Exercises_Git_Commands, StudentGitCommandProgress


# Signal to create StudentGitCommandProgress entries when a new student profile is created
@receiver(post_save, sender=StudentProfile)
def create_student_git_commands(sender, instance, created, **kwargs):
    if created:
        commands = Terminal_Exercises_Git_Commands.objects.all()
        for command in commands:
            StudentGitCommandProgress.objects.create(
                student=instance,
                command=command
            )

# Signal to create StudentGitCommandProgress entries when a new command is added
@receiver(post_save, sender=Terminal_Exercises_Git_Commands)
def create_command_for_all_students(sender, instance, created, **kwargs):
    if created:
        students = StudentProfile.objects.all()
        for student in students:
            StudentGitCommandProgress.objects.create(
                student=student,
                command=instance
            )