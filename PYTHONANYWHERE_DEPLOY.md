# 🚀 PythonAnywhere Deployment Guide - SIMPLE!

**Your Site:** https://ramzi77.pythonanywhere.com

---

## 📋 Quick Setup (5 Steps)

### **Step 1: Upload Your Code**

**Option A: Git (Recommended)**
```bash
# In PythonAnywhere Bash Console:
cd ~
git clone https://github.com/YOUR_USERNAME/gulf_emperor.git
cd gulf_emperor
```

**Option B: Upload Files**
- Use "Files" tab in PythonAnywhere
- Upload your project folder

---

### **Step 2: Create Virtual Environment**

```bash
# In Bash Console:
cd ~/gulf_emperor
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### **Step 3: Configure Django Settings**

Create/Edit: `~/gulf_emperor/.env`

```env
# Basic Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=ramzi77.pythonanywhere.com

# Database (SQLite for testing)
DATABASE_URL=sqlite:///db.sqlite3

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/home/ramzi77/gulf_emperor/staticfiles

# Media Files
MEDIA_URL=/media/
MEDIA_ROOT=/home/ramzi77/gulf_emperor/media

# Email (Console for testing)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Stripe (Your test keys)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

---

### **Step 4: Setup Database & Static Files**

```bash
# In Bash Console:
cd ~/gulf_emperor
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

### **Step 5: Configure Web App**

**Go to:** Web tab in PythonAnywhere

**Click:** "Add a new web app"
- Choose: Manual configuration
- Python version: 3.10

**Configure WSGI File:**

Click on WSGI configuration file, replace with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/ramzi77/gulf_emperor'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Activate virtual environment
activate_this = '/home/ramzi77/gulf_emperor/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Configure Virtual Environment:**
- Virtualenv path: `/home/ramzi77/gulf_emperor/venv`

**Configure Static Files:**
- URL: `/static/`
- Directory: `/home/ramzi77/gulf_emperor/staticfiles`

**Configure Media Files:**
- URL: `/media/`
- Directory: `/home/ramzi77/gulf_emperor/media`

**Click:** Reload button (green button at top)

---

## ✅ Done! Visit Your Site

**Your URL:** https://ramzi77.pythonanywhere.com

---

## 🔧 Quick Settings Update

Update `config/settings.py` for production:

```python
# Add this to ALLOWED_HOSTS
ALLOWED_HOSTS = ['ramzi77.pythonanywhere.com', 'localhost', '127.0.0.1']

# Update CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://ramzi77.pythonanywhere.com',
]
```

---

## 🐛 Troubleshooting

### **Error: "Internal Server Error"**
```bash
# Check error log in PythonAnywhere:
# Web tab → Error log
```

### **Static files not loading**
```bash
# Re-collect static files:
cd ~/gulf_emperor
source venv/bin/activate
python manage.py collectstatic --noinput
# Then reload web app
```

### **Database issues**
```bash
# Run migrations:
cd ~/gulf_emperor
source venv/bin/activate
python manage.py migrate
```

---

## 📝 Common Commands

**Bash Console:**
```bash
# Activate environment
cd ~/gulf_emperor
source venv/bin/activate

# Run management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Check for errors
python manage.py check
```

**After code changes:**
1. Upload/pull new code
2. Run migrations if needed
3. Collect static files if needed
4. **Click Reload** in Web tab

---

## ⚠️ Important Notes

1. **Free Account Limits:**
   - 1 web app
   - Limited CPU time
   - Website sleeps after inactivity

2. **Database:**
   - SQLite is fine for testing
   - For production, upgrade to MySQL

3. **Stripe Webhooks:**
   - Won't work on free account (needs custom domain)
   - Use test mode only

4. **Debug Mode:**
   - Set `DEBUG=False` in production
   - Check error logs in PythonAnywhere

---

## 🔄 Update Process

**When you make changes:**
```bash
# 1. SSH into PythonAnywhere
cd ~/gulf_emperor

# 2. Pull new code
git pull

# 3. Activate environment
source venv/bin/activate

# 4. Run migrations (if models changed)
python manage.py migrate

# 5. Collect static files (if CSS/JS changed)
python manage.py collectstatic --noinput

# 6. Reload web app (in Web tab)
```

---

## 🎯 That's It!

Simple 5-step deployment for testing. Your site should be live at:

**https://ramzi77.pythonanywhere.com**

---

*Last Updated: November 4, 2025*
