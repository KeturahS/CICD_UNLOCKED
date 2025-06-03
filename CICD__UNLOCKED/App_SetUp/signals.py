from django.db.models.signals import pre_save, post_save

from .models import User, LecturerProfile, StudentProfile, AdminProfile

# File: App_SetUp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from App_SetUp.models import StudentProfile

# app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    StudentProfile,
    LearningVideo,
    Podcast,
    Presentation,
    StudentModuleProgress,
    StudentVideoCompletion,
    StudentPresentationCompletion
)
from django.db import transaction

from GitExercises.models import Terminal_Exercises_Git_Commands



@receiver(pre_save, sender=User)
def store_previous_status(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an existing user (not a new one)
        prev_instance = User.objects.get(pk=instance.pk)
        instance._previous_is_active = prev_instance.is_active
    else:
        instance._previous_is_active = None  # For new users


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if hasattr(instance,
               '_previous_is_active') and not instance._previous_is_active and instance.is_active and instance.is_student:
        StudentProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def create_lecturer_profile(sender, instance, created, **kwargs):
    if created:
        return

    if hasattr(instance,
               '_previous_is_active') and not instance._previous_is_active and instance.is_active and instance.is_lecturer:
        LecturerProfile.objects.get_or_create(user=instance)


# Create an AdminProfile only if the user became active
@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        return

    if hasattr(instance,
               '_previous_is_active') and not instance._previous_is_active and instance.is_active and instance.is_admin:
        AdminProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=StudentProfile)
def create_student_completions(sender, instance, created, **kwargs):
    if created:
        student = instance
        # Modules

        modules = ['Git', 'Jenkins', 'Docker']
        for module in modules:
            StudentModuleProgress.objects.get_or_create(student=student, module=module)

        # Videos
        for video in LearningVideo.objects.all():
            StudentVideoCompletion.objects.get_or_create(student=student, video=video)

        # Presentations
        for presentation in Presentation.objects.all():
            StudentPresentationCompletion.objects.get_or_create(student=student, presentation=presentation)


