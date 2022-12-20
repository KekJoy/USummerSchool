from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import Form
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from .forms import CustomUserChangeForm, TaskSolveForm, TaskCreationForm
from authentication.models import Profile
from .models import Programs, ProgramList
from .models import TaskList
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import TaskAnswer
from .forms import ProgramCreationForm


def index(request):
    return render(request, 'users/account_student.html')


@login_required
def home(request):
    return render(request, 'users/account_student.html')


@login_required
def edit(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('lk_account_student')
    else:
        form = CustomUserChangeForm(instance=profile)
    return render(request, 'users/account_student_edit.html')


@login_required
def edit_programs(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    programs = []
    for program in Programs.objects.filter(profile=profile):
        programs.append(program.program_list.pk)

    context = {
        'blya': ProgramList.objects.all(),
        'programs': programs,
    }
    if request.method == 'POST':
        langs = request.POST.getlist("test", [])

        context = {'blya': ProgramList.objects.all(),
                   'forms': langs,
                   'programs': programs,
                   }
        if len(langs) != 0:
            for lang in langs:
                if not Programs.objects.filter(profile=profile,
                                               program_list=ProgramList.objects.get(title=lang)).exists():
                    try:
                        programs = Programs()
                        programs.profile = profile
                        programs.program_list = ProgramList.objects.get(title=lang)
                        programs.save()
                    except:
                        return render(request, 'users/account_student_program_change.html', context=context)

            # TODO: При удалении направления пользователем (снятие чекбоксов),
            #  в модели Programs удаляется направление за пользователем

            return render(request, 'users/account_student_program_change.html', context=context)
        return redirect('lk_account_student')
    else:
        return render(request, 'users/account_student_program_change.html', context=context)


class ViewPrograms(ListView):
    template_name = 'users/account_student_view_programs.html'
    model = Programs

    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        context = {'programs': Programs.objects.filter(profile=profile)}
        return render(request, 'users/account_student_view_programs.html', context=context)


@login_required
def view_programs(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    context = {'programs': Programs.objects.filter(profile=profile)}
    return render(request, 'users/account_student_view_programs.html', context=context)


@login_required
def view_task(request, pk):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if not Programs.objects.filter(profile=profile, program_list=pk).exists():
        return HttpResponse('Обнаружен недопустимый заголовок')

    context = {'programs': Programs.objects.filter(profile=profile, program_list=pk),
               'tasks': TaskList.objects.filter(program=pk),
               'pk': pk,
               'task': TaskList.objects.filter(program=pk).first().pk}

    task = str(TaskList.objects.filter(program=pk).first().number)

    # return render(request, 'users/account_student_view_task.html', context=context)
    return redirect(reverse('lk_account_student_task_solve', kwargs={'pk': pk, 'task': task}))


@login_required
def solve_task(request, pk, task):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if not Programs.objects.filter(profile=profile, program_list=pk).exists():
        return HttpResponse('Обнаружен недопустимый заголовок')

    if not TaskList.objects.filter(program=pk, number=task).exists():
        return HttpResponse('Такого задания нет')
    context = {'programs': Programs.objects.filter(profile=profile, program_list=pk),
               'tasks': TaskList.objects.filter(program=pk),
               'task': TaskList.objects.get(program=pk, number=task),
               'pk_id': pk, }

    if request.method == 'POST':
        form = TaskSolveForm(request.POST)
        if form.is_valid() and not TaskAnswer.objects.filter(
                programs=Programs.objects.get(profile=profile, program_list=pk),
                task=TaskList.objects.get(number=task)).exists():
            answer = form.cleaned_data['answer']
            task_list = form.save(commit=False)
            task_list.answer = answer
            task_list.programs = Programs.objects.get(profile=profile, program_list=pk)
            task_list.task = TaskList.objects.get(program=pk, number=task)
            task_list.save()
            messages.success(request, 'Task Successfully')

        # return render(request, 'users/test.html', context={'test': test})
        return redirect(reverse('lk_account_student_task_solve', kwargs={'pk': pk, 'task': str(int(task) + 1)}))

    return render(request, 'users/account_student_view_task.html', context=context)


@login_required
def view_students(request):
    context = {
        'task_answers': TaskAnswer.objects.all(),
        'students': Programs.objects.all(),
    }
    return render(request, 'users/account_curator_students.html', context=context)


@login_required
def view_student_task(request, pk):
    context = {
        'task_answers': TaskAnswer.objects.filter(programs=pk),
        'program_id': pk,
    }

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        grade = request.POST.get('grade')
        token = request.POST.get('token')
        if grade:
            try:
                a = TaskAnswer.objects.get(pk=token)
                a.grade = grade
                a.save()
            except:
                return HttpResponse(request, 'Нет')

        return redirect(reverse('lk_account_curator_student_task', kwargs={'pk': pk}))
    else:
        return render(request, 'users/account_curator_student_task.html', context=context)


def create_program(request):
    if request.method == 'POST':
        form = ProgramCreationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            program_list = form.save()
            program_list.title = title
            program_list.save()
            messages.success(request, 'Program Successfully')
        return render(request, 'registration_acc/create_program.html')

    return render(request, 'registration_acc/create_program.html')


class ProgramView(ListView):
    model = ProgramList
    template_name = 'registration_acc/programs.html'
    context_object_name = 'programs'


class ProgramUpdateView(UpdateView):
    model = ProgramList
    template_name = 'registration_acc/programs_update.html'
    fields = ['title', ]
    context_object_name = 'program'


class TaskCreateView(DetailView):
    model = ProgramList
    template_name = 'registration_acc/create_task.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context['program'] = ProgramList.objects.all()
        # context['tvchannel'] = TVChannel.objects.order_by('id')
        return context


def test_create(request, pk):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            task_list = form.save(commit=False)
            task_list.title = title
            task_list.description = description
            task_list.program_id = pk

            if not TaskList.objects.filter(program=pk).exists():
                task_list.number = '1'
            else:
                a = TaskList.objects.filter(program=pk).order_by('-number')[0]
                task_list.number = str(int(a.number) + 1)

            task_list.save()
            messages.success(request, 'Task Successfully')
        return render(request, 'registration_acc/blya.html')

    return render(request, 'registration_acc/blya.html')
