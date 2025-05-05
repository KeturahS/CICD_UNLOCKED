from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# מודל משתמש מותאם אישית
class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_student = models.BooleanField('Is student', default=False)
    is_lecturer = models.BooleanField('Is lecturer', default=False)

# פרופיל סטודנט
class StudentProfile(models.Model):
    INSTITUTION_CHOICES = [
        ('SCE', 'SCE - המכללה האקדמית להנדסה ע"ש סמי שמעון'),
        ('TAU', 'אוניברסיטת תל אביב'),
        ('HUJI', 'האוניברסיטה העברית בירושלים'),
        ('TECH', 'הטכניון'),
        ('BIU', 'אוניברסיטת בר אילן'),
        ('BGU', 'אוניברסיטת בן גוריון'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    institution = models.CharField('Institution', max_length=255, choices=INSTITUTION_CHOICES)
    target_completion_date = models.DateField('Target completion date', blank=True, null=True)

    def __str__(self):
        return f"Student Profile of {self.user.username}"

# פרופיל מרצה
class LecturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lecturer_profile")

    def __str__(self):
        return f"Lecturer Profile of {self.user.username}"

# פרופיל מנהל
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")

    def __str__(self):
        return f"Admin Profile of {self.user.username}"

# טופס יצירת קשר
class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('support', 'תמיכה טכנית'),
        ('lecturer', 'פנייה למרצה'),
        ('admin', 'פנייה להנהלה'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.category})"

# דירוג לומדה
class LearningModuleRating(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} - {self.module_name} ({self.rating}★)"
