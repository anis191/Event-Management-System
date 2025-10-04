# Event-Zone: Event Management System

![Django](https://img.shields.io/badge/Django-5.1.5-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue.svg)

> A full-stack Event Management web application built with Django (MVT).
> Clean, modular, and production-ready — featuring event CRUD, role-based dashboards, RSVP, email activation, and more.

🔗 **Live Demo:** [event-management-system-v44p.onrender.com](https://event-management-system-v44p.onrender.com)  
📁 **Source Code:** [GitHub Repository](https://github.com/anis191/Event-Management-System)

---

## About

**Event-Zone** is a Django-based Event Management System that follows the Model-View-Template (MVT) pattern. It was designed to be beginner-friendly, extendable, and ready for production deployment. The project includes user authentication, role-based access (organizer/participant), event creation and management, RSVP flow, email activation, and admin dashboards.

---

## Features

* User authentication (register / login / logout)
* Email-based account activation
* Role-based dashboards (organizer vs participant)
* Create / read / update / delete events and categories
* RSVP to events (participant flow)
* Event lists, detail pages, and search/filtering
* Admin panel for site management
* Static file handling using WhiteNoise
* Support for PostgreSQL (production) and SQLite (development)
* Faker for generating sample data during development

---

## Technology Stack

### Backend
- **Framework:** Django 5.1.5
- **Database:** PostgreSQL
- **Authentication:** Django Auth System
- **File Storage:** Whitenoise for static files

### Frontend
- **Templating:** Django Templates
- **Styling:** CSS3 with responsive design
- **JavaScript:** Vanilla JS for interactivity

### Development & Deployment
- **Environment Management:** python-decouple
- **Database ORM:** Django ORM
- **Static Files:** Whitenoise
- **Deployment:** Render.com

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anis191/Event-Management-System.git
   cd Event-Management-System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgres://username:password@localhost:5432/event_zone
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load Sample Data (Optional)**
   ```bash
   python manage.py loaddata sample_data.json
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to view the application.

## 📁 Project Structure

```
Event-Management-System/
├── event_zone/                 # Main project directory
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── events/                    # Events app
│   ├── models.py             # Event models
│   ├── views.py              # Event views
│   ├── urls.py               # Event URLs
│   └── templates/            # Event templates
├── users/                     # Users app
│   ├── models.py             # User models
│   ├── views.py              # User views
│   └── templates/            # User templates
├── static/                    # Static files
│   ├── css/                  # CSS files
│   ├── js/                   # JavaScript files
│   └── images/               # Image assets
├── media/                     # User uploaded files
├── requirements.txt           # Project dependencies
└── manage.py                 # Django management script
```
---

## Database & static files

* **Migrations**

  * Run `python manage.py makemigrations` and `python manage.py migrate` as needed.
* **Static files**

  * For production, run:

    ```bash
    python manage.py collectstatic --noinput
    ```
  * The project uses **WhiteNoise** to serve static files in production (no separate web server required for static content).

---

## Deploying (quick notes)

Below are general steps — adapt to your chosen host (e.g. Render, Heroku, Railway, etc).

1. Push repository to GitHub.
2. Create a new web service on your host and connect GitHub repo.
3. Set environment variables on the host (SECRET_KEY, DEBUG=false, DATABASE_URL, ALLOWED_HOSTS, EMAIL_*).
4. Ensure build and start commands include collecting static files and running migrations:

   * Example Build Command:

     ```bash
     pip install -r requirements.txt
     python manage.py migrate
     python manage.py collectstatic --noinput
     ```
   * Example Start Command (Gunicorn):

     ```
     gunicorn <your_django_project>.wsgi:application --bind 0.0.0.0:$PORT
     ```

     Replace `<your_django_project>` with the actual project package name (the one with `settings.py` inside).

**Render-specific tips**

* Create a PostgreSQL instance and set `DATABASE_URL`.
* Add `python manage.py collectstatic --noinput` as part of build or start process.
* Ensure `ALLOWED_HOSTS` includes your Render domain.

---

## Common issues & troubleshooting

**1. `TemplateSyntaxError: <ExtendsNode: extends "..." > must be the first tag in the template.`**

* Cause: You have `{% load static %}` or another tag **before** `{% extends "base.html" %}`.
* Fix: Ensure `{% extends %}` is the first tag (first non-whitespace code) in the child template. Move `{% load static %}` into the base template (or place it after `{% extends %}` in the child).

**2. Static files not loading in production**

* Ensure `collectstatic` was run and `whitenoise` is configured in `MIDDLEWARE`.
* Confirm `STATIC_ROOT` is set in settings and that your host serves collected static files.

**3. Database connection errors on deploy**

* Verify `DATABASE_URL` syntax and credentials.
* Ensure the host firewall / DB service allows remote connections if applicable.

**4. Email not sending**

* Double-check SMTP credentials and ports.
* Check host provider restrictions (some hosts block SMTP ports by default).

If you run into other errors, check Django logs and traceback in the server console — they reveal the specific file/line to fix.

---

## Contributing

Contributions are welcome! If you'd like to help:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make your changes and add tests where applicable.
4. Open a pull request describing your change.

Please follow consistent code style and include a descriptive commit message.

---

## License

**License:** [MIT License](LICENSE) – This project is open source and available under the MIT license.

---

## Contact

Created by **Anisul Alam** — see the repo: [https://github.com/anis191/Event-Management-System](https://github.com/anis191/Event-Management-System)
