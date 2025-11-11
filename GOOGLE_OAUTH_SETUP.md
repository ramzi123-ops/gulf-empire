# Google OAuth Authentication Setup Guide

## 🎯 Overview
This guide will help you set up Google OAuth authentication for the Gulf Emperor e-commerce platform, allowing users to sign up and log in using their Google accounts.

---

## 📋 Step 1: Install Required Package

Run this command in your terminal:

```bash
pip install django-allauth
```

Then update your `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---

## 🔑 Step 2: Get Google OAuth Credentials

### 2.1 Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2.2 Create a New Project (or select existing)
1. Click on the project dropdown (top left)
2. Click "New Project"
3. Name it: **Gulf Emperor** (or your preferred name)
4. Click "Create"

### 2.3 Enable Google+ API
1. In the left sidebar, go to **"APIs & Services" > "Library"**
2. Search for **"Google+ API"**
3. Click on it and press **"Enable"**

### 2.4 Configure OAuth Consent Screen
1. Go to **"APIs & Services" > "OAuth consent screen"**
2. Select **"External"** (for public users)
3. Click **"Create"**
4. Fill in the required fields:
   - **App name**: Gulf Emperor
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click **"Save and Continue"**
6. Skip "Scopes" → Click **"Save and Continue"**
7. Skip "Test users" → Click **"Save and Continue"**
8. Click **"Back to Dashboard"**

### 2.5 Create OAuth Client ID
1. Go to **"APIs & Services" > "Credentials"**
2. Click **"Create Credentials" > "OAuth client ID"**
3. Choose **"Web application"**
4. Fill in:
   - **Name**: Gulf Emperor Web Client
   - **Authorized JavaScript origins**:
     ```
     http://localhost:8000
     http://127.0.0.1:8000
     https://yourdomain.com
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:8000/accounts/google/login/callback/
     http://127.0.0.1:8000/accounts/google/login/callback/
     https://yourdomain.com/accounts/google/login/callback/
     ```
5. Click **"Create"**
6. **IMPORTANT**: Copy your **Client ID** and **Client Secret** - you'll need these!

---

## 🔧 Step 3: Configure Environment Variables

Add these to your `.env` file:

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

**Replace** `your_client_id_here` and `your_client_secret_here` with the credentials from Step 2.5

---

## 💾 Step 4: Run Database Migrations

Run these commands to create necessary database tables:

```bash
python manage.py migrate
```

This will create:
- `django_site` table
- `socialaccount` tables
- `socialapp` tables

---

## 🌐 Step 5: Configure Site in Django Admin

1. Run your server:
   ```bash
   python manage.py runserver
   ```

2. Go to Django Admin:
   ```
   http://127.0.0.1:8000/admin/
   ```

3. Navigate to **"Sites"** (under Django Contrib)
4. Edit the existing site or create new one:
   - **Domain name**: `127.0.0.1:8000` (for local) or `yourdomain.com` (for production)
   - **Display name**: Gulf Emperor
5. **Note the Site ID** (should be `1` if it's your first site)

6. Navigate to **"Social applications"** (under Social Accounts)
7. Click **"Add social application"**
8. Fill in:
   - **Provider**: Google
   - **Name**: Gulf Emperor Google Login
   - **Client id**: Paste your Google Client ID
   - **Secret key**: Paste your Google Client Secret
   - **Sites**: Select your site (Gulf Emperor) and move it to "Chosen sites"
9. Click **"Save"**

---

## ✅ Step 6: Test the Integration

### 6.1 Test Login Page
1. Go to: `http://127.0.0.1:8000/auth/login/`
2. You should see:
   - Regular login form
   - "أو" (Or) divider
   - **"تسجيل الدخول باستخدام Google"** button with Google logo

### 6.2 Test Register Page
1. Go to: `http://127.0.0.1:8000/auth/register/`
2. You should see:
   - Regular registration form
   - "أو" (Or) divider
   - **"التسجيل باستخدام Google"** button with Google logo

### 6.3 Test Google Authentication Flow
1. Click the Google button
2. You'll be redirected to Google's login page
3. Select your Google account
4. Grant permissions
5. You'll be redirected back and automatically logged in!

---

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
**Solution**: Make sure the redirect URI in Google Cloud Console exactly matches:
```
http://127.0.0.1:8000/accounts/google/login/callback/
```

### Error: "Site matching query does not exist"
**Solution**: 
1. Check `SITE_ID = 1` in `settings.py`
2. Verify the site exists in Django admin
3. Run migrations again if needed

### Error: "SocialApp matching query does not exist"
**Solution**:
1. Go to Django admin
2. Add Social Application (Step 5.6)
3. Make sure you selected the correct site

### Google button doesn't work
**Solution**:
1. Check that `django-allauth` is installed
2. Verify URL is correct: `{% url 'google_login' %}`
3. Check browser console for errors

---

## 📱 For Production Deployment

### Update `.env` for production:
```env
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
```

### Update Google Cloud Console:
1. Add production domain to **Authorized JavaScript origins**:
   ```
   https://yourdomain.com
   ```
2. Add production callback to **Authorized redirect URIs**:
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```

### Update Django Admin:
1. Update the **Site** domain to your production domain
2. Update **Social Application** if needed

---

## 🔒 Security Best Practices

1. ✅ **Never commit** `.env` file to Git
2. ✅ Keep `GOOGLE_CLIENT_SECRET` private
3. ✅ Use different credentials for development and production
4. ✅ Set `ACCOUNT_EMAIL_VERIFICATION = 'mandatory'` for production
5. ✅ Enable HTTPS for production
6. ✅ Regularly rotate secrets

---

## 📚 Additional Features

### Get User Information from Google
When users sign in with Google, you automatically get:
- ✅ Email address
- ✅ First name
- ✅ Last name
- ✅ Profile picture (if you configure it)

The user is created automatically in your database with this information!

### Customize Sign-Up Process
You can customize what happens after Google sign-up in:
```python
# settings.py
SOCIALACCOUNT_AUTO_SIGNUP = True  # Auto-create account
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # or 'mandatory'
```

---

## 🎉 Success!

Users can now:
- ✅ Sign up with Google in one click
- ✅ Log in with Google without password
- ✅ Automatically have their email and name filled
- ✅ Enjoy a seamless authentication experience

---

## 📞 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify all steps were completed
3. Check Django server logs for errors
4. Review Google Cloud Console settings

---

**Last Updated**: November 2025  
**Django Version**: 5.2.7  
**django-allauth Version**: Latest
