from django import forms
from .models import Contact, BlogPost, Comment
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'tags', 'content', 'featured_image', 'excerpt', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary (optional)'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_title(self):
        """Generate a unique slug from the title"""
        title = self.cleaned_data['title']
        if self.instance.pk:
            # If this is an edit of an existing post
            if BlogPost.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
                raise ValidationError('A post with this title already exists.')
        else:
            # If this is a new post
            if BlogPost.objects.filter(title=title).exists():
                raise ValidationError('A post with this title already exists.')
        return title
    
    def save(self, commit=True, author=None):
        instance = super().save(commit=False)
        # Generate slug from title
        instance.slug = slugify(instance.title)
        
        # Set author if provided and this is a new post
        if author and not instance.pk:
            instance.author = author
            
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Comment'}),
        }