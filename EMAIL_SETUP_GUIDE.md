# Email Configuration Guide for Django

## Option 1: Gmail (Recommended - FREE)

### Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** → **2-Step Verification**
3. Follow the setup process

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other** (type "Django App")
4. Click **Generate**
5. **Copy the 16-character password** (you'll only see it once!)

### Step 3: Update render.yaml

Replace the email section with these values:

```yaml
# Email Configuration (Gmail)
- key: EMAIL_BACKEND
  value: django.core.mail.backends.smtp.EmailBackend

- key: EMAIL_HOST
  value: smtp.gmail.com

- key: EMAIL_PORT
  value: 587

- key: EMAIL_USE_TLS
  value: True

- key: EMAIL_HOST_USER
  value: your-email@gmail.com  # Replace with your Gmail

- key: EMAIL_HOST_PASSWORD
  value: xxxx xxxx xxxx xxxx  # Replace with App Password from Step 2

- key: DEFAULT_FROM_EMAIL
  value: your-email@gmail.com  # Same as EMAIL_HOST_USER
```

### Step 4: Test Email Sending

After deploying, test in Django shell:

```bash
# On Render Console
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email from Cohort Web.',
    'your-email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

---

## Option 2: Outlook/Hotmail (FREE)

```yaml
- key: EMAIL_HOST
  value: smtp-mail.outlook.com

- key: EMAIL_PORT
  value: 587

- key: EMAIL_USE_TLS
  value: True

- key: EMAIL_HOST_USER
  value: your-email@outlook.com

- key: EMAIL_HOST_PASSWORD
  value: your-password
```

---

## Option 3: SendGrid (FREE tier: 100 emails/day)

### Setup

1. Sign up: https://signup.sendgrid.com/
2. Create API Key:
   - Settings → API Keys → Create API Key
   - Name: "Django Cohort App"
   - Permission: Full Access
   - Copy the API key

### Configuration

```yaml
- key: EMAIL_BACKEND
  value: django.core.mail.backends.smtp.EmailBackend

- key: EMAIL_HOST
  value: smtp.sendgrid.net

- key: EMAIL_PORT
  value: 587

- key: EMAIL_USE_TLS
  value: True

- key: EMAIL_HOST_USER
  value: apikey  # Literally the word "apikey"

- key: EMAIL_HOST_PASSWORD
  value: SG.xxxxxxxxxxxxx  # Your SendGrid API key

- key: DEFAULT_FROM_EMAIL
  value: verified-sender@yourdomain.com  # Must be verified in SendGrid
```

**Note**: SendGrid requires you to verify your sender email address first.

---

## Option 4: Mailgun (FREE tier: 5,000 emails/month)

1. Sign up: https://signup.mailgun.com/
2. Get credentials from Dashboard → Sending → Domain settings

```yaml
- key: EMAIL_BACKEND
  value: django.core.mail.backends.smtp.EmailBackend

- key: EMAIL_HOST
  value: smtp.mailgun.org

- key: EMAIL_PORT
  value: 587

- key: EMAIL_USE_TLS
  value: True

- key: EMAIL_HOST_USER
  value: postmaster@your-domain.mailgun.org

- key: EMAIL_HOST_PASSWORD
  value: your-mailgun-password
```

---

## Recommended: Gmail for Students

**Why Gmail?**
- ✅ **Free** - No cost
- ✅ **Easy setup** - Just need App Password
- ✅ **Reliable** - High deliverability
- ✅ **Limit**: 500 emails/day (enough for your use case)

**For Production/Business:**
- SendGrid or Mailgun (better deliverability)
- Custom domain support
- Better analytics

---

## Security Best Practices

### ⚠️ NEVER commit passwords to Git!

**In render.yaml, use:**
```yaml
- key: EMAIL_HOST_PASSWORD
  sync: false  # This means "set in Render dashboard, not in code"
```

**Then set the password in Render Dashboard:**
1. Go to your service on Render
2. Environment → Add environment variable
3. Key: `EMAIL_HOST_PASSWORD`
4. Value: Your app password
5. Save

---

## Quick Setup Guide (Gmail)

### For render.yaml:

```yaml
# Email Configuration
- key: EMAIL_BACKEND
  value: django.core.mail.backends.smtp.EmailBackend

- key: EMAIL_HOST
  value: smtp.gmail.com

- key: EMAIL_PORT
  value: 587

- key: EMAIL_USE_TLS
  value: True

- key: EMAIL_HOST_USER
  value: YOUR_GMAIL@gmail.com

- key: EMAIL_HOST_PASSWORD
  sync: false  # Set this in Render dashboard for security

- key: DEFAULT_FROM_EMAIL
  value: YOUR_GMAIL@gmail.com
```

### In Render Dashboard:

1. Go to your service
2. **Environment** tab
3. Click **Add Environment Variable**
4. Key: `EMAIL_HOST_PASSWORD`
5. Value: *Paste your 16-character App Password*
6. **Save**

---

## Troubleshooting

### Issue: "SMTPAuthenticationError"

**Cause**: Wrong password or 2-step verification not enabled

**Fix:**
1. Enable 2-Step Verification
2. Generate new App Password
3. Update `EMAIL_HOST_PASSWORD` in Render

### Issue: "SMTPServerDisconnected"

**Cause**: Wrong host or port

**Fix:**
- Gmail: `smtp.gmail.com:587`
- Outlook: `smtp-mail.outlook.com:587`

### Issue: Emails go to Spam

**Solutions:**
1. Use a custom domain (advanced)
2. Add SPF/DKIM records
3. Use SendGrid/Mailgun (better deliverability)

---

## Testing Emails Locally

Create a test script:

```python
# backend/test_email.py
from django.core.mail import send_mail
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

send_mail(
    subject='Test from Cohort Web',
    message='This is a test email.',
    from_email=os.getenv('EMAIL_HOST_USER'),
    recipient_list=['your-test@email.com'],
    fail_silently=False,
)
print("Email sent successfully!")
```

Run it:
```bash
cd backend
python test_email.py
```

---

## Email Limits by Provider

| Provider | Free Tier Limit | Cost for More |
|----------|----------------|---------------|
| **Gmail** | 500/day | N/A (personal use) |
| **Outlook** | Unknown limit | N/A |
| **SendGrid** | 100/day | $19.95/month for 50K |
| **Mailgun** | 5,000/month | $35/month for 50K |
| **AWS SES** | 62,000/month | $0.10 per 1,000 |

For a student project, **Gmail is perfect**! 🎓
