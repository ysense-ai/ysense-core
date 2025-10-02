@echo off
REM YSense™ v4.1-Fresh GCP Deployment Script (Windows)
REM =================================================
REM This script creates a new GCP project and deploys YSense v4.1-Fresh to Cloud Run

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_ID=ysense-platform-v41
set REGION=asia-southeast1
set SERVICE_NAME=ysense-v41-fresh
set PORT=8501
set MEMORY=2Gi
set MIN_INSTANCES=1
set MAX_INSTANCES=10

echo 🚀 Starting YSense™ v4.1-Fresh GCP Deployment
echo ==============================================

REM Step 1: Create GCP Project
echo 📋 Step 1: Creating GCP Project...
gcloud projects describe %PROJECT_ID% >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Project %PROJECT_ID% already exists
) else (
    echo 🆕 Creating new project: %PROJECT_ID%
    gcloud projects create %PROJECT_ID% --name="YSense Platform v4.1 Fresh"
    echo ✅ Project created successfully
)

REM Set the project
gcloud config set project %PROJECT_ID%
echo ✅ Project set to: %PROJECT_ID%

REM Step 2: Enable Required APIs
echo.
echo 📋 Step 2: Enabling Required APIs...

echo 🔧 Enabling Cloud Run API...
gcloud services enable run.googleapis.com

echo 🔧 Enabling Cloud Build API...
gcloud services enable cloudbuild.googleapis.com

echo 🔧 Enabling Secret Manager API...
gcloud services enable secretmanager.googleapis.com

echo 🔧 Enabling Container API...
gcloud services enable container.googleapis.com

echo 🔧 Enabling Artifact Registry API...
gcloud services enable artifactregistry.googleapis.com

echo ✅ All APIs enabled successfully

REM Step 3: Configure Authentication
echo.
echo 📋 Step 3: Configuring Authentication...

REM Check if user is authenticated
gcloud auth list --filter=status:ACTIVE --format="value(account)" | findstr /R "." >nul
if %errorlevel% neq 0 (
    echo 🔐 Please authenticate with Google Cloud...
    gcloud auth login
)

REM Configure Docker authentication
gcloud auth configure-docker
echo ✅ Authentication configured

REM Step 4: Create Artifact Registry Repository
echo.
echo 📋 Step 4: Setting up Artifact Registry...

set REPO_NAME=ysense-v41
set REPO_LOCATION=asia-southeast1

gcloud artifacts repositories describe %REPO_NAME% --location=%REPO_LOCATION% >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Artifact Registry repository already exists
) else (
    echo 🆕 Creating Artifact Registry repository...
    gcloud artifacts repositories create %REPO_NAME% --repository-format=docker --location=%REPO_LOCATION% --description="YSense v4.1 Fresh Docker images"
    echo ✅ Artifact Registry repository created
)

REM Update image name to use Artifact Registry
set IMAGE_NAME=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/ysense-v41-fresh

REM Step 5: Build Docker Image
echo.
echo 📋 Step 5: Building Docker Image...

echo 🔨 Building Docker image: %IMAGE_NAME%
gcloud builds submit --tag %IMAGE_NAME% .

echo ✅ Docker image built successfully

REM Step 6: Deploy to Cloud Run
echo.
echo 📋 Step 6: Deploying to Cloud Run...

echo 🚀 Deploying service: %SERVICE_NAME%

gcloud run deploy %SERVICE_NAME% ^
    --image=%IMAGE_NAME% ^
    --platform=managed ^
    --region=%REGION% ^
    --port=%PORT% ^
    --memory=%MEMORY% ^
    --min-instances=%MIN_INSTANCES% ^
    --max-instances=%MAX_INSTANCES% ^
    --allow-unauthenticated ^
    --set-env-vars="PYTHONPATH=/app" ^
    --set-env-vars="STREAMLIT_SERVER_PORT=8501" ^
    --set-env-vars="STREAMLIT_SERVER_ADDRESS=0.0.0.0" ^
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true" ^
    --set-env-vars="STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"

echo ✅ Cloud Run service deployed successfully

REM Step 7: Get Service URL
echo.
echo 📋 Step 7: Getting Service Information...

for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo 🎉 DEPLOYMENT COMPLETE!
echo ======================
echo 🌐 Live URL: %SERVICE_URL%
echo 📊 Service: %SERVICE_NAME%
echo 🌍 Region: %REGION%
echo 💾 Memory: %MEMORY%
echo 🔢 Instances: %MIN_INSTANCES%-%MAX_INSTANCES%
echo 🔓 Access: Public (unauthenticated)

echo.
echo 🚀 Your YSense™ v4.1-Fresh platform is now live!
echo 📱 Open the URL in your browser to access the platform.

REM Step 8: Display Service Details
echo.
echo 📋 Service Details:
gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="table(metadata.name,status.url,spec.template.spec.containers[0].image,status.conditions[0].status)"

echo.
echo ✅ Deployment script completed successfully!
echo 🌐 Live URL: %SERVICE_URL%

pause
