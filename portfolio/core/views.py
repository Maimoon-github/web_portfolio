from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from .models import Project, Skill, BlogPost, Comment
from .forms import ContactForm, BlogPostForm, SignUpForm, CommentForm

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


def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted and will be visible after approval.')
        else:
            messages.error(request, 'There was an error submitting your comment. Please try again.')
    
    return redirect('core:blog_detail', slug=slug)

@login_required
def user_blog_posts(request):
    """Display all blog posts by the logged-in user"""
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'core/blog_management/user_posts.html', {'posts': user_posts})

@login_required
def create_blog_post(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('core:user_blog_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'core/blog_management/post_form.html', {
        'form': form,
        'title': 'Create New Blog Post'
    })

@login_required
def update_blog_post(request, slug):
    """Update an existing blog post"""
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if the logged in user is the author
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('core:user_blog_posts')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'core/blog_management/post_form.html', {
        'form': form,
        'post': post,
        'title': 'Edit Blog Post'
    })

@login_required
def delete_blog_post(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if the logged in user is the author
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('core:user_blog_posts')
        
    return render(request, 'core/blog_management/post_confirm_delete.html', {'post': post})

def custom_404_view(request, exception):
    """Custom handler for 404 errors (Page Not Found)."""
    return render(request, '404.html', status=404)

def custom_500_view(request):
    """Custom handler for 500 errors (Server Error)."""
    return render(request, '500.html', status=500)


def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})