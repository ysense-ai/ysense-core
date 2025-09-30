# GCP DEPLOYMENT GUIDE - YSense™ v4.1 Fresh 🚀

## 🎯 **Deployment Overview**

This guide will deploy your YSense™ Platform v4.1 Fresh to Google Cloud Platform using Cloud Run for a serverless, scalable deployment.

## 📋 **Prerequisites**

### **✅ Required:**
- **Google Cloud Account** with billing enabled
- **Google Cloud SDK** installed (`gcloud` command)
- **Docker** installed (for local testing)
- **API Keys** for QWEN and Anthropic

### **✅ Recommended:**
- **Custom Domain** (optional)
- **Cloud SQL** for production database (optional)

## 🔧 **Step 1: GCP Project Setup**

### **1.1 Create GCP Project:**
```bash
# Create new project
gcloud projects create ysense-platform-v41 --name="YSense Platform v4.1"

# Set as active project
gcloud config set project ysense-platform-v41

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### **1.2 Enable Required APIs:**
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable sqladmin.googleapis.com
```

## 🔐 **Step 2: Secrets Management**

### **2.1 Create API Key Secrets:**
```bash
# Create QWEN API key secret
echo "your_qwen_api_key_here" | gcloud secrets create ysense-qwen-api-key --data-file=-

# Create Anthropic API key secret
echo "your_anthropic_api_key_here" | gcloud secrets create ysense-anthropic-api-key --data-file=-

# Create secret key for app
echo "your_secret_key_here" | gcloud secrets create ysense-secret-key --data-file=-
```

### **2.2 Grant Cloud Run Access:**
```bash
# Get Cloud Run service account
SERVICE_ACCOUNT=$(gcloud projects describe ysense-platform-v41 --format="value(projectNumber)")-compute@developer.gserviceaccount.com

# Grant secret access
gcloud secrets add-iam-policy-binding ysense-qwen-api-key \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding ysense-anthropic-api-key \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding ysense-secret-key \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
```

## 🏗️ **Step 3: Build and Deploy**

### **3.1 Build Docker Image:**
```bash
# Navigate to your project directory
cd "YSense-Platform-v4.1-Fresh"

# Build image
gcloud builds submit --tag gcr.io/ysense-platform-v41/ysense-v41-fresh --file Dockerfile.v41 .
```

### **3.2 Deploy to Cloud Run:**
```bash
gcloud run deploy ysense-v41-fresh \
    --image gcr.io/ysense-platform-v41/ysense-v41-fresh \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --min-instances 1 \
    --set-env-vars "ENVIRONMENT=production" \
    --set-secrets "QWEN_API_KEY=ysense-qwen-api-key:latest" \
    --set-secrets "ANTHROPIC_API_KEY=ysense-anthropic-api-key:latest" \
    --set-secrets "SECRET_KEY=ysense-secret-key:latest"
```

## 🌐 **Step 4: Get Your Live URL**

### **4.1 Get Deployment URL:**
```bash
# Get service URL
gcloud run services describe ysense-v41-fresh \
    --region=asia-southeast1 \
    --format="value(status.url)"
```

### **4.2 Expected Output:**
```
https://ysense-v41-fresh-[hash]-uc.a.run.app
```

## 🎉 **Step 5: Test Your Live Platform**

### **5.1 Access Your Platform:**
1. **Open the URL** in your browser
2. **Test registration** with crypto key authentication
3. **Submit a story** and test AI analysis
4. **Check revenue dashboard** functionality
5. **Verify white paper** viewing and download

### **5.2 Monitor Performance:**
```bash
# View logs
gcloud logs read --service=ysense-v41-fresh --limit=50

# Check service status
gcloud run services describe ysense-v41-fresh --region=asia-southeast1
```

## 🔧 **Step 6: Production Optimizations**

### **6.1 Custom Domain (Optional):**
```bash
# Map custom domain
gcloud run domain-mappings create \
    --service ysense-v41-fresh \
    --domain ysenseai.org \
    --region asia-southeast1
```

