# 📧 Quick Email Setup - 3 Steps

## Step 1: Get Gmail App Password (5 minutes)

### A. Enable 2-Step Verification
1. Visit: https://myaccount.google.com/security
2. Click **2-Step Verification** → **Get Started**
3. Follow the prompts (use your phone)

### B. Generate App Password
1. Visit: https://myaccount.google.com/apppasswords
2. **Select app**: Mail
3. **Select device**: Other (Custom name)
4. Type: "Cohort Django App"
5. Click **Generate**
6. **COPY the 16-character password** ⚠️ (shown once!)
   ```
   Example: abcd efgh ijkl mnop
   ```

---

## Step 2: Update render.yaml

Open `render.yaml` and replace:

```yaml
- key: EMAIL_HOST_USER
  value: your-email@gmail.com
```

with YOUR Gmail:

```yaml
- key: EMAIL_HOST_USER
  value: yourname@gmail.com  # ← Your actual Gmail here
```

Also update:

```yaml
- key: DEFAULT_FROM_EMAIL
  value: yourname@gmail.com  # ← Same Gmail here
```

---

## Step 3: Add Password in Render Dashboard

### After deploying to Render:

1. Go to: https://dashboard.render.com/
2. Click your service: **cohort-backend-api**
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Fill in:
   ```
   Key: EMAIL_HOST_PASSWORD
   Value: [paste your 16-char App Password]
   ```
6. Click **Save**
7. Service will redeploy automatically

---

## ✅ Done! Test It

In Render Console → **Shell**:

```python
from django.core.mail import send_mail

send_mail(
    'Test from Cohort',
    'If you receive this, email is working!',
    'yourname@gmail.com',
    ['yourname@gmail.com'],  # Send to yourself
)
```

Check your Gmail inbox! 📬

---

## 🚨 Important Notes

- **Don't use your regular Gmail password** - Use App Password!
- **Keep App Password secret** - Never commit to Git
- **Gmail limit**: 500 emails/day (plenty for student project)
- **If you lose App Password**: Delete it and generate a new one

---

## Common Errors

### "Bad credentials"
→ You used regular password instead of App Password

### "2-Step Verification required"
→ Enable 2-Step Verification first (Step 1A)

### "App Passwords not available"
→ Make sure 2-Step Verification is enabled

---

## Values You Need:

| Setting | Your Value |
|---------|------------|
| `EMAIL_HOST` | `smtp.gmail.com` (already set) ✅ |
| `EMAIL_PORT` | `587` (already set) ✅ |
| `EMAIL_USE_TLS` | `True` (already set) ✅ |
| `EMAIL_HOST_USER` | **Your Gmail** ⬅️ UPDATE THIS |
| `EMAIL_HOST_PASSWORD` | **App Password** ⬅️ SET IN RENDER |
| `DEFAULT_FROM_EMAIL` | **Your Gmail** ⬅️ UPDATE THIS |
