# 🔧 WSGI Configuration Fix

## ✅ Fixes Both Errors:
1. ❌ `activate_this.py` not found
2. ❌ `ModuleNotFoundError: No module named 'config'`

---

## 🚨 IMPORTANT: Check These First!

### **1. Source Code Path (CRITICAL!)**
Go to **Web tab** and set:
- **Source code:** `/home/ramzi77/gulf_emperor`

### **2. Virtualenv Path**
- **Virtualenv:** `/home/ramzi77/gulf_emperor/venv`

### **3. Python Version**
Make sure you selected **Python 3.10** when creating the web app!

---

## 📝 What to Do Now

### **Copy This to Your PythonAnywhere WSGI File:**

Go to: **Web tab → WSGI configuration file**

Replace ALL content with:

```python
import os
import sys

# CONFIGURATION
USERNAME = 'ramzi77'
PROJECT_NAME = 'gulf_emperor'
PYTHON_VERSION = '3.10'

# Project Path
project_home = f'/home/{USERNAME}/{PROJECT_NAME}'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual Environment
import site
venv_packages = f'/home/{USERNAME}/{PROJECT_NAME}/venv/lib/python{PYTHON_VERSION}/site-packages'
site.addsitedir(venv_packages)

# Load .env
try:
    from dotenv import load_dotenv
    env_path = os.path.join(project_home, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

# Django Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django Application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 🔄 After Updating WSGI File

1. **Save** the WSGI file
2. **Click Reload** (green button at top of Web tab)
3. **Visit** your site: https://ramzi77.pythonanywhere.com

---

## ✅ This Should Work Now!

The new WSGI configuration:
- ✅ No longer uses `activate_this.py`
- ✅ Directly adds site-packages to Python path
- ✅ Loads .env variables
- ✅ Works with Python 3.10+

---

## 🐛 If Still Getting Errors

### Check These:

1. **Virtual environment exists?**
   ```bash
   ls /home/ramzi77/gulf_emperor/venv/lib/
   ```
   You should see `python3.10` folder

2. **.env file exists?**
   ```bash
   ls /home/ramzi77/gulf_emperor/.env
   ```

3. **Packages installed?**
   ```bash
   cd ~/gulf_emperor
   source venv/bin/activate
   pip list
   ```

4. **Check error log:**
   Web tab → Error log (link at top)

---

## 📞 Need Help?

If you see different errors, check the error log and let me know!
