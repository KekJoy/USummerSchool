from django.urls import path
from .views import create_program

urlpatterns = [
    path('create_program', create_program, name = 'create_program'),

]