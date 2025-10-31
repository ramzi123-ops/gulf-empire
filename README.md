# Gulf Emperor

> A production-ready e-commerce platform specializing in automotive parts, built with a modern Django, HTMX, and Tailwind CSS stack. This project features robust admin capabilities, secure payment processing, and an optimized user experience.

## 🛠️ Key Technologies

  * **Backend:** Django
  * **Frontend:** HTMX (for dynamic, server-rendered HTML)
  * **Styling:** Tailwind CSS (utility-first CSS framework)
  * **Database:** PostgreSQL (production-ready)

## 🏛️ Project Structure

This project follows a clean, modular architecture designed for scalability and maintainability.

```text
gulf_emperor/
├── .env.example            # Environment variable template
├── manage.py               # Django's command-line utility
├── package.json            # Node.js dependencies (Tailwind, HTMX)
├── tailwind.config.js      # Tailwind CSS configuration
├── requirements/           # Python dependencies (base.txt, development.txt)
│
├── assets/                 # Frontend SOURCE files (input.css, etc.)
│
├── config/                 # Django project config (settings, urls.py)
│
├── apps/                   # All custom Django applications
│   ├── users/              # User management, auth, profiles
│   ├── store/              # Product catalog, categories, reviews
│   ├── orders/             # Cart, checkout, order management
│   ├── inventory/          # Stock and inventory logic
│   └── payments/           # Payment gateway integration & webhooks
│
├── static/                 # COMPILED static files (output.css, htmx.min.js)
│
├── media/                  # User-uploaded files (e.g., product images)
│
└── templates/              # PROJECT-LEVEL shared templates (base.html)
```

  * **`apps/`**: Each app is a distinct business domain (e.g., `store`, `orders`).
  * **`templates/` (root)**: Holds shared base templates (`base.html`, `navbar.html`).
  * **`apps/*/templates/`**: Each app contains its own namespaced templates (e.g., `apps/store/templates/store/product_list.html`).
  * **`assets/` vs. `static/`**: `assets/` contains source CSS. `npm` scripts compile these into the `static/` directory, which is served to the user.

## ✨ Core Features

  * **E-commerce Engine:** Full product catalog, advanced filtering (compatibility, price), reviews, and inventory management.
  * **Modern UX:** A fast, responsive, and interactive user experience powered by **HTMX**, eliminating the need for a heavy JavaScript framework.
  * **User Management:** Secure user registration, social login, profile management, and order history.
  * **Checkout & Payments:** Multi-step checkout, guest checkout, and integration with multiple gateways (Stripe, PayPal, local methods).
  * **Admin Dashboard:** Custom-built admin capabilities for managing products, orders, customers, and running sales reports.

-----

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine for development.

### Prerequisites

  * Python 
  * Node.js and npm
  * PostgreSQL (or another database)

### 1\. Initial Setup

1.  Clone the repository:

    ```bash
    git clone https://your-repository-url/gulf_emperor.git
    cd gulf_emperor
    ```

2.  Create a Python virtual environment and activate it:

    ```bash
    python -m venv venv

    # On macOS/Linux
    source venv/bin/activate

    # On Windows
    .\venv\Scripts\activate
    ```

### 2\. Backend Setup (Python)

1.  Install the required Python dependencies:
    *(Note: You will need to create these `requirements` files first. A good starting point is `pip freeze > requirements/base.txt` after installing `django psycopg2-binary pillow`)*.

    ```bash
    pip install -r requirements/development.txt
    ```

2.  Set up your environment variables. Copy the example file and fill in your details (database credentials, secret key, etc.).

    ```bash
    cp .env.example .env
    ```

    > **Note:** You must edit the `.env` file with your local database settings.

3.  Set up the database. Ensure your PostgreSQL server is running and you've created the database specified in your `.env` file.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  Create a superuser to access the admin:

    ```bash
    python manage.py createsuperuser
    ```

### 3\. Frontend Setup (Node.js)

1.  Install the required `npm` packages:

    ```bash
    npm install
    ```

2.  Copy the `htmx.min.js` file from `node_modules` to your `static/js` directory so Django can serve it:

    ```bash
    # On macOS/Linux
    cp node_modules/htmx.org/dist/htmx.min.js static/js/

    # On Windows
    copy node_modules\htmx.org\dist\htmx.min.js static\js\
    ```

3.  Run an initial build of your Tailwind CSS:

    ```bash
    npm run build
    ```

-----

## 🖥️ Running the Development Server

You must run **two separate terminal processes** for development.

### Terminal 1: Tailwind CSS Watcher

This terminal will watch for any changes in your `templates` or `assets` files and automatically re-compile your `output.css` file.

```bash
# Activates the Tailwind watcher
npm run watch
```

### Terminal 2: Django Development Server

This terminal runs the main Django application.

```bash
# (Make sure your virtual environment is active)
source venv/bin/activate

# Run the Django server
python manage.py runserver
```

You can now access the application at **`http://127.0.0.1:8000`**.

-----

Would you like me to help you create the `requirements/` files or the `.env.example` file next?