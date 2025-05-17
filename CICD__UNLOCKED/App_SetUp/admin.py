from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, StudentProfile, LecturerProfile, AdminProfile, LearningVideo
from .models import ContactMessage, Podcast, Presentation, CourseContent

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


#@admin.register(CourseContent)
#class CourseContentAdmin(admin.ModelAdmin):
#    list_display = ('module_name', 'title', 'visibility_mode', 'scheduled_publish_time', 'owner')
#    list_filter = ('visibility_mode', 'module')
#    search_fields = ('title', 'description')
#    ordering = ('module_name',)
