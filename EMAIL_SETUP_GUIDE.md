# 📧 Email Configuration Guide - IMPORTANT!

## 🚨 SECURITY WARNING

**NEVER hardcode passwords in settings.py!** I noticed you had the password directly in the file. I've fixed this, but you need to update your `.env` file.

---

## ✅ Step-by-Step Gmail Setup

### **Step 1: Enable 2-Factor Authentication**
1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Follow the setup wizard

### **Step 2: Generate App Password**
1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Name it: **Django Gulf Emperor**
5. Click **Generate**
6. **Copy the 16-character password** (like: `abcd efgh ijkl mnop`)

### **Step 3: Update Your .env File**

Open `.env` file and add/update these lines:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=ramzihaidan537@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_app_password_here
DEFAULT_FROM_EMAIL=Gulf Emperor <noreply@gulfemperor.com>
```

**Example:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=ramzihaidan537@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Gulf Emperor <ramzihaidan537@gmail.com>
```

---

## ⚠️ Common Issues & Solutions

### **Issue 1: "Username and Password not accepted"**
**Solution:** You're using your regular Gmail password. You MUST use an **App Password**.

### **Issue 2: "SMTPAuthenticationError"**
**Solutions:**
1. Enable 2-Factor Authentication first
2. Generate a new App Password
3. Make sure no spaces in the password when copying to .env
4. Try using your email as FROM email too

### **Issue 3: "Connection refused"**
**Solutions:**
1. Check firewall settings
2. Make sure port 587 is open
3. Try port 465 with EMAIL_USE_SSL=True instead of EMAIL_USE_TLS

---

## 🧪 Test Email Configuration

### **Quick Test (Django Shell):**
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test message from Gulf Emperor.',
    'ramzihaidan537@gmail.com',
    ['ramzihaidan537@gmail.com'],
    fail_silently=False,
)
```

**Expected:** Email arrives in your inbox within 1-2 minutes.

---

## 📝 Alternative: For Development Only

If you don't need actual emails during development, use console backend:

**In settings.py:**
```python
# For development only
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the terminal instead of sending them.

---

## ✅ Final Checklist

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated
- [ ] `.env` file updated with App Password
- [ ] No hardcoded passwords in settings.py
- [ ] Test email sent successfully
- [ ] Django server restarted after .env changes

---

## 🔐 Security Best Practices

1. ✅ **Never commit .env file** (already in .gitignore)
2. ✅ **Use App Passwords, not regular passwords**
3. ✅ **Use environment variables** for all secrets
4. ✅ **Different credentials for production**
5. ✅ **Rotate passwords regularly**

---

## 📚 Additional Resources

- **Gmail App Passwords:** https://support.google.com/accounts/answer/185833
- **Django Email:** https://docs.djangoproject.com/en/5.1/topics/email/
- **SMTP Settings:** https://support.google.com/mail/answer/7126229

---

## 🎯 What's Now Fixed

✅ **Password Reset URLs** - Now use proper namespacing
✅ **Email Configuration** - Now reads from .env properly
✅ **Security** - No hardcoded passwords in settings.py
✅ **Success URLs** - All password reset views have proper redirects

---

*Last Updated: November 4, 2025*
