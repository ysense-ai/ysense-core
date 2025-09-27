# 🚀 YSense Platform v4.0 - AI-Powered Wisdom API

from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio
import hashlib
import secrets

from src.models import User, WisdomDrop, get_session, generate_wisdom_id
from api.auth import get_current_user, log_audit
from src.orchestrator_v4 import YSenseOrchestrator
from src.z_protocol_v2_validator import z_protocol_validator

router = APIRouter()
orchestrator = YSenseOrchestrator()

# ==================== Pydantic Models ====================

class StoryInput(BaseModel):
    """User story input for AI analysis"""
    story: str
    experience_title: Optional[str] = None
    cultural_context: str = "Global"
    language: str = "en"
    
    @validator('story')
    def validate_story(cls, v):
        if not v or len(v.strip()) < 50:
            raise ValueError('Story must contain at least 50 characters to provide meaningful analysis')
        return v.strip()

class AIAnalysisResponse(BaseModel):
    """Response from AI analysis"""
    success: bool
    story: str
    layers: Dict[str, str]
    agent_feedback: Dict[str, str]
    overall_score: float
    processing_time: float
    status: str
    recommendations: List[str]

class WisdomReview(BaseModel):
    """User review and edits of AI-generated layers"""
    layers: Dict[str, str]
    user_edits: Dict[str, str] = {}
    approved: bool = False
    notes: Optional[str] = None

class DeepVibeInput(BaseModel):
    """Deep Vibe Distillation input"""
    vibe_words: List[str]
    vibe_words_explanation: str
    personal_connection: str
    essence_description: Optional[str] = None
    
    @validator('vibe_words')
    def validate_vibe_words(cls, v):
        if len(v) != 3:
            raise ValueError('Must provide exactly 3 vibe words')
        return v
    
    @validator('vibe_words_explanation')
    def validate_vibe_words_explanation(cls, v):
        if not v or len(v.strip()) < 20:
            raise ValueError('Vibe words explanation must contain at least 20 characters')
        return v.strip()
    
    @validator('personal_connection')
    def validate_personal_connection(cls, v):
        if not v or len(v.strip()) < 20:
            raise ValueError('Personal connection must contain at least 20 characters')
        return v.strip()

# ==================== API Endpoints ====================

@router.post("/analyze-story", response_model=AIAnalysisResponse)
async def analyze_story(story_input: StoryInput, request: Request, 
                       current_user: User = Depends(get_current_user)):
    """Analyze user story with AI and all 7 agents"""
    
    db = get_session()
    
    try:
        # Prepare user context
        user_context = {
            "user_id": current_user.id,
            "username": current_user.username,
            "cultural_context": story_input.cultural_context,
            "jurisdiction": current_user.jurisdiction,
            "age": current_user.age,
            "z_protocol_tier": current_user.z_protocol_tier
        }
        
        # Process story with orchestrator
        results = await orchestrator.process_story(story_input.story, user_context)
        
        # Get agent feedback
        agent_feedback = orchestrator.get_agent_feedback(results)
        
        # Generate recommendations
        recommendations = _generate_recommendations(results)
        
        # Log the analysis
        log_audit(db, current_user.id, "AI_STORY_ANALYSIS", "create", 
                 "wisdom", "AI_ANALYSIS", {
                     "story_length": len(story_input.story),
                     "cultural_context": story_input.cultural_context,
                     "overall_score": results["overall_score"]
                 }, request)
        
        db.close()
        
        return AIAnalysisResponse(
            success=True,
            story=story_input.story,
            layers=results["layers"],
            agent_feedback=agent_feedback,
            overall_score=results["overall_score"],
            processing_time=results["processing_time"],
            status=results["status"],
            recommendations=recommendations
        )
    
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}"
        )

