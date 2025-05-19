#!/usr/bin/env python
"""
Script to test the blog management system by:
1. Creating a new user
2. Creating categories and tags
3. Creating a blog post with category and tags
4. Testing blog post view count
5. Editing the blog post
6. Testing related posts functionality
7. Deleting the blog post
"""

import os
import sys
import django
import random
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
sys.path.append(os.path.join(os.path.dirname(__file__), 'portfolio'))
django.setup()

# Now we can import Django models
from core.models import BlogPost, Category, Tag

# Create a test user
User = get_user_model()
username = 'testuser'
password = 'testpassword123'
email = 'test@example.com'

print(f"\n====== Testing Blog Management System ======\n")

# Try creating a user
try:
    user = User.objects.create_user(username=username, email=email, password=password)
    print(f"✅ Created test user: {username}")
except IntegrityError:
    user = User.objects.get(username=username)
    print(f"ℹ️ Using existing test user: {username}")

# Create test categories
print("\n----- Creating categories -----")
categories = [
    {'name': 'Technology', 'slug': 'technology', 'description': 'Tech related posts'},
    {'name': 'Travel', 'slug': 'travel', 'description': 'Travel adventures'},
    {'name': 'Coding', 'slug': 'coding', 'description': 'Programming tutorials'}
]

created_categories = []
for cat_data in categories:
    try:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name'], 'description': cat_data['description']}
        )
        created_categories.append(category)
        status = "Created" if created else "Already exists"
        print(f"✅ Category: {category.name} - {status}")
    except Exception as e:
        print(f"❌ Error creating category {cat_data['name']}: {e}")

# Create test tags
print("\n----- Creating tags -----")
tags = [
    {'name': 'Django', 'slug': 'django'},
    {'name': 'Python', 'slug': 'python'},
    {'name': 'Web Development', 'slug': 'web-development'},
    {'name': 'Frontend', 'slug': 'frontend'},
    {'name': 'Backend', 'slug': 'backend'},
]

created_tags = []
for tag_data in tags:
    try:
        tag, created = Tag.objects.get_or_create(
            slug=tag_data['slug'],
            defaults={'name': tag_data['name']}
        )
        created_tags.append(tag)
        status = "Created" if created else "Already exists"
        print(f"✅ Tag: {tag.name} - {status}")
    except Exception as e:
        print(f"❌ Error creating tag {tag_data['name']}: {e}")

# Create a test blog post
print("\n----- Creating a blog post with category and tags -----")
post = BlogPost(
    author=user,
    title="Test Blog Post with Categories and Tags",
    slug="test-blog-post-with-categories-and-tags",
    content="This is a test blog post content with detailed information.",
    excerpt="This is a test excerpt for testing categories and tags.",
    is_published=True,
    category=created_categories[0] if created_categories else None
)
try:
    post.save()
    if created_tags:
        # Add some tags to the post
        post.tags.add(*created_tags[:3])  # Add first 3 tags
    print(f"✅ Created blog post: {post.title}")
    print(f"   Slug: {post.slug}")
    print(f"   Author: {post.author.username}")
    print(f"   Category: {post.category.name if post.category else 'None'}")
    print(f"   Tags: {', '.join(tag.name for tag in post.tags.all())}")
    print(f"   Published: {'Yes' if post.is_published else 'No'}")
except Exception as e:
    print(f"❌ Error creating blog post: {e}")

# Test view count functionality
print("\n----- Testing view count functionality -----")
try:
    initial_views = post.views_count
    print(f"Initial views: {initial_views}")
    
    # Simulate multiple views
    for i in range(5):
        post.increment_views()
        
    post.refresh_from_db()
    final_views = post.views_count
    print(f"Final views: {final_views}")
    print(f"Views increased by: {final_views - initial_views}")
except Exception as e:
    print(f"❌ Error testing view count: {e}")

# Create another related post in the same category
print("\n----- Creating related posts -----")
try:
    related_post = BlogPost(
        author=user,
        title="Related Test Blog Post",
        slug="related-test-blog-post",
        content="This post is related to the first one by category.",
        excerpt="This is a test excerpt for a related post.",
        is_published=True,
        category=post.category
    )
    related_post.save()
    if created_tags:
        # Add some overlapping tags
        related_post.tags.add(*created_tags[1:4])  # Add some overlapping tags
    print(f"✅ Created related post: {related_post.title} in category {related_post.category.name if related_post.category else 'None'}")
except Exception as e:
    print(f"❌ Error creating related post: {e}")

# Test related posts functionality
print("\n----- Testing related posts functionality -----")
try:
    related_posts = post.get_related_posts()
    print(f"Found {related_posts.count()} related posts:")
    for idx, rp in enumerate(related_posts, 1):
        print(f"  {idx}. {rp.title}")
except Exception as e:
    print(f"❌ Error testing related posts: {e}")

# Edit the blog post
print("\n----- Editing blog post -----")
try:
    post.title = "Updated Test Blog Post"
    post.content = "This content has been updated with more information."
    # Change the category
    if len(created_categories) > 1:
        post.category = created_categories[1]
    post.save()
    print(f"✅ Updated blog post: {post.title}")
    print(f"   New category: {post.category.name if post.category else 'None'}")
except Exception as e:
    print(f"❌ Error updating blog post: {e}")

# List all posts for the user
print("\n----- Listing user's blog posts by category -----")
user_posts = BlogPost.objects.filter(author=user)
print(f"Total posts: {user_posts.count()}")
for category in created_categories:
    category_posts = user_posts.filter(category=category)
    if category_posts.count() > 0:
        print(f"\nCategory: {category.name} ({category_posts.count()} posts)")
        for idx, p in enumerate(category_posts, 1):
            tags_str = ", ".join([tag.name for tag in p.tags.all()])
            print(f"  {idx}. {p.title} - Tags: [{tags_str}]")

# Cleanup - Delete the posts
print("\n----- Cleaning up -----")
try:
    deleted_count, _ = user_posts.delete()
    print(f"✅ Deleted {deleted_count} blog post(s)")
except Exception as e:
    print(f"❌ Error deleting blog posts: {e}")

print("\n====== Blog Management System Test Complete ======\n")
