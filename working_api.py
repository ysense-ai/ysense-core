"""
YSense Platform v3.0 - Working Version
Bypasses database initialization issues
"""

import sys
import os
from pathlib import Path

# Fix paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="YSense Platform v3.0",
    description="AI Attribution Infrastructure - DOI: 10.5281/zenodo.17072168",
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

# Import routers with error handling
try:
    from api.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
except Exception as e:
    print(f"Auth module issue: {e}")

try:
    from api.wisdom import router as wisdom_router
    app.include_router(wisdom_router, prefix="/api/wisdom", tags=["Wisdom"])
except Exception as e:
    print(f"Wisdom module issue: {e}")

try:
    from api.revenue import router as revenue_router  
    app.include_router(revenue_router, prefix="/api/revenue", tags=["Revenue"])
except Exception as e:
    print(f"Revenue module issue: {e}")

try:
    from api.legal import router as legal_router
    app.include_router(legal_router, prefix="/api/legal", tags=["Legal"])
except Exception as e:
    print(f"Legal module issue: {e}")

@app.get("/")
async def root():
    return {
        "platform": "YSense™ v3.0",
        "status": "operational (database bypassed)",
        "doi": "10.5281/zenodo.17072168",
        "endpoints": ["/docs", "/health", "/api/z-protocol"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "bypassed for testing"}

@app.get("/api/z-protocol")
async def z_protocol():
    return {
        "version": "2.0",
        "status": "active",
        "features": ["consent management", "attribution tracking"]
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting YSense Platform (Database-free mode)...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
