from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import forms

from authentication.models import Profile
from django import forms
from .models import TaskAnswer, ProgramList, TaskList


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = {'university',
                  'phone',
                  'first_name',
                  'last_name',
                  'patronymic_name',
                  'university_faculty',
                  'university_specitality',
                  'university_course'}


class TaskSolveForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = {'answer', }

class ProgramCreationForm(forms.ModelForm):
    class Meta:
        model = ProgramList
        fields = {'title'}


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = {'title',
                  'description'}
