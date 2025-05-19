from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, Skill, BlogPost
from .forms import ContactForm

def home(request):
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    return render(request, 'core/home.html', {'recent_posts': recent_posts})

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

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'core/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'core/blog_detail.html', {'post': post})