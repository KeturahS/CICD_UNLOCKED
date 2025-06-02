from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


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


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"מאת {self.sender.username} אל {self.recipient.username}: {self.subject}"


class LearningVideo(models.Model):
    title = models.CharField(max_length=255)  # שם הסרטון
    youtube_id = models.CharField(max_length=50)  # מזהה YouTube: לדוגמה 'VtjoExU11d4'
    module = models.CharField(max_length=100, choices=[
        ('Git', 'Git'),
        ('Jenkins', 'Jenkins'),
        ('Docker', 'Docker'),
    ])
    description = models.TextField(blank=True)  # תיאור הסרטון
    order = models.PositiveIntegerField(default=0)  # סדר הצגה בתוך המודול

    def __str__(self):
        return f"{self.module} - {self.title}"


class Podcast(models.Model):
    MODULE_CHOICES = [
        ('Git', 'Git'),
        ('Jenkins', 'Jenkins'),
        ('Docker', 'Docker'),
    ]

    title = models.CharField(max_length=255)
    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    audio_file = models.FileField(upload_to='podcasts/')  # נשמור את הקובץ בתיקיית media/podcasts/
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.module})"


class Presentation(models.Model):
    MODULE_CHOICES = [
        ('Git', 'Git'),
        ('Jenkins', 'Jenkins'),
        ('Docker', 'Docker'),
    ]
    module = models.CharField(max_length=20, choices=MODULE_CHOICES)
    title = models.CharField(max_length=200)
    embed_url = models.URLField(help_text="קישור Google Slides עם embed")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.module} - {self.title}"


class CourseContent(models.Model):
    MODULE_CHOICES = [
        ('git', 'Git'),
        ('jenkins', 'Jenkins'),
        ('docker', 'Docker'),
    ]

    module = models.CharField(max_length=20, choices=MODULE_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    visibility_mode = models.CharField(
        max_length=10,
        choices=[('immediate', 'מיידי'), ('hidden', 'מוסתר')],
        default='hidden'
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_visible_to_students(self):
        return self.visibility_mode == 'immediate'

    def __str__(self):
        return f"{self.module} - {self.title}"


class StudentNote(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.module} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class StudentModuleProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='module_progress')
    module = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)
    progress_percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {self.module} - {'Completed' if self.completed else 'In Progress'}"


class StudentVideoCompletion(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='video_completions')
    video = models.ForeignKey(LearningVideo, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'video')

    def __str__(self):
        return f"{self.student.user.username} - {self.video.title} - {'Completed' if self.completed else 'In Progress'}"


class StudentPresentationCompletion(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='presentation_completions')
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'presentation')

    def __str__(self):
        return f"{self.student.user.username} - {self.presentation.title} - {'Completed' if self.completed else 'In Progress'}"

User = get_user_model()

class LecturerToAdminMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

class ServerLoadRecord(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} | CPU: {self.cpu_percent}%"

