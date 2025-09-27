"""
YSense Platform v3.0 - Full Featured Main
Integrates ALL designed components
"""

import sys
import os
from pathlib import Path

# Fix paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Import ALL your designed modules
from api import auth, wisdom, revenue, legal
from src.models import init_db, User, ConsentRecord
from src.orchestrator import YSenseOrchestrator
from src.qwen_integration import QwenIntegration  
from src.intelligent_agents import IntelligentAgents
from src.z_protocol_enhanced import ZProtocolEnhanced
from src.five_prompt_toolkit import FivePromptToolkit
from src.layer_analyzer import LayerAnalyzer

# Load environment
load_dotenv()

# Initialize components
orchestrator = YSenseOrchestrator()
qwen = QwenIntegration()
agents = IntelligentAgents()
z_protocol = ZProtocolEnhanced()
toolkit = FivePromptToolkit()
analyzer = LayerAnalyzer()

# Create FastAPI app with full features
app = FastAPI(
    title="YSense Platform v3.0 - Complete",
    description="Full AI Attribution Infrastructure with all modules",
    version="3.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ALL routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(wisdom.router, prefix="/api/wisdom", tags=["Wisdom"])
app.include_router(revenue.router, prefix="/api/revenue", tags=["Revenue"])
app.include_router(legal.router, prefix="/api/legal", tags=["Legal"])

# Scheduler for background tasks
scheduler = AsyncIOScheduler()
scheduler.start()

@app.on_event("startup")
async def startup():
    """Initialize all systems on startup"""
    init_db()  # Initialize database
    await orchestrator.initialize()
    await z_protocol.initialize()
    print("YSense Platform v3.0 - All systems initialized")

@app.get("/")
async def root():
    return {
        "platform": "YSense™ v3.0 Complete",
        "modules": {
            "orchestrator": "Active",
            "qwen_integration": "Active",
            "intelligent_agents": "Active",
            "z_protocol": "v2.0",
            "five_layer_toolkit": "Active",
            "layer_analyzer": "Active"
        },
        "doi": "10.5281/zenodo.17072168"
    }

@app.get("/api/orchestrate")
async def orchestrate(query: str):
    """Use full orchestration system"""
    result = await orchestrator.process(query)
    return result

@app.get("/api/analyze")
async def analyze(content: str):
    """Use five-layer perception toolkit"""
    analysis = toolkit.analyze(content)
    layers = analyzer.process(analysis)
    return {"analysis": analysis, "layers": layers}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
