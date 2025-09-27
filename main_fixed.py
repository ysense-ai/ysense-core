"""
YSense Platform v3.0 - Main API
Fixed import paths for proper module resolution
"""

import sys
import os
from pathlib import Path

# Fix Python path to find api folder
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Now these imports will work
from api import auth, wisdom, revenue, legal
from src.models import User, ConsentRecord, AuditLog
from src.orchestrator import YSenseOrchestrator
from src.qwen_integration import QwenIntegration
from src.z_protocol_enhanced import ZProtocolEnhanced

# Load environment
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="YSense Platform v3.0",
    description="AI Attribution Infrastructure - Protected by DOI: 10.5281/zenodo.17072168",
    version="3.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from api modules
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(wisdom.router, prefix="/api/wisdom", tags=["Wisdom"])
app.include_router(revenue.router, prefix="/api/revenue", tags=["Revenue"])
app.include_router(legal.router, prefix="/api/legal", tags=["Legal"])

@app.get("/")
async def root():
    return {
        "platform": "YSense™ v3.0",
        "status": "operational",
        "doi": "10.5281/zenodo.17072168",
        "founder": "Alton Lee Wei Bin",
        "location": "Teluk Intan, Malaysia"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "3.0"}

@app.get("/api/z-protocol")
async def z_protocol_info():
    return {
        "version": "2.0",
        "features": ["consent management", "attribution tracking", "revenue distribution"],
        "status": "active"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
