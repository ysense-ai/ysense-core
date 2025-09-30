# Manual .env Setup Guide - Fix API Key Issues

## 🚨 **Problem Identified:**

**The `.env` file is missing!** That's why your API keys aren't being used.

## 🔧 **Solution: Create .env File Manually**

### **Step 1: Create .env File**

1. **Navigate to**: `YSense-Platform-v4.1-Fresh` folder
2. **Create new file** named: `.env` (exactly this name, no extension)
3. **Copy this content** into the file:

```bash
# YSense™ Platform v4.1 Environment Configuration

# =============================================================================
# AI API KEYS
# =============================================================================

# QWEN API (Alibaba Cloud) - Replace with your actual key
QWEN_API_KEY=sk-e****07ef
QWEN_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
QWEN_MODEL=qwen-turbo

# Anthropic API (Claude) - Replace with your actual key  
ANTHROPIC_API_KEY=sk-ant-api03-oTu...EgAA
ANTHROPIC_MODEL=claude-3-sonnet

# =============================================================================
# SECURITY KEYS
# =============================================================================

# JWT Secret Key
JWT_SECRET_KEY=ysense_jwt_secret_key_2025_v41_secure_random_string

# Encryption Key
ENCRYPTION_KEY=ysense_encryption_key_2025_v41_secure_random_string

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Database Path
DATABASE_PATH=ysense_v41.db

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# SMTP Configuration (for future use)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=contact@ysenseai.org
SMTP_PASSWORD=your_email_password_here

# Email Addresses
FROM_EMAIL=contact@ysenseai.org
SUPPORT_EMAIL=support@ysenseai.org
ADMIN_EMAIL=admin@ysenseai.org

# =============================================================================
# PLATFORM CONFIGURATION
# =============================================================================

# Platform URL
PLATFORM_URL=https://ysenseai.org

# Debug Mode
DEBUG=True
```

### **Step 2: Replace API Keys**

**Replace these values with your actual API keys:**

1. **QWEN API Key**: Replace `sk-e****07ef` with your full QWEN key from Alibaba Cloud
2. **Anthropic API Key**: Replace `sk-ant-api03-oTu...EgAA` with your full Anthropic key from Claude Console

### **Step 3: Save and Test**

1. **Save the file** as `.env` (no extension)
2. **Restart the platform**
3. **Test AI Workflow**

## 🔍 **API Key Details from Your Screenshots:**

### **QWEN API (Alibaba Cloud):**
- **Key ID**: 32903
- **Partial Key**: sk-e****07ef
- **Description**: YSense™ v4.1 | 慧觉™ The Genesis of Human-AI Wisdom Collaboration
- **Created**: 2025-09-25 23:00:06

### **Anthropic API (Claude):**
- **Key Name**: alton-onboardin...
- **Partial Key**: sk-ant-api03-oTu...EgAA
- **Workspace**: Default
- **Created**: Sep 24, 2025
- **Last Used**: Never

## 🧪 **Test API Keys:**

### **Option 1: Use Setup Script**
```bash
cd YSense-Platform-v4.1-Fresh
python setup_api_keys.py
```

### **Option 2: Manual Test**
1. Create `.env` file with your keys
2. Restart platform
3. Go to AI Workflow
4. Enter a story
5. Click "Analyze with 6 AI Agents"

## 🎯 **Expected Results:**

### **Before (Current):**
- ❌ Error: `'coroutine' object has no attribute 'get'`
- ❌ Blue message: "This might be due to API key configuration"

### **After (Fixed):**
- ✅ Real AI analysis from QWEN and Anthropic
- ✅ Professional responses from all 6 agents
- ✅ No more errors

## 🔧 **Additional Configuration (If Needed):**

### **QWEN API Additional Setup:**
1. **Check API Key Permissions** in Alibaba Cloud Console
2. **Verify Model Access** (qwen-turbo, qwen-plus, qwen-max)
3. **Check Usage Limits** and billing

### **Anthropic API Additional Setup:**
1. **Check API Key Permissions** in Claude Console
2. **Verify Model Access** (claude-3-sonnet, claude-3-haiku)
3. **Check Usage Limits** and billing

## 🚀 **Quick Fix:**

**Just create the `.env` file with your API keys and restart the platform!**

The error will disappear and you'll get real AI analysis instead of mock results.

## 📞 **Need Help?**

If you're still having issues:
1. **Check API key format** - Make sure no extra spaces or quotes
2. **Verify API key permissions** - Check console settings
3. **Test API keys individually** - Use the setup script
4. **Check network connectivity** - Ensure internet access

**The platform will work perfectly once the `.env` file is created!** 🎉



