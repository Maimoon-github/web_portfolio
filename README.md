# Personal Portfolio Website with Blog

A Django-powered portfolio website with integrated blogging functionality.

## Features

- Portfolio showcase with projects, skills, and about sections
- Blog system with simple content management
- Contact form
- Responsive design with Bootstrap 5

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
6. Access the admin panel at `/admin` to add content

## Project Structure

- `core` app: Main application with portfolio and blog functionality
- Templates: All frontend templates
- Static files: CSS and JavaScript resources

## Technology Stack

- Django 5.2
- Bootstrap 5.1.3
- SQLite Database (development)
- Font Awesome 5.15.4