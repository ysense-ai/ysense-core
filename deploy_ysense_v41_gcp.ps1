# YSense™ v4.1-Fresh GCP Deployment Script (PowerShell)
# =====================================================
# This script creates a new GCP project and deploys YSense v4.1-Fresh to Cloud Run

# Configuration
$PROJECT_ID = "ysense-platform-v41"
$REGION = "asia-southeast1"
$SERVICE_NAME = "ysense-v41-fresh"
$PORT = "8501"
$MEMORY = "2Gi"
$MIN_INSTANCES = "1"
$MAX_INSTANCES = "10"

Write-Host "🚀 Starting YSense™ v4.1-Fresh GCP Deployment" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green

# Step 1: Create GCP Project
Write-Host "📋 Step 1: Creating GCP Project..." -ForegroundColor Yellow

try {
    gcloud projects describe $PROJECT_ID 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Project $PROJECT_ID already exists" -ForegroundColor Green
    }
} catch {
    Write-Host "🆕 Creating new project: $PROJECT_ID" -ForegroundColor Cyan
    gcloud projects create $PROJECT_ID --name="YSense Platform v4.1 Fresh"
    Write-Host "✅ Project created successfully" -ForegroundColor Green
}

# Set the project
gcloud config set project $PROJECT_ID
Write-Host "✅ Project set to: $PROJECT_ID" -ForegroundColor Green

# Step 2: Enable Required APIs
Write-Host ""
Write-Host "📋 Step 2: Enabling Required APIs..." -ForegroundColor Yellow

$APIS = @(
    "run.googleapis.com",
    "cloudbuild.googleapis.com", 
    "secretmanager.googleapis.com",
    "container.googleapis.com",
    "artifactregistry.googleapis.com"
)

foreach ($api in $APIS) {
    Write-Host "🔧 Enabling $api..." -ForegroundColor Cyan
    gcloud services enable $api
}

Write-Host "✅ All APIs enabled successfully" -ForegroundColor Green

# Step 3: Configure Authentication
Write-Host ""
Write-Host "📋 Step 3: Configuring Authentication..." -ForegroundColor Yellow

# Check if user is authenticated
$authCheck = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
if (-not $authCheck) {
    Write-Host "🔐 Please authenticate with Google Cloud..." -ForegroundColor Red
    gcloud auth login
}

# Configure Docker authentication
gcloud auth configure-docker
Write-Host "✅ Authentication configured" -ForegroundColor Green

# Step 4: Create Artifact Registry Repository
Write-Host ""
Write-Host "📋 Step 4: Setting up Artifact Registry..." -ForegroundColor Yellow

$REPO_NAME = "ysense-v41"
$REPO_LOCATION = "asia-southeast1"

try {
    gcloud artifacts repositories describe $REPO_NAME --location=$REPO_LOCATION 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Artifact Registry repository already exists" -ForegroundColor Green
    }
} catch {
    Write-Host "🆕 Creating Artifact Registry repository..." -ForegroundColor Cyan
    gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REPO_LOCATION --description="YSense v4.1 Fresh Docker images"
    Write-Host "✅ Artifact Registry repository created" -ForegroundColor Green
}

# Update image name to use Artifact Registry
$IMAGE_NAME = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/ysense-v41-fresh"

# Step 5: Build Docker Image
Write-Host ""
Write-Host "📋 Step 5: Building Docker Image..." -ForegroundColor Yellow

Write-Host "🔨 Building Docker image: $IMAGE_NAME" -ForegroundColor Cyan
gcloud builds submit --tag $IMAGE_NAME .

Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Step 6: Deploy to Cloud Run
Write-Host ""
Write-Host "📋 Step 6: Deploying to Cloud Run..." -ForegroundColor Yellow

Write-Host "🚀 Deploying service: $SERVICE_NAME" -ForegroundColor Cyan

gcloud run deploy $SERVICE_NAME `
    --image=$IMAGE_NAME `
    --platform=managed `
    --region=$REGION `
    --port=$PORT `
    --memory=$MEMORY `
    --min-instances=$MIN_INSTANCES `
    --max-instances=$MAX_INSTANCES `
    --allow-unauthenticated `
    --set-env-vars="PYTHONPATH=/app" `
    --set-env-vars="STREAMLIT_SERVER_PORT=8501" `
    --set-env-vars="STREAMLIT_SERVER_ADDRESS=0.0.0.0" `
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true" `
    --set-env-vars="STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"

Write-Host "✅ Cloud Run service deployed successfully" -ForegroundColor Green

# Step 7: Get Service URL
Write-Host ""
Write-Host "📋 Step 7: Getting Service Information..." -ForegroundColor Yellow

$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host "🌐 Live URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host "📊 Service: $SERVICE_NAME" -ForegroundColor White
Write-Host "🌍 Region: $REGION" -ForegroundColor White
Write-Host "💾 Memory: $MEMORY" -ForegroundColor White
Write-Host "🔢 Instances: $MIN_INSTANCES-$MAX_INSTANCES" -ForegroundColor White
Write-Host "🔓 Access: Public (unauthenticated)" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Your YSense™ v4.1-Fresh platform is now live!" -ForegroundColor Green
Write-Host "📱 Open the URL in your browser to access the platform." -ForegroundColor Yellow

# Step 8: Display Service Details
Write-Host ""
Write-Host "📋 Service Details:" -ForegroundColor Yellow
gcloud run services describe $SERVICE_NAME --region=$REGION --format="table(metadata.name,status.url,spec.template.spec.containers[0].image,status.conditions[0].status)"

Write-Host ""
Write-Host "✅ Deployment script completed successfully!" -ForegroundColor Green
Write-Host "🌐 Live URL: $SERVICE_URL" -ForegroundColor Cyan

Read-Host "Press Enter to continue"
