from django.shortcuts import render
from .models import Task, Assignment, Team

def browse(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment/browse.html', {'assignments': assignments})

def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'assignment/tasks.html', {'tasks': tasks})