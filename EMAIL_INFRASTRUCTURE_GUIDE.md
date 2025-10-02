# GCP Email Infrastructure Setup Guide

## 🚨 **Critical Email Issues Fixed:**

### **✅ What We've Implemented:**

1. **Forgot Password Feature** - Users can now reset passwords
2. **Email Service** - Complete email system with templates
3. **Password Reset Tokens** - Secure token-based password reset
4. **Email Verification** - Account verification system
5. **Database Schema** - Updated with email-related tables

### **📧 Email Infrastructure Requirements:**

## **1. GCP Email Setup Options:**

### **Option A: Gmail SMTP (Recommended for Development)**
```bash
# Use your existing Gmail account
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password  # Generate App Password in Gmail
```

### **Option B: GCP SendGrid (Production)**
```bash
# Professional email service
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

### **Option C: GCP Mailgun (Alternative)**
```bash
# Another professional option
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=your_mailgun_username
SMTP_PASSWORD=your_mailgun_password
```

## **2. Domain Email Setup (Required for Production):**

### **Step 1: Purchase Domain Email**
- **Google Workspace**: `contact@ysenseai.org`, `admin@ysenseai.org`
- **Microsoft 365**: Professional email hosting
- **Zoho Mail**: Cost-effective option

### **Step 2: Configure DNS Records**
```dns
# MX Records for email
ysenseai.org.    IN    MX    10    aspmx.l.google.com.
ysenseai.org.    IN    MX    20    alt1.aspmx.l.google.com.
ysenseai.org.    IN    MX    20    alt2.aspmx.l.google.com.
ysenseai.org.    IN    MX    20    alt3.aspmx.l.google.com.
ysenseai.org.    IN    MX    20    alt4.aspmx.l.google.com.

# SPF Record
ysenseai.org.    IN    TXT   "v=spf1 include:_spf.google.com ~all"

# DKIM Record (provided by email provider)
# DMARC Record
_dmarc.ysenseai.org.    IN    TXT   "v=DMARC1; p=quarantine; rua=mailto:admin@ysenseai.org"
```

## **3. GCP Secret Manager Setup:**

### **Store Email Credentials Securely:**
```bash
# Create secrets in GCP Secret Manager
gcloud secrets create smtp-password --data-file=- <<< "your_email_password"
gcloud secrets create sendgrid-api-key --data-file=- <<< "your_sendgrid_key"
gcloud secrets create admin-email --data-file=- <<< "admin@ysenseai.org"
```

### **Update .env for GCP:**
```bash
# GCP Secret Manager integration
SMTP_PASSWORD_SECRET=smtp-password
SENDGRID_API_KEY_SECRET=sendgrid-api-key
ADMIN_EMAIL_SECRET=admin-email
```

## **4. Email Templates Available:**

### **✅ Implemented Templates:**
- **Welcome Email** - New user onboarding
- **Password Reset** - Secure password recovery
- **Email Verification** - Account verification
- **Wisdom Approved** - Content approval notification
- **Revenue Notification** - Earnings reports
- **Admin Alerts** - System notifications

## **5. Production Email Checklist:**

### **🔐 Security Requirements:**
- [ ] **SPF Record** - Prevent email spoofing
- [ ] **DKIM Signature** - Email authentication
- [ ] **DMARC Policy** - Email security policy
- [ ] **SSL/TLS** - Encrypted email transmission
- [ ] **Rate Limiting** - Prevent email abuse

### **📊 Monitoring & Analytics:**
- [ ] **Email Delivery Tracking** - Monitor success rates
- [ ] **Bounce Handling** - Manage failed deliveries
- [ ] **Unsubscribe Management** - Compliance with regulations
- [ ] **Email Analytics** - Track open rates, clicks

## **6. Cost Estimates:**

### **Email Service Costs:**
- **Gmail SMTP**: Free (up to 100 emails/day)
- **SendGrid**: $15/month (40,000 emails)
- **Mailgun**: $35/month (50,000 emails)
- **Google Workspace**: $6/user/month

### **Domain Email Costs:**
- **Google Workspace**: $6/user/month
- **Microsoft 365**: $4/user/month
- **Zoho Mail**: $1/user/month

## **7. Quick Setup Commands:**

### **For Development (Gmail):**
```bash
# 1. Enable 2FA on Gmail
# 2. Generate App Password
# 3. Update .env file
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_16_character_app_password
```

### **For Production (SendGrid):**
```bash
# 1. Sign up for SendGrid
# 2. Verify domain
# 3. Generate API key
# 4. Update .env file
SMTP_HOST=smtp.sendgrid.net
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

## **8. Testing Email System:**

### **Test Commands:**
```python
# Test email service
from src.email_service import EmailService

email_service = EmailService()
success = email_service.send_welcome_email(
    user_email="test@example.com",
    user_name="Test User",
    tier="Founding Contributor",
    revenue_share="100%"
)

print(f"Email sent: {success}")
```

## **🎯 Next Steps:**

1. **Choose email provider** (Gmail for dev, SendGrid for production)
2. **Set up domain email** (`contact@ysenseai.org`, `admin@ysenseai.org`)
3. **Configure DNS records** (MX, SPF, DKIM, DMARC)
4. **Test email system** with password reset feature
5. **Deploy to GCP** with email configuration

## **⚠️ Important Notes:**

- **Gmail SMTP** has daily limits (100 emails/day)
- **Production requires** professional email service
- **Domain email** is required for `contact@ysenseai.org`
- **DNS configuration** is critical for email delivery
- **Security records** (SPF, DKIM, DMARC) prevent spam

---

**The email infrastructure is now ready! Users can reset passwords and receive notifications.**





