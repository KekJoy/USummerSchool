from django.urls import path
from . import views
from .views import home, edit

urlpatterns = [
    path('', views.index, name='account_student'),  # account/ # Главная страница ЛК в зависимости от группы

    path('edit/', views.edit, name='lk_account_student_edit'),  # account/edit/ # Изменение личных данных

    path('programs/', views.ViewPrograms.as_view(), name='lk_account_student_programs'),
    # account/programs/ # Список выбранных направлений СТУДЕНТ
    path('programs/edit/', views.edit_programs, name='lk_account_student_edit_programs'),
    # account/edit_programs/ # Изменение набора направлений СТУДЕНТ
    path('programs/<pk>/', views.view_task, name='lk_account_student_task'),
    # account/programs/<pk>/ # Просмотр направления - редирект ниже СТУДЕНТ
    path('programs/<pk>/<task>/', views.solve_task, name='lk_account_student_task_solve'),
    # account/programs/<pk>/<task>/	# Решение заданий СТУДЕНТ

    path('students/', views.view_students, name='lk_account_curator_students'),
    # account/students/ # Просмотр студентов и переход к ТЗ КУРАТОР
    path('students/<pk>/', views.view_student_task, name='lk_account_curator_student_task'),
    # account/<pk>/ # Проверка заданий КУРАТОР

    path('admin/programs/create/', views.create_program, name='create_program'),
    # register/create_program # Создание направления АДМИН
    path('admin/programs/', views.ProgramView.as_view(), name='programs'),  # register/programs # Все направления АДМИН
    path('admin/programs/<pk>/', views.ProgramUpdateView.as_view(), name='program'),
    # register/programs/4 # Список заданий и кнопка на создание заданий АДМИН
    path('admin/programs/<pk>/create_task/', views.test_create, name='create_task'),
    # register/programs/4/create_task # Создание задания АДМИН

]
