from django import forms
from .models import ProgramList, TaskList
from django.forms import ModelForm, TextInput, Textarea


class ProgramCreationForm(forms.ModelForm):
    class Meta:
        model = ProgramList
        fields = {'title'}


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = {'title',
                  'description'}
