from .models import LogoSettings

def logo_settings_context(request):
    logo_settings = LogoSettings.objects.first()

    background_color = "#2b2b3c"
    user = request.user
    if user.is_authenticated:
        if hasattr(user, 'is_admin') and user.is_admin:
            background_color = "#0a0e1a"
        elif hasattr(user, 'is_lecturer') and user.is_lecturer:
            background_color = "#0a0e1a"
        elif hasattr(user, 'is_student') and user.is_student:
            background_color = "#0a0e1a"

    return {
        'logo_settings': logo_settings,
        'background_color': background_color
    }
