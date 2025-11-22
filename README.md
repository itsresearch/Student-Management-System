**Student Management System**

A simple Django-based Student Management System for managing students, teachers, schedules, homework, and school administration tasks. This repository contains a Django project with several apps, optional Docker support, and a management command to seed demo data.

**Project Status**: Development

**Key Features**
- **Student Management**: Add, edit, and view student records (`student` app).
- **Authentication**: Registration and login views (`home_auth` app).
- **School Management**: Teacher profiles, schedules, homework, and related models (`school` app).
- **Demo Data**: A management command `seed_demo_data` to populate example data.

**Quick Links**
- **Code**: `manage.py`, `Home/`, `home_auth/`, `school/`, `student/`
- **Templates**: `templates/`
- **Static assets**: `static/` and `media/` for uploads

**Prerequisites**
- Python 3.8+ (or the version used in `requirements.txt`)
- Git
- Optional: Docker & Docker Compose (for containerized setup)

**Installation (Local - PowerShell)**
1. Clone the repo:
   `git clone https://github.com/itsresearch/Student-Management-System.git`
2. Create and activate a virtual environment:
   `python -m venv venv`
   `.\venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Apply migrations:
   `python manage.py migrate`
5. (Optional) Create a superuser:
   `python manage.py createsuperuser`
6. (Optional) Seed demo data:
   `python manage.py seed_demo_data`
7. Run the dev server:
   `python manage.py runserver`

**Installation (Docker)**
1. Build and run with Docker Compose:
   `docker-compose up --build`
2. When containers are running, apply migrations inside the web container or adapt your compose commands. Example (host):
   `docker-compose exec web python manage.py migrate`
3. Create superuser and seed as needed:
   `docker-compose exec web python manage.py createsuperuser`
   `docker-compose exec web python manage.py seed_demo_data`

**Running Tests**
`python manage.py test`

**Project Structure (high level)**
- `Home/` - Django project settings, ASGI/WGSI, and URL config.
- `home_auth/` - Authentication views and URLs.
- `school/` - School-related models, views, admin, and management commands.
- `student/` - Student models and views.
- `templates/` - HTML templates used by the project.
- `static/` and `media/` - Static assets and uploaded media.

**Useful Commands Summary**
- `pip install -r requirements.txt` : Install Python deps
- `python manage.py migrate` : Run DB migrations
- `python manage.py createsuperuser` : Create admin user
- `python manage.py seed_demo_data` : Populate demo data
- `python manage.py runserver` : Start local development server

**Notes & Configuration**
- If your setup expects environment variables (e.g., `SECRET_KEY`, `DATABASE_URL`, `DEBUG`), set them in your environment or add a `.env` loader to `settings.py`.
- Static files: in production, run `python manage.py collectstatic` and serve via a web server or CDN.

**Contributing**
- Feel free to open issues and pull requests. Keep changes small and focused.
- Run tests for the parts you modify and include migration files where necessary.

**License**
Specify your license here (e.g., MIT). If unsure, add a `LICENSE` file.

**Contact**
For questions, contact the repository owner or maintainers.
