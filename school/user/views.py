from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView

from django.views.generic.list import ListView

from .forms import ProgramCreationForm, TaskCreationForm
from .models import ProgramList, Programs


def create_program(request):
    if request.method == 'POST':
        form = ProgramCreationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            program_list = form.save()
            program_list.title = title
            program_list.save()
            messages.success(request, 'Program Successfully')
        return render(request, 'user/create_program.html')

    return render(request, 'user/create_program.html')


class ProgramView(ListView):
    model = ProgramList
    template_name = 'user/programs.html'
    context_object_name = 'programs'


class ProgramUpdateView(UpdateView):
    model = ProgramList
    template_name = 'user/programs_update.html'
    fields = ['title', ]
    context_object_name = 'program'


class TaskCreateView(DetailView):
    model = ProgramList
    template_name = 'user/create_task.html'
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
            task_list.save()
            messages.success(request, 'Task Successfully')
        return render(request, 'user/blya.html')

    return render(request, 'user/blya.html')


def get_answer(request, test_pk, pk):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            answer = form.cleaned_data['answer']
            answer_list = form.save()
            answer_list.title = title
            answer_list.answer = answer
            answer_list.answer_id = pk
            answer_list.save()
            form.save()
            messages.success(request, 'Ответ отправлен')
        return render(request, 'user/task.html')

    return render(request, 'user/task.html')
