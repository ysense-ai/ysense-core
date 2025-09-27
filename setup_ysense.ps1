# YSense Platform v3.0 - Quick Setup Script
# Run this script to quickly set up your development environment

Write-Host "🚀 YSense Platform v3.0 - Quick Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "src\main.py")) {
    Write-Host "❌ Error: Please run this script from the YSense Platform root directory" -ForegroundColor Red
    Write-Host "   Expected files: src\main.py, streamlit_app.py, requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found YSense Platform files" -ForegroundColor Green

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check for .env file
if (Test-Path ".env") {
    Write-Host "✅ Environment file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Creating .env template..." -ForegroundColor Yellow
    @"
# YSense Platform v3.0 Environment Configuration
# Copy this file and add your actual API keys

# API Keys (Required for full functionality)
QWEN_API_KEY=your_qwen_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security Keys (Auto-generated if not provided)
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Database (SQLite for development)
DATABASE_URL=sqlite:///ysense_local.db

# Platform Settings
PLATFORM_VERSION=3.0
ENVIRONMENT=development
DEBUG=true

# Revenue Settings
BASE_RATE_EUR=50.0
PLATFORM_FEE_PERCENTAGE=15
COMMUNITY_SHARE_PERCENTAGE=15

# Z Protocol
Z_PROTOCOL_VERSION=2.0
ENABLE_Z_PROTOCOL=true

# Defensive Publication
DEFENSIVE_PUBLICATION_DOI=10.5281/zenodo.17072168
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env template created. Please add your API keys!" -ForegroundColor Green
}

# Check database
if (Test-Path "ysense_local.db") {
    Write-Host "✅ Database found" -ForegroundColor Green
} else {
    Write-Host "🔄 Initializing database..." -ForegroundColor Yellow
    python -c "from src.models import init_database; init_database()"
    Write-Host "✅ Database initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your API keys to .env file" -ForegroundColor White
Write-Host "2. Start the backend: python -m uvicorn src.main:app --reload --port 8000" -ForegroundColor White
Write-Host "3. Start the frontend: streamlit run streamlit_app.py --server.port 8501" -ForegroundColor White
Write-Host "4. Access the platform:" -ForegroundColor White
Write-Host "   - API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   - UI: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation: PROJECT_BACKUP_GUIDE.md" -ForegroundColor Yellow
Write-Host "🛡️  Protection: DOI 10.5281/zenodo.17072168" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ready to continue building YSense! 💧" -ForegroundColor Cyan



