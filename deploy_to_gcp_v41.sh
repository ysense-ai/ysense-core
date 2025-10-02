# GCP Cloud Run Deployment Script - YSense™ v4.1 Fresh
# =====================================================

#!/bin/bash

# YSense™ v4.1 Fresh GCP Cloud Run Deployment
# =====================================================

set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="ysense-platform-v4-1"  # Your GCP Project ID
REGION="asia-southeast1"           # Singapore region (closest to you)
SERVICE_NAME="ysense-v41-fresh"    # Cloud Run service name
IMAGE_NAME="gcr.io/$PROJECT_ID/ysense-v41-fresh"

echo "🚀 Deploying YSense™ v4.1 Fresh to GCP Cloud Run"
echo "=================================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo "=================================================="

# 1. Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com

# 3. Create secrets in Secret Manager
echo "🔐 Setting up secrets..."
echo "QWEN_API_KEY=your_qwen_api_key_here" | gcloud secrets create ysense-qwen-api-key --data-file=-
echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" | gcloud secrets create ysense-anthropic-api-key --data-file=-
echo "SECRET_KEY=your_secret_key_here" | gcloud secrets create ysense-secret-key --data-file=-

# 4. Build and deploy Streamlit app
echo "🏗️ Building YSense™ v4.1 Fresh image..."
gcloud builds submit --tag $IMAGE_NAME --file Dockerfile.v41 .

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
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

# 5. Get deployment URL
echo "🌐 Getting deployment URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "=================================================="
echo "🎉 YSense™ v4.1 Fresh deployed successfully!"
echo "🌐 URL: $SERVICE_URL"
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo "1. Update your .env file with production API keys"
echo "2. Test the deployed platform"
echo "3. Set up custom domain (optional)"
echo "4. Configure monitoring and alerts"
echo ""
echo "🔗 Access your platform at: $SERVICE_URL"



