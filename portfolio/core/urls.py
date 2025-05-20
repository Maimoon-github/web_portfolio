from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('blog/category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('blog/tag/<slug:tag_slug>/', views.tag_posts, name='tag_posts'),
    path('blog/search/', views.search_posts, name='search_posts'),
    
    # Authentication
    
    # Blog management
    path('dashboard/posts/', views.user_blog_posts, name='user_blog_posts'),
    path('dashboard/posts/new/', views.create_blog_post, name='create_blog_post'),
    path('dashboard/posts/<slug:slug>/edit/', views.update_blog_post, name='update_blog_post'),
    path('dashboard/posts/<slug:slug>/delete/', views.delete_blog_post, name='delete_blog_post'),
]