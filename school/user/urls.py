from django.urls import path
from . import views

urlpatterns = [
    path('create_program', views.create_program, name='create_program'),  # register/create_program
    path('programs', views.ProgramView.as_view(), name='programs'),  # register/programs
    path('programs/<pk>', views.ProgramUpdateView.as_view(), name='program'),  # register/programs/4
    path('programs/<pk>/create_task', views.test_create, name='create_task'),  # register/programs/4/create_task
    path('programs/<pk>/<test_pk>', views.get_answer, name = 'get_answer'),
    path('student/programs', views.Programs, name = 'my_school')
]