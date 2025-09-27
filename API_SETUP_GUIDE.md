# 🚀 YSense Platform v4.0 - API Setup Guide

## 🎯 **Goal: Get Your Platform Live with Full AI Capabilities**

Your platform is ready to go live! You just need to add your API keys to enable the full AI functionality.

---

## 📋 **Step 1: Create .env File**

Create a file named `.env` in your project root directory with this content:

```bash
# YSense Platform v4.0 - Production Environment Configuration
# ================================================================

# Platform Configuration
PLATFORM_VERSION=4.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# API Keys - ADD YOUR ACTUAL API KEYS HERE
# ========================================

# QWEN API (Alibaba Cloud) - Primary AI Engine
# Get your key from: https://dashscope.aliyun.com
QWEN_API_KEY=your_qwen_api_key_here
QWEN_MODEL=qwen-turbo

# Anthropic API (Claude) - Advanced Reasoning
# Get your key from: https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here
ANTHROPIC_MODEL=claude-3-sonnet

# Security Configuration
# =====================
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Database Configuration
# =====================
USE_POSTGRESQL=false
DATABASE_URL=sqlite:///ysense_local.db

# Email Configuration (for key recovery)
# =====================================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here

# Revenue Settings
# ================
BASE_RATE_EUR=0.10
PLATFORM_FEE_PERCENTAGE=15

# CORS Settings
# =============
ALLOWED_ORIGINS=http://localhost:8501,http://localhost:8502,https://ysenseai.org

# API Rate Limiting
# =================
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=900
```

---

## 🔑 **Step 2: Get Your API Keys**

### **QWEN API Key (Required for Core AI Functions)**

1. **Visit**: [https://dashscope.aliyun.com](https://dashscope.aliyun.com)
2. **Sign up/Login** with your account
3. **Navigate to**: API Keys section
4. **Create new API key**
5. **Copy the key** and replace `your_qwen_api_key_here` in your `.env` file

**Cost**: Very affordable - approximately 80% cheaper than OpenAI
**Usage**: Powers your Five-Layer Perception Toolkit and story analysis

### **Anthropic API Key (Required for Advanced Reasoning)**

1. **Visit**: [https://console.anthropic.com](https://console.anthropic.com)
2. **Sign up/Login** with your account
3. **Navigate to**: API Keys section
4. **Create new API key** (starts with `sk-ant-`)
5. **Copy the key** and replace `sk-ant-your_anthropic_key_here` in your `.env` file

**Cost**: Pay-per-use, very reasonable for your expected volume
**Usage**: Powers your 7 intelligent agents and advanced reasoning

---

## 🔐 **Step 3: Generate Security Keys**

Replace these placeholder values in your `.env` file:

```bash
# Generate these using Python or online tools
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

**Quick way to generate them:**
```python
import secrets
print("SECRET_KEY=" + secrets.token_hex(32))
print("JWT_SECRET_KEY=" + secrets.token_hex(32))
print("ENCRYPTION_KEY=" + secrets.token_hex(32))
```

---

## 📧 **Step 4: Configure Email (Optional but Recommended)**

For the crypto key recovery feature:

1. **Use Gmail**: Set up an App Password
2. **Replace in .env**:
   - `SMTP_USERNAME=your_email@gmail.com`
   - `SMTP_PASSWORD=your_app_password_here`

**Gmail App Password Setup:**
1. Go to Google Account settings
2. Security → 2-Step Verification → App passwords
3. Generate password for "Mail"
4. Use that password in your `.env` file

---

## 🚀 **Step 5: Test Your Setup**

After creating your `.env` file with real API keys:

```bash
# Test the platform
python test_v4_complete.py
```

**Expected Results:**
- ✅ User registration with crypto keys
- ✅ Real AI story analysis (QWEN)
- ✅ Advanced agent reasoning (Anthropic)
- ✅ Full v4.0 workflow working

---

## 🌐 **Step 6: Deploy to Production**

Your platform is now ready for production deployment!

### **Current Status:**
- ✅ **Backend**: Fully operational
- ✅ **Frontend**: Both v3.0 and v4.0 working
- ✅ **Database**: SQLite configured
- ✅ **APIs**: Ready for your keys
- ✅ **Security**: Crypto key authentication
- ✅ **Domain**: ysenseai.org configured

### **Deployment Options:**

**Option 1: Keep Local Development**
- Perfect for testing and development
- Full control over your environment
- Easy to debug and modify

**Option 2: Deploy to Cloud (Recommended)**
- **Heroku**: Easy deployment, free tier available
- **Railway**: Modern platform, good for Python apps
- **DigitalOcean**: More control, reasonable pricing
- **AWS/GCP**: Enterprise-grade, more complex setup

---

## 💰 **Cost Estimation**

**QWEN API**: ~$5-20/month (depending on usage)
**Anthropic API**: ~$10-30/month (depending on usage)
**Total**: ~$15-50/month for full AI capabilities

**This is very reasonable for a production AI platform!**

---

## 🎯 **What Happens After Setup**

Once you add your API keys:

1. **Real AI Analysis**: Your Five-Layer Perception Toolkit will use actual AI
2. **Intelligent Agents**: All 7 agents will provide real strategic insights
3. **Cultural Understanding**: Better Malaysian/Southeast Asian context
4. **Quality Scoring**: Accurate revenue potential calculations
5. **Professional Responses**: Real AI-generated user interactions

---

## 🆘 **Need Help?**

If you encounter any issues:

1. **Check API Keys**: Make sure they're correctly formatted
2. **Test Individual APIs**: Use the test scripts provided
3. **Check Logs**: Look at the terminal output for error messages
4. **Verify .env File**: Ensure it's in the correct location

---

## ✅ **You're Almost There!**

Your YSense platform is 95% ready for production. Just add your API keys and you'll have a fully functional AI-powered wisdom platform!

**Next Steps:**
1. Create `.env` file with your API keys
2. Test the platform
3. Deploy to production
4. Start collecting wisdom! 🎉
