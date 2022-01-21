from django import forms
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


class NewTaskForm(forms.Form):
    task = forms.CharField(label='New Task',
    widget=forms.TextInput(attrs={
        'class': 'input-class',
        'id': 'task-input',
        'autocomplete': 'off'
    }))


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    if 'tasks' not in request.session:
        request.session['tasks'] = []
    return render(request, 'tasks/user.html', {
        'tasks': request.session['tasks']
    })


def add(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            request.session['tasks'] += [task]
            return redirect(reverse('tasks:index'))
        else:
            return render(request, 'tasks/add.html', {
                'form': form
            })
    return render(request, 'tasks/add.html', {
        'form': NewTaskForm()
    })

