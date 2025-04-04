from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_student = models.BooleanField('Is student', default=False)
    is_lecturer = models.BooleanField('Is lecturer', default=False)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    institution = models.CharField('Institution', max_length=255)
    target_completion_date = models.DateField('Target completion date', blank=True, null=True)

    def __str__(self):
        return f"Student Profile of {self.user.username}"

class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer_profile")

    def __str__(self):
        return f"Lecturer Profile of {self.user.username}"


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")

    def __str__(self):
        return f"Lecturer Profile of {self.user.username}"
