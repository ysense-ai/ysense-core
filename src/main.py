# main.py
"""
YSense Platform v4.1 - Complete AI-Enhanced Platform
Integrates Layer Analyzer, Intelligent Agents, and Orchestrator
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Import core components
from models import create_tables
from config import Config

# Import v4.1 AI components (with error handling)
try:
    from orchestrator import YSenseOrchestrator
    orchestrator = YSenseOrchestrator()
    ORCHESTRATOR_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Orchestrator not available: {e}")
    orchestrator = None
    ORCHESTRATOR_AVAILABLE = False

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    try:
        create_tables()
        print("🚀 YSense v4.1 Platform Starting...")
        print("✨ AI Components: Layer Analyzer, Intelligent Agents, Orchestrator")
        print(f"🔧 Environment: {Config.ENVIRONMENT}")
        print(f"🗄️  Database: {Config.DATABASE_URL}")

        # Start background scheduler for orchestrator if available
        if ORCHESTRATOR_AVAILABLE and orchestrator:
            scheduler.add_job(
                orchestrator.execute_daily_workflow,
                'interval',
                hours=24,
                id='daily_workflow',
                name='Daily Agent Workflow'
            )
            scheduler.start()
            print("⚙️ Orchestrator scheduler started")
        else:
            print("⚠️  Orchestrator scheduler skipped (not available)")

        print("✅ YSense v4.1 Platform Started Successfully!")

    except Exception as e:
        print(f"❌ Error during startup: {e}")

    yield

    # Shutdown
    if ORCHESTRATOR_AVAILABLE:
        scheduler.shutdown()
    print("🛑 YSense v4.1 Platform Shutting Down...")

app = FastAPI(
    title="YSense™ Platform v4.1",
    description="AI Attribution Infrastructure - Human-AI Collaboration Platform",
    version="4.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if Config.CORS_ALLOW_ALL else Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: API routers are currently not implemented
# These will be added in future updates
# For now, the platform uses direct integration via Streamlit frontend

@app.get("/")
async def root():
    """Root endpoint - Platform information"""
    return {
        "platform": "YSense™ | 慧觉™",
        "version": "4.1.0",
        "status": "operational",
        "description": "AI Attribution Infrastructure",
        "features": {
            "core": ["Five-Layer Perception", "Deep Vibe Distillation", "Z Protocol v2.0"],
            "ai_enhanced": ["6 Intelligent Agents", "Dual AI Models", "3-Stage Methodology"],
            "compliance": ["Malaysia PDPA", "Singapore PDPA", "GDPR", "Z Protocol"],
            "security": ["Crypto Authentication", "No Password", "JWT Tokens"]
        },
        "doi": "10.5281/zenodo.17072168",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from models import get_session
        session = get_session()
        session.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "version": "4.1.0",
        "environment": Config.ENVIRONMENT,
        "components": {
            "database": db_status,
            "ai_services": "ready" if Config.QWEN_API_KEY and Config.ANTHROPIC_API_KEY else "fallback_mode",
            "orchestrator": "active" if ORCHESTRATOR_AVAILABLE else "unavailable",
            "crypto_auth": "enabled",
            "z_protocol": "v2.0"
        },
        "api_keys_configured": {
            "qwen": bool(Config.QWEN_API_KEY and not Config.QWEN_API_KEY.startswith("your-")),
            "anthropic": bool(Config.ANTHROPIC_API_KEY and not Config.ANTHROPIC_API_KEY.startswith("your-"))
        }
    }

@app.get("/api/v4/status")
async def detailed_status():
    """Detailed platform status"""
    return {
        "platform": "YSense™ v4.1",
        "status": "operational",
        "features_enabled": {
            "z_protocol": Config.ENABLE_Z_PROTOCOL,
            "dual_model": Config.ENABLE_DUAL_MODEL,
            "agent_orchestration": ORCHESTRATOR_AVAILABLE,
            "mcp_server": Config.ENABLE_MCP_SERVER
        },
        "database": {
            "type": "PostgreSQL" if Config.USE_POSTGRESQL else "SQLite",
            "url_prefix": Config.DATABASE_URL[:30] + "..."
        },
        "revenue_tiers": list(Config.Z_PROTOCOL_TIERS.keys())
    }

@app.post("/api/v4/orchestrator/trigger")
async def trigger_orchestrator(background_tasks: BackgroundTasks):
    """Manually trigger orchestrator workflow"""
    if not ORCHESTRATOR_AVAILABLE:
        raise HTTPException(status_code=503, detail="Orchestrator not available")

    background_tasks.add_task(orchestrator.execute_daily_workflow)
    return {
        "message": "Orchestrator workflow triggered",
        "status": "processing",
        "workflow_id": f"manual_{int(asyncio.get_event_loop().time())}"
    }
