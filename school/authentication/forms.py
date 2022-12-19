from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'university',
                  'phone',
                  'first_name',
                  'last_name',
                  'patronymic_name',
                  'university_faculty',
                  'university_specitality',
                  'university_course',
                  'school_program'}