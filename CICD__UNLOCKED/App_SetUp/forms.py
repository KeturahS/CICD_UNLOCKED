from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from .models import StudentProfile
from .models import ContactMessage

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_lecturer', 'is_student')



User = get_user_model()
class StudentProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='שם פרטי', max_length=30)
    last_name = forms.CharField(label='שם משפחה', max_length=30)
    email = forms.EmailField(label='אימייל')

    class Meta:
        model = StudentProfile
        fields = ['institution', 'target_completion_date', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # אתחול שדות המשתמש
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['category', 'subject', 'message']
        labels = {
            'category': 'נושא הפנייה',
            'subject': 'כותרת',
            'message': 'תוכן הפנייה',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }