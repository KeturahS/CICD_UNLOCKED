from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, StudentProfile, LecturerProfile, AdminProfile
from .models import ContactMessage

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)
admin.site.register(AdminProfile)
admin.site.register(ContactMessage)
