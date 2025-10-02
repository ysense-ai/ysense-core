# GCP Cloud Run Deployment Guide
# =====================================================

## 🚀 YSense™ v4.1 GCP Cloud Run Deployment Guide

### **📋 Prerequisites**

1. **✅ GCP Account** - With billing enabled
2. **✅ Google Cloud SDK** - Installed and configured
3. **✅ Docker** - For building container images
4. **✅ Domain** - Your custom domain (optional)

### **🔧 Step 1: GCP Project Setup**

```bash
# Create new GCP project
gcloud projects create ysense-platform-v41 --name="YSense Platform v4.1"

# Set project
gcloud config set project ysense-platform-v41

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### **🔧 Step 2: API Keys Setup**

```bash
# Store API keys in Secret Manager
gcloud secrets create ysense-qwen-api-key --data-file=- <<< "your_qwen_api_key"
gcloud secrets create ysense-anthropic-api-key --data-file=- <<< "your_anthropic_api_key"
gcloud secrets create ysense-secret-key --data-file=- <<< "your_jwt_secret_key"
```

### **🔧 Step 3: Database Setup (Optional)**

```bash
# Create Cloud SQL instance (for production)
gcloud sql instances create ysense-db \
    --database-version=POSTGRES_13 \
    --tier=db-f1-micro \
    --region=asia-southeast1

# Create database
gcloud sql databases create ysense --instance=ysense-db
```

### **🔧 Step 4: Deploy to Cloud Run**

```bash
# Make deployment script executable
chmod +x deploy_to_gcp.sh

# Run deployment
./deploy_to_gcp.sh
```

### **🌐 Step 5: Custom Domain Setup**

```bash
# Map custom domain to Cloud Run
gcloud run domain-mappings create \
    --service=ysense-frontend \
    --domain=ysense.ai \
    --region=asia-southeast1
```

### **📊 Step 6: Monitoring Setup**

```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com
```

### **💰 Cost Estimation**

**Cloud Run Pricing (Singapore region):**
- **Backend**: ~$5-15/month (2 CPU, 2GB RAM)
- **Frontend**: ~$2-8/month (1 CPU, 1GB RAM)
- **Database**: ~$10-25/month (Cloud SQL)
- **Storage**: ~$1-5/month (Cloud Storage)
- **Total**: ~$18-53/month

### **🔒 Security Features**

1. **✅ Secret Manager** - API keys stored securely
2. **✅ HTTPS Only** - Automatic SSL certificates
3. **✅ IAM Authentication** - Fine-grained access control
4. **✅ VPC Security** - Network isolation
5. **✅ Audit Logging** - Complete activity tracking

### **📈 Scaling Features**

1. **✅ Auto-scaling** - 0 to 1000 instances
2. **✅ Load Balancing** - Automatic traffic distribution
3. **✅ CDN Integration** - Global content delivery
4. **✅ Health Checks** - Automatic failover

### **🎯 Production Checklist**

- [ ] GCP project created with billing
- [ ] API keys stored in Secret Manager
- [ ] Docker images built and pushed
- [ ] Cloud Run services deployed
- [ ] Custom domain configured
- [ ] SSL certificates active
- [ ] Monitoring enabled
- [ ] Backup strategy implemented

### **🚀 Quick Deploy Command**

```bash
# One-command deployment
gcloud run deploy ysense-platform --source . --region asia-southeast1 --allow-unauthenticated
```

### **📞 Support**

- **GCP Console**: https://console.cloud.google.com
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **YSense Support**: support@ysense.ai

---

**🎉 Your YSense™ v4.1 platform will be live at:**
**https://ysense-frontend-[region]-[project-id].a.run.app**





