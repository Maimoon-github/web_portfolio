from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Skill
from .forms import ContactForm

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/projects.html', {'projects': projects})

def skills(request):
    skills = Skill.objects.all()
    return render(request, 'core/skills.html', {'skills': skills})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})