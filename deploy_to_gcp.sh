# GCP Cloud Run Deployment Script
# =====================================================

#!/bin/bash

# YSense™ v4.1 GCP Cloud Run Deployment
# =====================================================

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="asia-southeast1"  # Singapore region
SERVICE_NAME_BACKEND="ysense-backend"
SERVICE_NAME_FRONTEND="ysense-frontend"
IMAGE_BACKEND="gcr.io/$PROJECT_ID/ysense-backend"
IMAGE_FRONTEND="gcr.io/$PROJECT_ID/ysense-frontend"

echo "🚀 Deploying YSense™ v4.1 to GCP Cloud Run"
echo "=========================================="

# 1. Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com

# 3. Build and deploy backend
echo "🏗️ Building backend image..."
gcloud builds submit --tag $IMAGE_BACKEND --file Dockerfile.backend .

echo "🚀 Deploying backend to Cloud Run..."
gcloud run deploy $SERVICE_NAME_BACKEND \
    --image $IMAGE_BACKEND \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --set-env-vars "ENVIRONMENT=production" \
    --set-secrets "QWEN_API_KEY=ysense-qwen-api-key:latest" \
    --set-secrets "ANTHROPIC_API_KEY=ysense-anthropic-api-key:latest" \
    --set-secrets "SECRET_KEY=ysense-secret-key:latest"

# 4. Build and deploy frontend
echo "🏗️ Building frontend image..."
gcloud builds submit --tag $IMAGE_FRONTEND --file Dockerfile.frontend .

echo "🚀 Deploying frontend to Cloud Run..."
gcloud run deploy $SERVICE_NAME_FRONTEND \
    --image $IMAGE_FRONTEND \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 5 \
    --set-env-vars "ENVIRONMENT=production" \
    --set-env-vars "BACKEND_URL=https://$SERVICE_NAME_BACKEND-$REGION-$PROJECT_ID.a.run.app"

# 5. Get service URLs
BACKEND_URL=$(gcloud run services describe $SERVICE_NAME_BACKEND --region=$REGION --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe $SERVICE_NAME_FRONTEND --region=$REGION --format="value(status.url)")

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo "API Docs: $BACKEND_URL/docs"
echo ""
echo "🌐 Your YSense™ v4.1 platform is now live!"
echo "Visit: $FRONTEND_URL"