### **6.2 Cloud SQL Database (Optional):**
```bash
# Create Cloud SQL instance
gcloud sql instances create ysense-db \
    --database-version=POSTGRES_13 \
    --tier=db-f1-micro \
    --region=asia-southeast1

# Create database
gcloud sql databases create ysense_production --instance=ysense-db
```

### **6.3 Monitoring Setup:**
```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com

# Create alerting policy
gcloud alpha monitoring policies create --policy-from-file=alert-policy.yaml
```

## 📊 **Deployment Architecture**

### **✅ Cloud Run Benefits:**
- **Serverless**: No server management
- **Auto-scaling**: Scales based on traffic
- **Pay-per-use**: Only pay for actual usage
- **Global CDN**: Fast access worldwide
- **HTTPS**: Automatic SSL certificates

### **✅ Security Features:**
- **Secret Manager**: Secure API key storage
- **IAM**: Fine-grained access control
- **VPC**: Network isolation
- **Audit Logs**: Complete activity tracking

## 🚀 **Quick Deployment Commands**

### **✅ One-Command Deployment:**
```bash
# Make script executable
chmod +x deploy_to_gcp_v41.sh

# Run deployment
./deploy_to_gcp_v41.sh
```

### **✅ Manual Step-by-Step:**
```bash
# 1. Set project
gcloud config set project ysense-platform-v41

# 2. Build and deploy
gcloud builds submit --tag gcr.io/ysense-platform-v41/ysense-v41-fresh --file Dockerfile.v41 .

gcloud run deploy ysense-v41-fresh \
    --image gcr.io/ysense-platform-v41/ysense-v41-fresh \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --set-secrets "QWEN_API_KEY=ysense-qwen-api-key:latest" \
    --set-secrets "ANTHROPIC_API_KEY=ysense-anthropic-api-key:latest" \
    --set-secrets "SECRET_KEY=ysense-secret-key:latest"
```

## 📋 **Post-Deployment Checklist**

### **✅ Functionality Tests:**
- [ ] **Platform loads** without errors
- [ ] **Registration works** with crypto keys
- [ ] **Story submission** saves to database
- [ ] **AI analysis** completes successfully
- [ ] **Revenue dashboard** displays correctly
- [ ] **White paper** viewing works
- [ ] **All navigation** links functional

### **✅ Performance Tests:**
- [ ] **Page load times** under 3 seconds
- [ ] **AI analysis** completes in reasonable time
- [ ] **Database operations** work smoothly
- [ ] **Concurrent users** handled properly

### **✅ Security Tests:**
- [ ] **HTTPS** enabled and working
- [ ] **API keys** properly secured
- [ ] **User data** protected
- [ ] **Database** access restricted

## 🎯 **Expected Results**

### **✅ Live Platform Features:**
- **🌐 Public Access**: Available worldwide via HTTPS
- **🔐 Secure Authentication**: Crypto key-based login
- **🤖 AI Analysis**: Real QWEN and Anthropic integration
- **💰 Revenue Tracking**: Transparent attribution system
- **📊 Analytics**: User metrics and platform statistics
- **📄 White Paper**: Public access for credibility

### **✅ Performance Metrics:**
- **⚡ Fast Loading**: Cloud Run + CDN
- **📈 Auto-scaling**: Handles traffic spikes
- **🔄 High Availability**: 99.9% uptime
- **💾 Persistent Storage**: Database survives restarts

## 🎉 **Success!**

**Your YSense™ Platform v4.1 Fresh is now live on Google Cloud Platform!**

### **🌐 Access Your Platform:**
```
https://ysense-v41-fresh-[hash]-uc.a.run.app
```

### **📊 Monitor Your Platform:**
- **Cloud Console**: https://console.cloud.google.com/run
- **Logs**: https://console.cloud.google.com/logs
- **Monitoring**: https://console.cloud.google.com/monitoring

### **🔧 Manage Your Platform:**
- **Update Code**: Re-run deployment script
- **Scale Resources**: Adjust memory/CPU in Cloud Console
- **Monitor Costs**: Check billing dashboard
- **Add Features**: Deploy new versions seamlessly

**Congratulations! Your YSense™ Platform v4.1 Fresh is now live and ready for the world!** 🎉