@router.post("/review-layers")
async def review_layers(review: WisdomReview, request: Request,
                       current_user: User = Depends(get_current_user)):
    """Review and edit AI-generated layers"""
    
    db = get_session()
    
    try:
        # Apply user edits
        final_layers = review.layers.copy()
        final_layers.update(review.user_edits)
        
        # Validate final layers
        for layer_name, content in final_layers.items():
            if not content or len(content.strip()) < 20:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{layer_name} must contain at least 20 characters"
                )
        
        # Log the review
        log_audit(db, current_user.id, "LAYER_REVIEW", "update", 
                 "wisdom", "LAYER_REVIEW", {
                     "approved": review.approved,
                     "edits_count": len(review.user_edits),
                     "notes": review.notes
                 }, request)
        
        db.close()
        
        return {
            "success": True,
            "message": "Layers reviewed successfully",
            "final_layers": final_layers,
            "approved": review.approved
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Layer review failed: {str(e)}"
        )

@router.post("/create-wisdom-drop")
async def create_wisdom_drop(
    story_input: StoryInput,
    review: WisdomReview,
    vibe_input: DeepVibeInput,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Create complete wisdom drop from story to publication"""
    
    db = get_session()
    
    try:
        # Step 1: AI Analysis
        user_context = {
            "user_id": current_user.id,
            "username": current_user.username,
            "cultural_context": story_input.cultural_context,
            "jurisdiction": current_user.jurisdiction,
            "age": current_user.age,
            "z_protocol_tier": current_user.z_protocol_tier
        }
        
        analysis_results = await orchestrator.process_story(story_input.story, user_context)
        
        # Step 2: Apply user edits
        final_layers = analysis_results["layers"].copy()
        final_layers.update(review.user_edits)
        
        # Step 3: Create wisdom drop
        wisdom_id = generate_wisdom_id(current_user.username, story_input.experience_title or "AI Generated")
        
        wisdom_drop = WisdomDrop(
            id=wisdom_id,
            user_id=current_user.id,
            title=story_input.experience_title or "AI-Generated Wisdom",
            experience_title=story_input.experience_title,
            
            # Five Layers (from AI analysis + user edits)
            layer_narrative=final_layers["narrative"],
            layer_somatic=final_layers["somatic"],
            layer_attention=final_layers["attention"],
            layer_synesthetic=final_layers["synesthetic"],
            layer_temporal_auditory=final_layers["temporal_auditory"],
            
            # Deep Vibe Distillation
            vibe_words=vibe_input.vibe_words,
            vibe_words_explanation=vibe_input.vibe_words_explanation,
            personal_connection=vibe_input.personal_connection,
            essence=vibe_input.essence_description,
            distillation_completed=True,
            
            # Cultural Context
            cultural_context=story_input.cultural_context,
            language=story_input.language,
            
            # Quality & Scoring
            quality_score=analysis_results["overall_score"],
            completeness={"ai_generated": True, "user_reviewed": True},
            
            # Status
            status="complete",
            published=True,
            published_at=datetime.utcnow()
        )
        
        # Generate attribution hash using Z Protocol v2.0
        attribution_string = f"{current_user.id}:{wisdom_id}:{story_input.story}"
        wisdom_drop.attribution_hash = z_protocol_validator.generate_attribution_hash(
            current_user.id, wisdom_id, story_input.story
        )
        wisdom_drop.attribution_text = z_protocol_validator.generate_attribution_text({
            "username": current_user.username,
            "id": current_user.id
        })
        
        # Z Protocol v2.0 Compliance Validation
        user_data = {
            "consent_data_collection": True,  # Assuming user consented during registration
            "consent_commercial_use": True,
            "consent_ai_training": True,
            "consent_revenue_sharing": True,
            "consent_attribution": True,
            "consent_terms": True
        }
        
        wisdom_data = {
            "attribution_hash": wisdom_drop.attribution_hash,
            "attribution_text": wisdom_drop.attribution_text,
            "cultural_context": story_input.cultural_context,
            "cultural_multiplier": wisdom_drop.cultural_multiplier or 1.0,
            "quality_score": analysis_results.get("overall_score", 0.0) or 0.0,
            "completeness": analysis_results.get("completeness", {"overall": 0.0})
        }
        
        z_protocol_compliance = z_protocol_validator.validate_wisdom_drop(wisdom_data, user_data)
        wisdom_drop.z_protocol_score = z_protocol_compliance["z_protocol_score"]
        
        # Log Z Protocol v2.0 compliance audit
        audit_data = z_protocol_validator.audit_compliance(
            "WISDOM_DROP_CREATED", current_user.id, wisdom_id, z_protocol_compliance
        )
        
        # Calculate revenue potential
        agent_results = analysis_results.get("agent_results", {})
        revenue_result = agent_results.get("revenue_tracker", {})
        wisdom_drop.revenue_potential = revenue_result.get("estimated_revenue", 0)
        
        db.add(wisdom_drop)
        db.commit()
        db.refresh(wisdom_drop)
        
        # Log creation
        log_audit(db, current_user.id, "WISDOM_DROP_CREATED", "create", 
                 "wisdom", wisdom_id, {
                     "ai_generated": True,
                     "quality_score": analysis_results["overall_score"],
                     "revenue_potential": wisdom_drop.revenue_potential
                 }, request)
        
        return {
            "success": True,
            "message": "Wisdom drop created successfully",
            "wisdom_id": wisdom_id,
            "quality_score": analysis_results["overall_score"],
            "revenue_potential": wisdom_drop.revenue_potential,
            "z_protocol_score": z_protocol_compliance["z_protocol_score"],
            "z_protocol_compliant": z_protocol_compliance["compliant"],
            "z_protocol_violations": z_protocol_compliance["violations"],
            "z_protocol_recommendations": z_protocol_compliance["recommendations"],
            "attribution_hash": wisdom_drop.attribution_hash,
            "attribution_text": wisdom_drop.attribution_text,
            "agent_feedback": orchestrator.get_agent_feedback(analysis_results),
            "created_at": wisdom_drop.created_at.isoformat(),
            "audit_data": audit_data
        }
    
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Wisdom drop creation failed: {str(e)}"
        )

@router.get("/agent-status")
async def get_agent_status():
    """Get status of all 7 agents"""
    
    status_info = {}
    for name, agent in orchestrator.agents.items():
        status_info[name] = {
            "name": agent.name,
            "description": agent.description,
            "status": agent.status
        }
    
    return {
        "orchestrator_status": orchestrator.status,
        "agents": status_info,
        "total_agents": len(orchestrator.agents)
    }

@router.get("/analysis-history")
async def get_analysis_history(current_user: User = Depends(get_current_user)):
    """Get user's AI analysis history"""
    
    db = get_session()
    
    try:
        # Get recent wisdom drops created with AI
        wisdom_drops = db.query(WisdomDrop).filter(
            WisdomDrop.user_id == current_user.id,
            WisdomDrop.status == "complete"
        ).order_by(WisdomDrop.created_at.desc()).limit(10).all()
        
        history = []
        for drop in wisdom_drops:
            history.append({
                "id": drop.id,
                "title": drop.title,
                "created_at": drop.created_at.isoformat(),
                "quality_score": drop.quality_score,
                "revenue_potential": drop.revenue_potential,
                "cultural_context": drop.cultural_context,
                "ai_generated": drop.completeness.get("ai_generated", False) if drop.completeness else False
            })
        
        db.close()
        
        return {
            "success": True,
            "history": history,
            "total_count": len(history)
        }
    
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis history: {str(e)}"
        )

# ==================== Helper Functions ====================

def _generate_recommendations(results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on analysis results"""
    recommendations = []
    
    overall_score = results.get("overall_score", 0)
    if overall_score < 7.0:
        recommendations.append("Consider adding more detail to your story for better analysis")
    
    agent_results = results.get("agent_results", {})
    
    # Market recommendations
    market_result = agent_results.get("market_scanner", {})
    if market_result.get("market_potential", 0) > 0.7:
        recommendations.append("High market potential detected - consider targeting specific audiences")
    
    # Quality recommendations
    quality_result = agent_results.get("quality_assessor", {})
    if quality_result.get("quality_score", 0) < 0.7:
        recommendations.append("Enhance story depth for higher quality score")
    
    # Cultural recommendations
    cultural_result = agent_results.get("cultural_context", {})
    if cultural_result.get("cultural_score", 0) > 0.8:
        recommendations.append("Strong cultural elements - consider localization opportunities")
    
    return recommendations
