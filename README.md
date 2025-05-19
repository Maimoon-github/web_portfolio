# Personal Portfolio Website with Blog Management System

A Django-powered portfolio website with integrated blogging functionality and a full user blog management system.

## Features

### Portfolio Features
- Home page with banner image and introduction
- Projects showcase with images and descriptions
- Skills listing with proficiency indicators
- About page
- Contact form
- Responsive design with Bootstrap 5

### Blog System Features
- Blog listing page showing published posts
- Individual blog post pages with author attribution
- Comment system with moderation
- User dashboard for blog management
- Create, read, update, delete (CRUD) functionality
- Featured image uploads
- Publish/draft functionality

## Authentication System
- User registration with sign-up form
- Login/logout functionality
- Password reset via email
- User-specific content management

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
6. Access the admin panel at `/admin` to add/manage content
7. Visit the site at `/` to view the portfolio and blog
8. Register a user account to create and manage blog posts

## Project Structure

- `core/`: Main app containing all models, views, and templates
  - `models.py`: Data models for Portfolio, Blog, and Comments
  - `views.py`: View functions for all functionality
  - `urls.py`: URL routing
  - `forms.py`: Form handling for blog posts, comments, and user accounts
  - `templates/`: Templates organized by feature
- `portfolio/`: Project settings and configuration
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded content
- `templates/`: Global templates (including authentication templates)

## Technology Stack

- Django 5.2
- Bootstrap 5.1.3
- SQLite Database (development)
- Font Awesome 5.15.4
- JavaScript
- Custom CSS

## License

This project is licensed under the MIT License.