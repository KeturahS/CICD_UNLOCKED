from django.core.management.base import BaseCommand
from App_SetUp.models import StudentProfile
from GitExercises.models import StudentJenkinsPipelineExercise, JenkinsPipelineStage

class Command(BaseCommand):
    help = "Populate StudentJenkinsPipelineExercise for all students and assign all stages"

    def handle(self, *args, **kwargs):
        students = StudentProfile.objects.all()
        stages = JenkinsPipelineStage.objects.all()
        for student in students:
            exercise, created = StudentJenkinsPipelineExercise.objects.get_or_create(student=student)
            if created:
                exercise.stages.set(stages)  # Assign all stages to the exercise
        self.stdout.write(self.style.SUCCESS("Successfully populated StudentJenkinsPipelineExercise for all students."))