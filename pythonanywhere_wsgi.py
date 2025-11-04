"""
WSGI Configuration for PythonAnywhere

Copy this content to your WSGI configuration file in PythonAnywhere
Web tab → WSGI configuration file

IMPORTANT: Replace 'ramzi77' with your actual PythonAnywhere username
"""

import os
import sys

# ============================================================================
# Add your project directory to Python path
# ============================================================================
# Replace 'ramzi77' with your PythonAnywhere username
project_home = '/home/ramzi77/gulf_emperor'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================================================
# Set Django settings module
# ============================================================================
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# ============================================================================
# Activate virtual environment
# ============================================================================
# Replace 'ramzi77' with your PythonAnywhere username
activate_this = '/home/ramzi77/gulf_emperor/venv/bin/activate_this.py'

try:
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})
except FileNotFoundError:
    # If activate_this.py doesn't exist, try alternative method
    pass

# ============================================================================
# Load environment variables from .env file
# ============================================================================
from dotenv import load_dotenv
env_path = os.path.join(project_home, '.env')
load_dotenv(env_path)

# ============================================================================
# Import Django WSGI application
# ============================================================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
