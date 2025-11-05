# 🔍 Debug Steps - Find the Problem

## Step 1: Use Debug WSGI

1. **Copy content from `debug_wsgi.py`**
2. **Go to Web tab → WSGI configuration file**
3. **Replace ALL content with the debug code**
4. **Save and Reload**
5. **Visit your site** - it will show diagnostic information

This will tell us:
- ✅ Does `/home/ramzi77/gulf_emperor` exist?
- ✅ Does `/home/ramzi77/gulf_emperor/config` exist?
- ✅ What files are in the directory?
- ✅ Is Python finding the right paths?

---

## Step 2: Verify Code Upload

Open **Bash Console** and run:

```bash
# Check if project exists
ls -la /home/ramzi77/

# Check project contents
ls -la /home/ramzi77/gulf_emperor/

# Check config folder
ls -la /home/ramzi77/gulf_emperor/config/
```

**Expected Output:**
```
/home/ramzi77/gulf_emperor/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
├── manage.py
├── requirements.txt
└── venv/
```

---

## Step 3: Common Issues

### **Issue A: Code Not Uploaded**
If `ls /home/ramzi77/gulf_emperor/` shows "No such file or directory":

```bash
# Upload code via git
cd ~
git clone YOUR_GITHUB_REPO_URL gulf_emperor
```

Or use **Files tab** to upload.

---

### **Issue B: Wrong Directory Structure**
If files are there but config folder is missing:

Check if your code structure is:
```
/home/ramzi77/gulf_emperor/gulf_emperor/config/
```

If so, your WSGI should use:
```python
project_home = '/home/ramzi77/gulf_emperor/gulf_emperor'
```

---

### **Issue C: Python Version Mismatch**
Check your venv Python version:

```bash
ls /home/ramzi77/gulf_emperor/venv/lib/
```

If you see `python3.10` but using 3.13, either:
- Change WSGI to use `PYTHON_VERSION = '3.10'`
- Or recreate venv with 3.13

---

## Step 4: Verify Virtualenv

```bash
cd ~/gulf_emperor
source venv/bin/activate

# Check Python version
python --version

# Check Django installed
python -c "import django; print(django.get_version())"

# List installed packages
pip list
```

---

## Step 5: Test Django Manually

```bash
cd ~/gulf_emperor
source venv/bin/activate

# Try to import config
python -c "import config.settings"

# If that works, try Django
python manage.py check
```

If these work in bash but not in WSGI, the issue is WSGI path configuration.

---

## Quick Checklist

Run these in **Bash Console**:

```bash
# 1. Does project exist?
test -d ~/gulf_emperor && echo "✅ Project exists" || echo "❌ Project missing"

# 2. Does config exist?
test -d ~/gulf_emperor/config && echo "✅ Config exists" || echo "❌ Config missing"

# 3. Does settings.py exist?
test -f ~/gulf_emperor/config/settings.py && echo "✅ Settings exists" || echo "❌ Settings missing"

# 4. Does venv exist?
test -d ~/gulf_emperor/venv && echo "✅ Venv exists" || echo "❌ Venv missing"

# 5. Check Python version in venv
ls ~/gulf_emperor/venv/lib/
```

---

## After Debugging

Once you find the issue:
1. Fix the problem
2. Replace debug WSGI with the real one from `pythonanywhere_wsgi.py`
3. Click Reload
4. Check error log if still failing

---

**Start with Step 1 (Debug WSGI) and share what you see!** 🔍
