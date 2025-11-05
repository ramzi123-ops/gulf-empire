"""
WSGI Configuration for PythonAnywhere

Copy this content to your WSGI configuration file in PythonAnywhere
Web tab → WSGI configuration file

IMPORTANT: Replace 'ramzi77' with your actual PythonAnywhere username
"""

import os
import sys

# ============================================================================
# CONFIGURATION - Update these values for your setup
# ============================================================================
USERNAME = 'ramzi77'  # Your PythonAnywhere username
PROJECT_NAME = 'gulf-empire'  # Your project folder name (NOTE: hyphen not underscore!)
PYTHON_VERSION = '3.13'  # Python version used in virtual environment

# ============================================================================
# Project Path Setup
# ============================================================================
project_home = f'/home/{USERNAME}/{PROJECT_NAME}'

# Add project directory to Python path (MUST be first)
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================================================
# Virtual Environment Setup
# ============================================================================
# Add virtual environment's site-packages to Python path
import site
venv_packages = f'/home/{USERNAME}/{PROJECT_NAME}/venv/lib/python{PYTHON_VERSION}/site-packages'

# Add to site-packages directories
site.addsitedir(venv_packages)

# ============================================================================
# Environment Variables
# ============================================================================
# Load .env file before importing Django
try:
    from dotenv import load_dotenv
    env_path = os.path.join(project_home, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    # dotenv not available, skip
    pass

# ============================================================================
# Django Settings
# ============================================================================
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ============================================================================
# Django Application
# ============================================================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
