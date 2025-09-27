# main.py
"""
YSense Platform v3.0 - Complete AI-Enhanced Platform
Integrates Layer Analyzer, Intelligent Agents, and Orchestrator
"""

import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Import core components
from api import auth, wisdom, wisdom_v4, revenue, legal, key_recovery
from core import mcp_integration
from src.models import create_tables

# Import v3.0 AI components
from src.orchestrator import YSenseOrchestrator

# Initialize orchestrator
orchestrator = YSenseOrchestrator()
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    create_tables()
    print("🚀 YSense v3.0 Platform Starting...")
    print("✨ AI Components: Layer Analyzer, Intelligent Agents, Orchestrator")
    
    # Start background scheduler for orchestrator
    scheduler.add_job(
        orchestrator.execute_daily_workflow,
        'interval',
        hours=24,
        id='daily_workflow',
        name='Daily Agent Workflow'
    )
    scheduler.start()
    print("⚙️ Orchestrator scheduler started")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("YSense v3.0 Platform Shutting Down...")

app = FastAPI(
    title="YSense™ Platform v3.0",
    description="AI-Enhanced Human Wisdom Library with Intelligent Agents",
    version="3.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],  # Streamlit v3.0 and v4.0
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v3/auth", tags=["Authentication"])
app.include_router(wisdom.router, prefix="/api/v3/wisdom", tags=["Wisdom"])
app.include_router(wisdom_v4.router, prefix="/api/v4/wisdom", tags=["Wisdom v4.0"])
app.include_router(revenue.router, prefix="/api/v3/revenue", tags=["Revenue"])
app.include_router(legal.router, prefix="/api/v3/legal", tags=["Legal"])
app.include_router(key_recovery.router, prefix="/api/v4/recovery", tags=["Key Recovery"])

@app.get("/")
async def root():
    return {
        "platform": "YSense™ | 慧觉™",
        "version": "3.0.0",
        "status": "operational",
        "features": {
            "core": ["Five-Layer Perception", "Deep Vibe Distillation", "Z Protocol"],
            "ai_enhanced": ["Layer Analyzer", "Intelligent Agents", "Orchestrator"],
            "compliance": ["Malaysia PDPA", "Singapore PDPA", "GDPR"]
        },
        "doi": "10.5281/zenodo.17072168"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "components": {
            "database": "connected",
            "ai_services": "operational",
            "orchestrator": "active"
        }
    }

@app.post("/api/v3/orchestrator/trigger")
async def trigger_orchestrator(background_tasks: BackgroundTasks):
    """Manually trigger orchestrator workflow"""
    background_tasks.add_task(orchestrator.execute_daily_workflow)
    return {"message": "Orchestrator workflow triggered", "status": "processing"}
