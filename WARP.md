# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Gulf Emperor is a Django-based e-commerce platform for automotive parts, using HTMX for dynamic interactions and Tailwind CSS for styling. The project uses a modular, app-based architecture with PostgreSQL as the production database (currently using SQLite in development).

## Common Commands

### Development Setup

```bash
# Python setup (Windows)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements/development.txt

# Node.js setup
npm install
npm run build

# Copy HTMX to static directory (Windows)
copy node_modules\htmx.org\dist\htmx.min.js static\js\

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Running the Development Server

**You must run two terminal processes concurrently:**

```bash
# Terminal 1: Tailwind CSS watcher (auto-recompiles on changes)
npm run watch

# Terminal 2: Django development server
.\venv\Scripts\activate
python manage.py runserver
```

### Building and Testing

```bash
# Build Tailwind CSS for production
npm run build

# Run Django management commands
python manage.py <command>

# Collect static files for production
python manage.py collectstatic
```

## Architecture

### Project Structure

```
gulf_emperor/
├── config/              # Django settings, URLs, WSGI/ASGI
│   └── settings.py      # Settings module (DJANGO_SETTINGS_MODULE='config.settings')
├── apps/                # All Django applications (domain-driven)
│   ├── users/           # User auth, profiles, address management
│   ├── store/           # Product catalog, categories, reviews
│   ├── orders/          # Shopping cart, checkout, order management
│   ├── inventory/       # Stock and inventory logic
│   └── payments/        # Payment gateway integration
├── templates/           # Shared project-level templates (base.html, navbar, footer)
├── apps/*/templates/    # App-specific namespaced templates (e.g., store/product_list.html)
├── assets/              # Source files (input.css, main.js)
├── static/              # Compiled/static files served to users (output.css, htmx.min.js)
├── media/               # User uploads (product images, etc.)
└── requirements/        # Python dependencies split by environment
```

### Key Architectural Patterns

**Django Settings Module:** The project uses `config` as the settings package (`DJANGO_SETTINGS_MODULE='config.settings'`).

**App Organization:** Each app in `apps/` represents a distinct business domain. When creating models, views, or admin classes, organize them in subdirectories:
- `apps/store/models/` (e.g., `product.py`, `category.py`)
- `apps/store/views/` (e.g., `product_views.py`, `category_views.py`)
- `apps/store/admins/` (e.g., `product_admin.py`)

**Template Organization:**
- Global shared templates (base.html, navbar, footer) live in `templates/` at the project root
- Each app contains namespaced templates in `apps/<app>/templates/<app>/` (e.g., `apps/store/templates/store/product_detail.html`)
- HTMX partials are stored in `templates/partials/` or `apps/*/templates/partials/`

**HTMX Integration:** This project uses HTMX for dynamic, server-rendered HTML without heavy JavaScript. HTMX is loaded from `static/js/htmx.min.js` and enables:
- Dynamic content swapping (hx-get, hx-post)
- Partial template updates
- Progressive enhancement patterns

**Static Assets Pipeline:**
- **Source files:** `assets/css/input.css` is the Tailwind source
- **Compiled files:** `npm run build` or `npm run watch` compiles to `static/css/output.css`
- Tailwind watches `templates/**/*.html` and `apps/*/templates/**/*.html` for class usage

**Database:** 
- Currently using SQLite in development (see `config/settings.py`)
- Configured for PostgreSQL in production
- When modifying models, always run `makemigrations` then `migrate`

## Development Workflow

1. **Adding a new feature:** Identify the appropriate app (store, orders, users, etc.) or create a new one with `python manage.py startapp <name>` inside `apps/`
2. **Models:** Define in `apps/<app>/models/`, import in `apps/<app>/models/__init__.py`
3. **Views:** Define in `apps/<app>/views/`, import in `apps/<app>/views/__init__.py`
4. **URLs:** Define in `apps/<app>/urls.py` and include in `config/urls.py`
5. **Templates:** Add to `apps/<app>/templates/<app>/` for app-specific templates or `templates/` for shared ones
6. **Static assets:** Update `assets/css/input.css` and ensure `npm run watch` is running
7. **Admin:** Register models in `apps/<app>/admins/`

## Important Notes

- The project follows Django's app-based architecture where each app is self-contained with its own models, views, templates, and URLs
- All apps are registered in `config/settings.py` under `INSTALLED_APPS` using the `apps.` prefix (e.g., `apps.store`)
- Environment-specific settings should be moved to `.env` (currently hardcoded in settings.py)
- Static files are served from `STATICFILES_DIRS` in development; use `collectstatic` for production
- Templates use Django's template language with HTMX attributes for dynamic behavior
