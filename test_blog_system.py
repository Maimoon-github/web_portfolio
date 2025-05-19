#!/usr/bin/env python
"""
Script to test the blog management system by:
1. Creating a new user
2. Creating a blog post
3. Editing the blog post
4. Deleting the blog post
"""

import os
import sys
import django
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
sys.path.append(os.path.join(os.path.dirname(__file__), 'portfolio'))
django.setup()

# Now we can import Django models
from core.models import BlogPost

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

# Create a test blog post
print("\n----- Creating a blog post -----")
post = BlogPost(
    author=user,
    title="Test Blog Post",
    slug="test-blog-post",
    content="This is a test blog post content.",
    excerpt="This is a test excerpt.",
    is_published=True
)
try:
    post.save()
    print(f"✅ Created blog post: {post.title}")
    print(f"   Slug: {post.slug}")
    print(f"   Author: {post.author.username}")
    print(f"   Published: {'Yes' if post.is_published else 'No'}")
except Exception as e:
    print(f"❌ Error creating blog post: {e}")

# List all posts for the user
print("\n----- Listing user's blog posts -----")
user_posts = BlogPost.objects.filter(author=user)
print(f"Total posts: {user_posts.count()}")
for idx, p in enumerate(user_posts, 1):
    print(f"{idx}. {p.title} - {'Published' if p.is_published else 'Draft'}")

# Edit the blog post
print("\n----- Editing blog post -----")
try:
    post = user_posts.first()
    post.title = "Updated Test Blog Post"
    post.slug = "updated-test-blog-post"
    post.content = "This content has been updated."
    post.save()
    print(f"✅ Updated blog post: {post.title}")
except Exception as e:
    print(f"❌ Error updating blog post: {e}")

# Delete the blog post
print("\n----- Deleting blog post -----")
try:
    deleted_count, _ = user_posts.delete()
    print(f"✅ Deleted {deleted_count} blog post(s)")
except Exception as e:
    print(f"❌ Error deleting blog post: {e}")

print("\n====== Blog Management System Test Complete ======\n")
