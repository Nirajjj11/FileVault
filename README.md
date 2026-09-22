# FileVault

FileVault is a Django-based web application for managing personal files through an organized, authenticated workspace. Users can register, sign in, create nested folders, upload files, view stored content, rename resources, download files, and delete resources they own.

> **Project status:** FileVault is currently configured for local development with SQLite. The documentation also includes an optional PostgreSQL configuration path for deployments that need a production database.

## Contents

- [Project Overview](#project-overview)
- [Objectives and Motivation](#objectives-and-motivation)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Application and Request Flow](#application-and-request-flow)
- [Data Model and ER Diagram](#data-model-and-er-diagram)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Environment Configuration](#environment-configuration)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [Using FileVault](#using-filevault)
- [URL and Feature Reference](#url-and-feature-reference)
- [Testing and Maintenance](#testing-and-maintenance)
- [Production Checklist](#production-checklist)
- [Limitations and Future Enhancements](#limitations-and-future-enhancements)
- [License](#license)

## Project Overview

FileVault provides a single web interface for storing and organizing user-owned digital content. It uses Django's built-in authentication system and ownership-aware querysets to keep a user's folders and files isolated from other users.

The project demonstrates a practical Django Model-View-Template (MVT) application with:

- Authentication and authorization
- Class-based views
- Model forms and validation
- Relational database design
- Nested folder management
- Multipart file uploads
- Media-file serving during development
- Dashboard statistics based on stored file metadata
- Responsive templates using Bootstrap 5 and custom CSS

## Objectives and Motivation

### Objective

The objective is to build a simple, understandable, and extensible file-management platform where a user can manage personal files from a browser without relying on an unstructured upload directory.

### Motivation

FileVault was created to address common file-management needs in a focused application:

- Keep documents, images, videos, audio, and other uploads in meaningful folders.
- Make file operations accessible from a browser.
- Learn how Django authentication, forms, models, views, templates, and media storage work together.
- Demonstrate ownership-based access control for user-generated resources.
- Provide a foundation that can later be extended with sharing, search, quotas, previews, and cloud storage.

## Features

### Implemented

- User registration with username, email, and password confirmation
- Login and logout using Django authentication
- Authenticated dashboard
- Root-folder and nested-folder creation
- Folder detail pages
- Folder rename and deletion
- File upload into a selected folder
- File rename and deletion
- File metadata capture: original name, MIME type, byte size, and upload timestamp
- Inline media previews where supported by the browser
- File download through the stored media URL
- Dashboard totals for folders, files, storage used, and common file categories
- Owner-scoped folder and file queries
- Bootstrap-based responsive interface

### Current scope note

The landing page describes file sharing as a product direction, but the current codebase does not yet contain share-link models, sharing URLs, or sharing views. Sharing should therefore be treated as a planned enhancement rather than an available feature.

## Technology Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.12+ recommended |
| Web framework | Django 6.1.1 |
| Database (current default) | SQLite 3 via Django ORM |
| Optional production database | PostgreSQL with `psycopg` |
| Frontend | Django Templates, HTML, Bootstrap 5.3.8, CSS, JavaScript |
| Authentication | `django.contrib.auth` |
| Static files | Django staticfiles and `static/` |
| Uploaded files | Django `FileField` and `media/uploads/` |
| Dependency file | `requirements.txt` |

The current dependency file pins these packages:

- Django 6.1.1
- `sqlparse` 0.6.0
- `tzdata` 2026.4

## Architecture

FileVault follows Django's MVT architecture:

```mermaid
flowchart LR
    Browser[Browser] --> URLs[URL dispatcher]
    URLs --> Accounts[accounts app]
    URLs --> Storage[storage app]
    Accounts --> Auth[Django authentication]
    Storage --> Views[Class-based views]
    Views --> Forms[Model forms]
    Views --> Models[Django ORM models]
    Models --> DB[(SQLite or PostgreSQL)]
    Views --> Templates[Django templates]
    Templates --> Browser
    Views --> Media[media/uploads]
    Browser --> Static[static CSS and JavaScript]
```

### Application responsibilities

- **`filevault/`**: project configuration, settings, root URL routing, WSGI, and ASGI entry points.
- **`accounts/`**: registration, login, logout, and account forms.
- **`storage/`**: folders, files, upload handling, ownership checks, dashboard statistics, and storage templates.
- **`templates/`**: shared site templates and public pages.
- **`static/`**: project CSS and JavaScript.
- **`media/`**: user-uploaded files during development.

## Application and Request Flow

A typical authenticated upload request follows this path:

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant D as Django URL dispatcher
    participant V as FileUploadView
    participant F as FileUploadForm
    participant M as File model
    participant DB as Database
    participant FS as media/uploads
    participant T as Folder template

    U->>B: Select a file in a folder
    B->>D: POST /storage/folder/{folder_id}/upload/
    D->>V: Resolve FileUploadView
    V->>DB: Confirm folder belongs to logged-in user
    V->>F: Validate multipart form
    F->>M: Set original name, MIME type, and size
    V->>DB: Save File row
    V->>FS: Save uploaded binary
    V->>T: Redirect to folder detail
    T-->>B: Render updated folder contents
```

For normal page requests, the shorter flow is:

```mermaid
flowchart LR
    A[Browser request] --> B[Root URL configuration]
    B --> C[App URL configuration]
    C --> D[LoginRequiredMixin or view]
    D --> E[Queryset and form logic]
    E --> F[(Database)]
    E --> G[Template context]
    G --> H[HTML response]
```

## Data Model and ER Diagram

Django's built-in `User` model owns both folders and files. A folder may optionally point to another folder through the self-referencing `parent` relationship, which creates a tree of nested folders. Every file belongs to exactly one folder and one user.

```mermaid
erDiagram
    USER ||--o{ FOLDER : owns
    USER ||--o{ FILE : owns
    FOLDER ||--o{ FOLDER : contains
    FOLDER ||--o{ FILE : contains

    USER {
        integer id PK
        string username
        string email
        string password_hash
    }

    FOLDER {
        integer id PK
        integer owner_id FK
        integer parent_id FK
        string name
        datetime created_at
        datetime updated_at
    }

    FILE {
        integer id PK
        integer owner_id FK
        integer folder_id FK
        string file
        string original_name
        string file_type
        bigint size
        datetime uploaded_at
    }
```

### Relationship rules

- Deleting a user cascades to that user's folders and files.
- Deleting a folder cascades to its child folders and contained files.
- A root folder has `parent = NULL`.
- A file cannot exist without a parent folder.
- Folder and file views filter by `request.user`, preventing normal users from accessing another user's resources through these views.
- The physical upload is stored below `MEDIA_ROOT/uploads/`; the database stores the associated `FileField` path and metadata.

## Project Structure

```text
FileVault/
├── manage.py                         # Django management entry point
├── requirements.txt                  # Python dependencies
├── db.sqlite3                        # Local development database
├── README.md
├── Project.docx                      # Project reference document
├── accounts/                         # Authentication application
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                      # Registration and login forms
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py                      # Register, login, logout
│   ├── migrations/
│   └── templates/accounts/
│       ├── login.html
│       └── register.html
├── storage/                          # File and folder application
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                      # Folder, upload, rename forms
│   ├── models.py                     # Folder and File models
│   ├── tests.py
│   ├── urls.py
│   ├── views.py                      # Dashboard and CRUD views
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/storage/
│       ├── dashboard.html
│       ├── file_confirm_delete.html
│       ├── file_rename.html
│       ├── file_upload.html
│       ├── folder_confirm_delete.html
│       ├── folder_details.html
│       └── folder_form.html
├── filevault/                        # Django project package
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/                        # Shared and public templates
│   ├── about.html
│   ├── base.html
│   └── home.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── media/uploads/                    # User uploads in development
└── screenshorts/                     # Application screenshots
    ├── 1.png
    ├── 2.png
    ├── 3.png
    ├── 4.png
    ├── 5.png
    └── 6.png
```

## Screenshots

### Landing page

![FileVault landing page](screenshorts/1.png)

### Dashboard

![FileVault dashboard](screenshorts/2.png)

### About page

![FileVault about page](screenshorts/3.png)

### About page features and authentication section

![FileVault features](screenshorts/4.png)

### Technology and module overview

![FileVault technology overview](screenshorts/5.png)

### Folder detail and file management

![FileVault folder detail](screenshorts/6.png)

## Prerequisites

Install the following before starting:

- Python 3.12 or newer
- Git
- A terminal such as PowerShell, Command Prompt, or Bash
- Optional for PostgreSQL: PostgreSQL 14+ and a database user with permission to create or use a database

Verify Python and Git:

```powershell
python --version
git --version
```

On some systems, use `py --version` instead of `python --version`.

## Local Setup

The commands below are written for Windows PowerShell.

### 1. Clone the repository

```powershell
git clone https://github.com/Nirajjj11/FileVault.git
cd FileVault
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation for the current user, run PowerShell as the current user and use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again. On macOS or Linux, use:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Upgrade pip and install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

For local development, the checked-in settings use SQLite and a development secret key. Before deployment, create a `.env` file or configure environment variables as described in [Environment Configuration](#environment-configuration).

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

### 8. Check the project

```powershell
python manage.py check
```

## Environment Configuration

The current `filevault/settings.py` contains development values. Production deployments should move secrets and environment-specific values out of source control.

Recommended variables:

| Variable | Purpose | Example |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret used for signing Django data | `replace-with-a-long-random-value` |
| `DJANGO_DEBUG` | Enables development diagnostics | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated permitted hostnames | `example.com,www.example.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Trusted HTTPS origins when needed | `https://example.com` |
| `DATABASE_URL` | Optional PostgreSQL connection URL | `postgresql://filevault:password@localhost:5432/filevault` |
| `DJANGO_SETTINGS_MODULE` | Settings module | `filevault.settings` |

Example PowerShell session:

```powershell
$env:DJANGO_SECRET_KEY = "replace-with-a-long-random-value"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:DJANGO_SETTINGS_MODULE = "filevault.settings"
```

Do not commit real passwords, API keys, production secret keys, or private database URLs. Add `.env` to `.gitignore` when using a dotenv loader.

## Database Configuration

### SQLite: current default

The repository currently uses SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite is convenient for development, demos, and small installations. The database file is created in the project root after migrations run.

### PostgreSQL: optional production path

PostgreSQL is not currently enabled by the checked-in settings. To use it:

1. Install PostgreSQL and create a database and user.
2. Install a PostgreSQL Django driver in the virtual environment:

```powershell
python -m pip install "psycopg[binary]"
```

3. Add the driver to the dependency file used for deployment.
4. Update `DATABASES` in `filevault/settings.py` to read a `DATABASE_URL` or individual PostgreSQL environment variables. A typical Django configuration is:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
```

5. Run migrations against PostgreSQL:

```powershell
python manage.py migrate
```

6. Back up and migrate existing data before switching a real installation. For a simple SQLite export, use Django fixtures or a purpose-built migration process rather than copying the database file into a live PostgreSQL system.

## Running the Application

Start Django's development server from the project root:

```powershell
python manage.py runserver
```

Open:

- Home page: `http://127.0.0.1:8000/`
- About page: `http://127.0.0.1:8000/about/`
- Registration: `http://127.0.0.1:8000/accounts/register/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Dashboard: `http://127.0.0.1:8000/storage/`
- Admin: `http://127.0.0.1:8000/admin/`

During development, Django serves files below `MEDIA_ROOT` because `filevault/urls.py` adds the media URL pattern when `DEBUG` is enabled. This is not a production media-serving strategy.

## Using FileVault

1. Open the home page.
2. Select **Register** and create an account.
3. Log in with the new account.
4. From the dashboard, create a root folder.
5. Open a folder and optionally create a nested folder.
6. Upload a file into the current folder.
7. View the file preview or use the download control when available.
8. Rename or delete files and folders as required.
9. Use the dashboard statistics to review file totals, storage usage, and detected file categories.
10. Log out when finished.

The upload form records the browser-provided content type and file size. The application should still validate file types, size limits, and security rules more strictly before production use.

## URL and Feature Reference

### Public and account routes

| Method | URL | Name | Purpose |
| --- | --- | --- | --- |
| GET | `/` | `home` | Public landing page |
| GET | `/about/` | `about` | About page |
| GET/POST | `/accounts/register/` | `accounts:register` | Create an account |
| GET/POST | `/accounts/login/` | `accounts:login` | Authenticate a user |
| POST | `/accounts/logout/` | `accounts:logout` | End the current session |

### Storage routes

| Method | URL | Name | Purpose |
| --- | --- | --- | --- |
| GET | `/storage/` | `storage:dashboard` | Show the user's root folders and statistics |
| GET | `/storage/folder/<pk>/` | `storage:folder-detail` | Show subfolders and files |
| GET/POST | `/storage/folder/create/` | `storage:folder-create` | Create a folder |
| GET/POST | `/storage/folder/<pk>/rename/` | `storage:folder-rename` | Rename a folder |
| GET/POST | `/storage/folder/<pk>/delete/` | `storage:folder-delete` | Delete a folder and descendants |
| GET/POST | `/storage/folder/<folder_id>/upload/` | `storage:file-upload` | Upload a file into a folder |
| GET/POST | `/storage/file/<pk>/rename/` | `storage:file-rename` | Rename a file's displayed name |
| GET/POST | `/storage/file/<pk>/delete/` | `storage:file-delete` | Delete a file |

## Testing and Maintenance

Run Django's project checks and tests from the activated virtual environment:

```powershell
python manage.py check
python manage.py test
```

Useful maintenance commands:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py collectstatic
```

Before creating migrations, update the model code intentionally and review the generated migration. Do not edit an applied migration casually; create a new migration for subsequent schema changes.

## Production Checklist

Before deploying FileVault publicly:

- Set `DJANGO_DEBUG=False`.
- Replace the development `SECRET_KEY` with a strong secret stored outside source control.
- Configure `ALLOWED_HOSTS` with real hostnames.
- Configure CSRF trusted origins and HTTPS settings as appropriate.
- Use PostgreSQL or another production-supported database for the expected workload.
- Run `python manage.py check --deploy`.
- Run `python manage.py collectstatic` and serve static files through a web server or CDN.
- Serve uploaded media through a controlled object-storage or web-server configuration.
- Add upload size, extension, MIME, and malware controls.
- Configure backups for both database records and uploaded files.
- Add logging, monitoring, rate limiting, and error reporting.
- Review authorization for every new file or folder endpoint.
- Use a production WSGI or ASGI server behind a reverse proxy instead of `runserver`.
- Add tests for ownership boundaries, upload validation, deletion behavior, and production database configuration.

## Limitations and Future Enhancements

Potential next steps include:

- Share links with expiration and permission levels
- Search and filtering by name, type, and date
- File versioning and restore
- Per-user storage quotas
- Trash or soft deletion
- Stronger upload validation and antivirus scanning
- Cloud object storage such as Amazon S3 or Azure Blob Storage
- Folder breadcrumbs and bulk operations
- Automated thumbnails and document previews
- API endpoints and a client application
- Expanded automated tests and CI checks

## License

No license file is currently included in the repository. Add a license before distributing FileVault as an open-source project or incorporating it into another product.
