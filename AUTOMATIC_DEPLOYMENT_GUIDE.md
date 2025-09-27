# 🚀 YSense™ v4.0 Automatic Deployment Guide

## Overview
This guide shows you how to set up automatic deployment so that any updates to your platform v4.0 are automatically deployed to the live platform.

## 🎯 Deployment Options

### Option 1: Vercel (Recommended - Easiest)
**Best for**: Quick setup, automatic updates, free tier available

#### Setup Steps:
1. **Go to [vercel.com](https://vercel.com)**
2. **Sign up with GitHub** (connect your `ysense-ai` account)
3. **Import Repository**: `ysense-ai/ysense-core`
4. **Configure Settings**:
   - Framework Preset: `Other`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `./`
5. **Add Environment Variables**:
   - `QWEN_API_KEY`: Your QWEN API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `JWT_SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `ENCRYPTION_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
6. **Deploy**: Click "Deploy"

#### Automatic Updates:
- ✅ **Every push to `main` branch** = Automatic deployment
- ✅ **Preview deployments** for pull requests
- ✅ **Zero downtime** updates

### Option 2: Railway
**Best for**: Full-stack apps, database support

#### Setup Steps:
1. **Go to [railway.app](https://railway.app)**
2. **Connect GitHub** and select `ysense-ai/ysense-core`
3. **Configure**:
   - Use `Procfile` (already created)
   - Add environment variables (same as Vercel)
4. **Deploy**

### Option 3: Google Cloud Platform (GCP)
**Best for**: Enterprise scale, full control

#### Setup Steps:
1. **Create GCP project**
2. **Enable Cloud Run API**
3. **Deploy using Cloud Build**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/ysense
   gcloud run deploy --image gcr.io/PROJECT_ID/ysense --platform managed
   ```

## 🔄 How Automatic Updates Work

### GitHub → Live Platform Flow:
```
1. You make changes locally
2. git add . && git commit -m "Update feature X"
3. git push origin main
4. Cloud service detects changes
5. Automatically builds and deploys
6. Live platform updates (usually 2-5 minutes)
```

### What Gets Updated Automatically:
- ✅ **Code changes** in `src/`, `api/`, `streamlit_v4_app.py`
- ✅ **Dependencies** in `requirements.txt`
- ✅ **Configuration** files
- ✅ **Database migrations** (if any)

### What Requires Manual Update:
- ❌ **Environment variables** (API keys, secrets)
- ❌ **Database data** (user data, wisdom drops)
- ❌ **File uploads** (if using local storage)

## 🛠️ Testing Your Setup

### 1. Test Local Changes
```bash
# Make a small change
echo "# Test Update" >> README.md
git add README.md
git commit -m "Test automatic deployment"
git push origin main
```

### 2. Monitor Deployment
- **Vercel**: Check dashboard for deployment status
- **Railway**: Check logs in dashboard
- **GCP**: Check Cloud Build logs

### 3. Verify Live Platform
- Visit your live URL
- Check if changes appear
- Test platform functionality

## 🔧 Configuration Files

### `vercel.json` (for Vercel)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "streamlit_v4_app.py", 
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "src/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "streamlit_v4_app.py"
    }
  ]
}
```

### `Procfile` (for Railway/Heroku)
```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
streamlit: streamlit run streamlit_v4_app.py --server.port $PORT
```

### `requirements.txt` (Dependencies)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
email-validator==2.1.0
python-dotenv==1.0.0
requests==2.31.0
```

## 🚨 Important Notes

### Security:
- **Never commit** `.env` files
- **Use environment variables** for API keys
- **Enable HTTPS** on your domain

### Database:
- **SQLite** works for development
- **PostgreSQL** recommended for production
- **Backup** your data regularly

### Monitoring:
- **Set up alerts** for deployment failures
- **Monitor** API usage and costs
- **Check logs** regularly

## 🎯 Quick Start (Vercel)

1. **Push these files to GitHub**:
   ```bash
   git add vercel.json Procfile requirements.txt AUTOMATIC_DEPLOYMENT_GUIDE.md
   git commit -m "Add automatic deployment configuration"
   git push origin main
   ```

2. **Go to Vercel** and import your repository

3. **Add environment variables** in Vercel dashboard

4. **Deploy** and get your live URL

5. **Test automatic updates** by making a small change and pushing

## ✅ Success Checklist

- [ ] Repository connected to deployment service
- [ ] Environment variables configured
- [ ] Initial deployment successful
- [ ] Live platform accessible
- [ ] Test update deployed automatically
- [ ] API keys working on live platform
- [ ] Custom domain configured (optional)

---

**Result**: Every time you push changes to the `main` branch, your live platform will automatically update within 2-5 minutes! 🚀
