from django.contrib import admin
from .models import Project, Skill, Contact, BlogPost, Comment, Category, Tag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency')
    list_editable = ('proficiency',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'views_count', 'is_published')
    list_editable = ('is_published', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'excerpt')
    list_filter = ('is_published', 'created_at', 'author', 'category', 'tags')
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'is_approved')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content')