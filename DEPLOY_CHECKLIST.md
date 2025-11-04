# ✅ PythonAnywhere Deployment Checklist

**Site:** https://ramzi77.pythonanywhere.com

---

## 📦 Pre-Deployment

- [ ] Code is pushed to GitHub
- [ ] All migrations are created locally
- [ ] Static files work locally
- [ ] Admin panel accessible locally

---

## 🚀 Deployment Steps

### **1. Upload Code** ✅
```bash
# In PythonAnywhere Bash Console
cd ~
git clone YOUR_GITHUB_REPO_URL gulf_emperor
cd gulf_emperor
```

### **2. Virtual Environment** ✅
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **3. Environment File** ✅
```bash
# Copy the example file
cp env.pythonanywhere.example .env

# Edit the .env file
nano .env

# Update:
# - SECRET_KEY (generate new one)
# - DEBUG=False
# - ALLOWED_HOSTS=ramzi77.pythonanywhere.com
# - Stripe keys
```

### **4. Django Setup** ✅
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### **5. Configure Web App** ✅

**Go to Web tab:**

1. **Add new web app** → Manual configuration → Python 3.10

2. **Source code:** `/home/ramzi77/gulf_emperor`

3. **Virtual environment:** `/home/ramzi77/gulf_emperor/venv`

4. **WSGI file:** Click to edit, copy content from `pythonanywhere_wsgi.py`

5. **Static files:**
   - URL: `/static/`
   - Directory: `/home/ramzi77/gulf_emperor/staticfiles`

6. **Media files:**
   - URL: `/media/`
   - Directory: `/home/ramzi77/gulf_emperor/media`

7. **Click:** Reload (green button)

---

## 🧪 Testing

- [ ] Visit https://ramzi77.pythonanywhere.com
- [ ] Home page loads ✅
- [ ] Admin login works `/admin/` ✅
- [ ] Static files load ✅
- [ ] Products display ✅
- [ ] Cart works ✅
- [ ] Registration works ✅
- [ ] Login works ✅

---

## 🔄 Update Process

When you make changes:

```bash
# 1. Pull latest code
cd ~/gulf_emperor
git pull

# 2. Activate environment
source venv/bin/activate

# 3. Install new packages (if any)
pip install -r requirements.txt

# 4. Run migrations (if models changed)
python manage.py migrate

# 5. Collect static files (if CSS/JS changed)
python manage.py collectstatic --noinput

# 6. Reload web app
# Go to Web tab → Click Reload
```

---

## 🐛 Troubleshooting

### Check Error Logs
```
Web tab → Error log (link at top)
Web tab → Server log (link at top)
```

### Common Issues

**Issue:** "Internal Server Error"
```bash
# Check logs and ensure:
- WSGI file is correct
- Virtual environment path is correct
- .env file exists
```

**Issue:** "Static files not loading"
```bash
python manage.py collectstatic --noinput
# Then reload web app
```

**Issue:** "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📝 Important Files

- `requirements.txt` - Python packages
- `pythonanywhere_wsgi.py` - WSGI configuration
- `env.pythonanywhere.example` - Environment variables template
- `.env` - Your actual environment file (create this)

---

## ⚠️ Remember

1. ✅ Set `DEBUG=False` in production
2. ✅ Use strong `SECRET_KEY`
3. ✅ Check error logs if issues
4. ✅ Reload web app after changes
5. ✅ Free account has CPU limits

---

## 🎯 Quick Commands

```bash
# Connect to bash
cd ~/gulf_emperor
source venv/bin/activate

# Django commands
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py check

# View logs
tail -f /var/log/ramzi77.pythonanywhere.com.error.log
```

---

**Status:** Ready to Deploy! 🚀
