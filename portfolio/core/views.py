from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project, Skill, BlogPost, Comment, Category, Tag
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
    # Get all published posts
    all_posts = BlogPost.objects.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(all_posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        posts = paginator.page(paginator.num_pages)
    
    # Get categories and popular tags
    categories = Category.objects.all()
    
    # Get popular tags (tags with most posts)
    popular_tags = Tag.objects.annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count')[:15]
    
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'popular_tags': popular_tags
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.increment_views()
    
    # Get related posts
    related_posts = post.get_related_posts()
    
    # Get popular posts
    popular_posts = BlogPost.objects.filter(is_published=True).order_by('-views_count')[:3]
    
    return render(request, 'core/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
        'popular_posts': popular_posts
    })
    
def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    all_posts = BlogPost.objects.filter(category=category, is_published=True)
    
    # Pagination
    paginator = Paginator(all_posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count')[:15]
    
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'categories': Category.objects.all(),
        'popular_tags': popular_tags,
        'current_category': category
    })
    
def tag_posts(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    all_posts = tag.posts.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(all_posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count')[:15]
    
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'categories': Category.objects.all(),
        'popular_tags': popular_tags,
        'current_tag': tag
    })
    
def search_posts(request):
    query = request.GET.get('q', '')
    all_posts = BlogPost.objects.filter(is_published=True)
    
    if query:
        all_posts = all_posts.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(excerpt__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(all_posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get popular tags
    popular_tags = Tag.objects.annotate(
        posts_count=models.Count('posts')
    ).order_by('-posts_count')[:15]
    
    return render(request, 'core/blog_list.html', {
        'posts': posts,
        'categories': Category.objects.all(),
        'popular_tags': popular_tags,
        'search_query': query
    })


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
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Apply filters if provided
    if category_filter:
        user_posts = user_posts.filter(category__slug=category_filter)
    
    if status_filter:
        is_published = status_filter == 'published'
        user_posts = user_posts.filter(is_published=is_published)
    
    # Get categories for the filter dropdown
    user_categories = Category.objects.filter(posts__author=request.user).distinct()
    
    # Get some statistics
    total_posts = user_posts.count()
    published_posts = user_posts.filter(is_published=True).count()
    draft_posts = total_posts - published_posts
    
    return render(request, 'core/blog_management/user_posts.html', {
        'posts': user_posts,
        'categories': user_categories,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'category_filter': category_filter,
        'status_filter': status_filter
    })

@login_required
def create_blog_post(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # For ManyToMany fields, save the form again
            form.save_m2m()  # This saves the tags
            messages.success(request, 'Blog post created successfully!')
            return redirect('core:user_blog_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'core/blog_management/post_form.html', {
        'form': form,
        'title': 'Create New Blog Post',
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()
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
            form.save()  # This will save the post and the ManyToMany relationships
            messages.success(request, 'Blog post updated successfully!')
            return redirect('core:user_blog_posts')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'core/blog_management/post_form.html', {
        'form': form,
        'post': post,
        'title': 'Edit Blog Post',
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()
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