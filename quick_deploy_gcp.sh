#!/bin/bash
# YSense™ v4.1 Fresh - Quick GCP Deployment
# ==========================================

echo "🚀 YSense™ v4.1 Fresh - GCP Deployment"
echo "======================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found!"
    echo "Please install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please log in to Google Cloud:"
    gcloud auth login
fi

# Set project (you'll need to update this)
PROJECT_ID="ysense-platform-v41"
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Create secrets (you'll need to update these with your actual keys)
echo "🔐 Creating secrets..."
echo "your_qwen_api_key_here" | gcloud secrets create ysense-qwen-api-key --data-file=- 2>/dev/null || echo "Secret already exists"
echo "your_anthropic_api_key_here" | gcloud secrets create ysense-anthropic-api-key --data-file=- 2>/dev/null || echo "Secret already exists"
echo "your_secret_key_here" | gcloud secrets create ysense-secret-key --data-file=- 2>/dev/null || echo "Secret already exists"

# Build and deploy
echo "🏗️ Building and deploying..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/ysense-v41-fresh --file Dockerfile.v41 .

gcloud run deploy ysense-v41-fresh \
    --image gcr.io/$PROJECT_ID/ysense-v41-fresh \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --port 8501 \
    --memory 2Gi \
    --cpu 2 \
    --set-env-vars "ENVIRONMENT=production" \
    --set-secrets "QWEN_API_KEY=ysense-qwen-api-key:latest" \
    --set-secrets "ANTHROPIC_API_KEY=ysense-anthropic-api-key:latest" \
    --set-secrets "SECRET_KEY=ysense-secret-key:latest"

# Get URL
SERVICE_URL=$(gcloud run services describe ysense-v41-fresh --region=asia-southeast1 --format="value(status.url)")

echo "======================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "🌐 Your platform is live at:"
echo "   $SERVICE_URL"
echo "======================================="
echo ""
echo "📋 Next steps:"
echo "1. Update secrets with your real API keys"
echo "2. Test your platform functionality"
echo "3. Set up custom domain (optional)"
echo ""
echo "🔗 Access your platform: $SERVICE_URL"

