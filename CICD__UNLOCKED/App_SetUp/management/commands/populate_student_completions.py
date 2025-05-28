from django.core.management.base import BaseCommand
from App_SetUp.models import (
    StudentProfile,
    LearningVideo,
    Podcast,
    Presentation,
    StudentModuleProgress,
    StudentVideoCompletion,
    StudentPodcastCompletion,
    StudentPresentationCompletion
)

class Command(BaseCommand):
    help = "Populate module progress and completion tables for all existing students"

    def handle(self, *args, **kwargs):
        modules = ['Git', 'Jenkins', 'Docker']

        students = StudentProfile.objects.all()
        videos = LearningVideo.objects.all()
        podcasts = Podcast.objects.all()
        presentations = Presentation.objects.all()

        created_count = 0

        for student in students:
            for module in modules:
                obj, created = StudentModuleProgress.objects.get_or_create(student=student, module=module)
                if created:
                    created_count += 1

            for video in videos:
                obj, created = StudentVideoCompletion.objects.get_or_create(student=student, video=video)
                if created:
                    created_count += 1

            for podcast in podcasts:
                obj, created = StudentPodcastCompletion.objects.get_or_create(student=student, podcast=podcast)
                if created:
                    created_count += 1

            for presentation in presentations:
                obj, created = StudentPresentationCompletion.objects.get_or_create(student=student, presentation=presentation)
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Done. {created_count} new records created."))
