from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from .models import StudentProfile
from .models import ContactMessage
from django.core.exceptions import ValidationError
from datetime import date
from GitExercises.models import GitHubSentence, GitSentence, Terminal_Exercises_Git_Commands


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
                ,
                "autocomplete": "off"
            }
        )
    )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
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
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_admin', 'is_lecturer', 'is_student')

class StudentExtraForm(forms.Form):
    INSTITUTION_CHOICES = [
        ('SCE', 'SCE - המכללה האקדמית להנדסה ע"ש סמי שמעון'),
        ('TAU', 'אוניברסיטת תל אביב'),
        ('HUJI', 'האוניברסיטה העברית בירושלים'),
        ('TECH', 'הטכניון'),
        ('BIU', 'אוניברסיטת בר אילן'),
        ('BGU', 'אוניברסיטת בן גוריון'),
    ]
    institution = forms.ChoiceField(label="מוסד לימודים", choices=INSTITUTION_CHOICES)
    target_completion_date = forms.DateField(
        label="תאריך סיום קורס",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    agree_terms = forms.BooleanField(label="אני מאשר את תנאי השימוש", required=True)

    def clean_course_completion_date(self):
        data = self.cleaned_data['target_completion_date']
        if data < date.today():
            raise ValidationError("תאריך הסיום לא יכול להיות בעבר")
        return data

User = get_user_model()
class StudentProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='שם פרטי', max_length=30)
    last_name = forms.CharField(label='שם משפחה', max_length=30)
    email = forms.EmailField(label='אימייל')

    class Meta:
        model = StudentProfile
        fields = ['institution', 'target_completion_date', 'first_name', 'last_name', 'email']
        widgets = {
            'target_completion_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # אתחול שדות המשתמש
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

    def clean_target_completion_date(self):
        target_date = self.cleaned_data.get('target_completion_date')
        if target_date and target_date < date.today():
            raise ValidationError("תאריך הסיום לא יכול להיות תאריך מהעבר")
        return target_date
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



class GitSentenceForm(forms.ModelForm):
    class Meta:
        model = GitSentence
        fields = ['sentence']

class GitHubSentenceForm(forms.ModelForm):
    class Meta:
        model = GitHubSentence
        fields = ['sentence']

class TerminalExercisesGitCommandsForm(forms.ModelForm):
    class Meta:
        model = Terminal_Exercises_Git_Commands
        fields = ['command', 'English_Description','Hebrew_Description', 'git_feedback', 'git_command_scenario', 'level']