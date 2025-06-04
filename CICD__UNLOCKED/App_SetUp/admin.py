from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, StudentProfile, LecturerProfile, AdminProfile, LearningVideo, StudentModuleProgress, \
    StudentVideoCompletion, StudentPresentationCompletion, StudentGeneralProgress
from .models import ContactMessage, Podcast, Presentation, CourseContent, LogoSettings

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)
admin.site.register(AdminProfile)
admin.site.register(ContactMessage)

admin.site.register(LearningVideo)
admin.site.register(Podcast)
admin.site.register(Presentation)
admin.site.register(CourseContent)
admin.site.register(StudentModuleProgress)
admin.site.register(StudentVideoCompletion)
admin.site.register(StudentPresentationCompletion)
admin.site.register(StudentGeneralProgress)
admin.site.register(LogoSettings)



