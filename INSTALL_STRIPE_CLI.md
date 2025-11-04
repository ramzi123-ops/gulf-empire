# 🚀 Install Stripe CLI - Windows

## Method 1: Direct Download (Easiest)

1. **Download Stripe CLI:**
   - Go to: https://github.com/stripe/stripe-cli/releases/latest
   - Download: `stripe_X.X.X_windows_x86_64.zip`

2. **Extract:**
   - Extract the ZIP file
   - You'll get `stripe.exe`

3. **Move to a permanent location:**
   ```powershell
   # Create directory
   mkdir C:\stripe
   
   # Move stripe.exe there
   # (Manually move the file to C:\stripe\)
   ```

4. **Add to PATH (Optional but recommended):**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to "Advanced" tab → "Environment Variables"
   - Under "User variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\stripe`
   - Click OK on all windows
   - **Restart PowerShell**

5. **Verify:**
   ```powershell
   stripe --version
   ```

---

## Method 2: Using PowerShell (Quick)

Run this in PowerShell (Admin):

```powershell
# Download latest Stripe CLI
$url = "https://github.com/stripe/stripe-cli/releases/latest/download/stripe_windows_x86_64.zip"
$output = "$env:TEMP\stripe.zip"
Invoke-WebRequest -Uri $url -OutFile $output

# Extract
Expand-Archive -Path $output -DestinationPath "C:\stripe" -Force

# Add to current session PATH
$env:Path += ";C:\stripe"

# Verify
stripe --version
```

---

## Method 3: Without Installation (Direct Run)

If you don't want to install globally, just:

1. Download `stripe.exe` from: https://github.com/stripe/stripe-cli/releases/latest
2. Put it in your project folder
3. Run it directly:
   ```powershell
   .\stripe.exe login
   .\stripe.exe listen --forward-to localhost:8000/payments/webhook/stripe/
   ```

---

## After Installation:

### 1. Login to Stripe:
```powershell
stripe login
```
- Opens browser to authorize
- Returns to terminal when done

### 2. Start Webhook Forwarding:
```powershell
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

### 3. Copy Webhook Secret:
You'll see output like:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

### 4. Add to .env:
```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### 5. Restart Django Server

### 6. Test Payment Again!

---

## Quick Test (After Setup):

1. ✅ Stripe CLI running in one terminal
2. ✅ Django server running in another terminal
3. ✅ Go to payment page
4. ✅ Use card: `4242 4242 4242 4242`
5. ✅ Watch webhook events in Stripe CLI terminal!

---

## Expected Output in Stripe CLI:

```
2025-11-04 19:45:23   --> payment_intent.created [evt_xxx]
2025-11-04 19:45:24   --> payment_intent.succeeded [evt_xxx]
2025-11-04 19:45:24  <--  [200] POST http://localhost:8000/payments/webhook/stripe/
```

---

## Troubleshooting:

**"stripe: command not found"**
→ Add `C:\stripe` to PATH and restart terminal

**"Cannot open browser"**
→ Copy the URL and paste in browser manually

**"Webhook secret invalid"**
→ Make sure you copied the `whsec_` value to .env

**"Connection refused"**
→ Make sure Django server is running on port 8000

---

Choose Method 1 or 2, then continue with the setup steps!
