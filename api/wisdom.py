# api/wisdom.py
"""
YSense Platform v3.0 Wisdom Management API
Handles wisdom drop creation, distillation, and publication
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import secrets

from src.models import User, WisdomDrop, UsageRecord, ZProtocolValidation, get_session, generate_wisdom_id
from api.auth import get_current_user, log_audit
from src.five_prompt_toolkit import FivePromptToolkit
from src.z_protocol_enhanced import ZProtocolValidator

router = APIRouter()
toolkit = FivePromptToolkit()
z_validator = ZProtocolValidator()

# ==================== Pydantic Models ====================

class WisdomDropCreate(BaseModel):
    """Create a new wisdom drop with Five-Layer responses"""
    title: str
    experience_title: str
    
    # Five Layers (required)
    layer_narrative: str
    layer_somatic: str  
    layer_attention: str
    layer_synesthetic: str
    layer_temporal_auditory: str
    
    # Cultural Context
    cultural_context: str = "Global"
    language: str = "en"
    
    @validator('layer_narrative', 'layer_somatic', 'layer_attention', 
               'layer_synesthetic', 'layer_temporal_auditory')
    def validate_layer_content(cls, v):
        if not v or len(v.strip()) < 20:
            raise ValueError(f'Each layer must contain at least 20 characters. Current length: {len(v.strip())} characters. Please provide more detailed responses to capture the full depth of your experience.')
        return v.strip()

class DeepVibeDistillation(BaseModel):
    """Complete the Deep Vibe Distillation process"""
    vibe_words: List[str]
    personal_connection: str
    essence: Optional[str] = None
    
    @validator('vibe_words')
    def validate_vibe_words(cls, v):
        # Special case for "A drop"
        if v == ["A drop 💧"] or v == ["A drop"]:
            return v
        if len(v) != 3:
            raise ValueError('Deep Vibe Distillation requires exactly 3 words')
        for word in v:
            if not word or len(word) < 2:
                raise ValueError('Each vibe word must be meaningful')
            if len(word) > 20:
                raise ValueError('Vibe words should be concise (under 20 characters)')
        return v

class WisdomDropUpdate(BaseModel):
    """Update wisdom drop content"""
    title: Optional[str] = None
    layer_narrative: Optional[str] = None
    layer_somatic: Optional[str] = None
    layer_attention: Optional[str] = None
    layer_synesthetic: Optional[str] = None
    layer_temporal_auditory: Optional[str] = None
    cultural_context: Optional[str] = None

class WisdomDropPublish(BaseModel):
    """Publish wisdom drop after validation"""
    confirm_authenticity: bool
    confirm_no_copyright: bool
    confirm_attribution: bool
    
    @validator('confirm_authenticity', 'confirm_no_copyright', 'confirm_attribution')
    def validate_confirmations(cls, v):
        if not v:
            raise ValueError('All confirmations must be accepted before publishing')
        return v

# ==================== Helper Functions ====================

def generate_attribution_hash(wisdom_drop: WisdomDrop) -> str:
    """Generate cryptographic attribution hash"""
    data = {
        'author_id': wisdom_drop.user_id,
        'title': wisdom_drop.title,
        'timestamp': wisdom_drop.created_at.isoformat(),
        'layers_hash': hashlib.sha256(
            f"{wisdom_drop.layer_narrative}{wisdom_drop.layer_somatic}".encode()
        ).hexdigest()[:16]
    }
    
    attribution_string = f"{data['author_id']}:{data['title']}:{data['timestamp']}:{data['layers_hash']}"
    return hashlib.sha256(attribution_string.encode()).hexdigest()

async def validate_with_z_protocol(wisdom_drop: WisdomDrop, user: User) -> Dict:
    """Validate wisdom drop with Z Protocol"""
    
    validation_data = {
        "consent_record": user.consent_record,
        "attribution": {
            "contributor_id": user.id,
            "contributor_name": user.attribution_name,
            "culture": wisdom_drop.cultural_context,
            "location": user.jurisdiction,
            "contribution_date": wisdom_drop.created_at.isoformat()
        },
        "authenticity_declaration": {
            "is_original": True,
            "contains_copyrighted": False,
            "accept_liability": True
        },
        "contributor_verified": user.age_verified,
        "contributor_age": user.age,
        "gdpr_compliant": True,
        "copyright_cleared": True,
        "terms_accepted": True,
        "usage_disclosed": True,
        "revenue_explained": True,
        "retention_explained": True,
        "sharing_disclosed": True,
        "audit_trail": {
            "submission_timestamp": wisdom_drop.created_at.isoformat(),
            "ip_address": "recorded",
            "user_agent": "recorded",
            "consent_timestamp": user.consent_timestamp.isoformat(),
            "validation_history": []
        },
        "content": {
            "wisdom": wisdom_drop.title,
            "layers": {
                "narrative": wisdom_drop.layer_narrative,
                "somatic": wisdom_drop.layer_somatic,
                "attention": wisdom_drop.layer_attention,
                "synesthetic": wisdom_drop.layer_synesthetic,
                "temporal_auditory": wisdom_drop.layer_temporal_auditory
            }
        }
    }
    
    return await z_validator.validate_wisdom_drop(validation_data)

def calculate_revenue_potential(wisdom_drop: WisdomDrop) -> float:
    """Calculate revenue potential based on quality and cultural context"""
    base_rate = 50.0  # €50 base
    
    # Quality multiplier
    quality_multiplier = wisdom_drop.quality_score / 100.0
    
    # Cultural multiplier based on toolkit configuration
    cultural_multipliers = {
        'Malaysian': 1.5,
        'Malaysian Chinese': 1.6,
        'Hokkien': 1.7,
        'Southeast Asian': 1.3,
        'Kampung': 1.4,
        'Indigenous': 1.4,
        'Global South': 1.15,
        'Global': 1.0
    }
    
    cultural_multiplier = cultural_multipliers.get(
        wisdom_drop.cultural_context,
        1.0
    )
    
    # Distillation bonus
    distillation_bonus = 1.2 if wisdom_drop.distillation_completed else 1.0
    
    revenue = base_rate * quality_multiplier * cultural_multiplier * distillation_bonus
    
    return round(revenue, 2)

# ==================== API Endpoints ====================

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_wisdom_drop(
    wisdom_data: WisdomDropCreate,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Create a new wisdom drop (Stage 1: Five Layers)"""
    
    db = get_session()
    
    # Generate wisdom drop ID
    wisdom_id = generate_wisdom_id(current_user.id, wisdom_data.title)
    
    # Create wisdom drop
    wisdom_drop = WisdomDrop(
        id=wisdom_id,
        user_id=current_user.id,
        title=wisdom_data.title,
        experience_title=wisdom_data.experience_title,
        
        # Five Layers
        layer_narrative=wisdom_data.layer_narrative,
        layer_somatic=wisdom_data.layer_somatic,
        layer_attention=wisdom_data.layer_attention,
        layer_synesthetic=wisdom_data.layer_synesthetic,
        layer_temporal_auditory=wisdom_data.layer_temporal_auditory,
        
        # Cultural Context
        cultural_context=wisdom_data.cultural_context,
        language=wisdom_data.language,
        
        # Status
        status="awaiting_distillation",
        moderation_status="pending",
        
        # Attribution
        attribution_hash="",  # Will be set after creation
        attribution_text=f"Wisdom by {current_user.attribution_name} ({wisdom_data.cultural_context})"
    )
    
    # Calculate initial quality score
    wisdom_drop.quality_score = wisdom_drop.calculate_quality_score()
    
    # Generate attribution hash
    wisdom_drop.attribution_hash = generate_attribution_hash(wisdom_drop)
    
    db.add(wisdom_drop)
    
    # Log creation
    log_audit(db, current_user.id, "WISDOM_DROP_CREATE", "create", 
             "wisdom_drop", wisdom_id,
             {"title": wisdom_data.title, "cultural_context": wisdom_data.cultural_context},
             request)
    
    db.commit()
    db.close()
    
    return {
        "id": wisdom_id,
        "title": wisdom_drop.title,
        "status": wisdom_drop.status,
        "quality_score": wisdom_drop.quality_score,
        "attribution_hash": wisdom_drop.attribution_hash[:16] + "...",
        "message": "Wisdom drop created. Please complete Deep Vibe Distillation to maximize quality.",
        "next_step": f"/api/v2/wisdom/{wisdom_id}/distill"
    }

@router.post("/{wisdom_id}/distill")
async def complete_distillation(
    wisdom_id: str,
    distillation: DeepVibeDistillation,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Complete Deep Vibe Distillation (Stage 2)"""
    
    db = get_session()
    
    # Get wisdom drop
    wisdom_drop = db.query(WisdomDrop).filter(
        WisdomDrop.id == wisdom_id,
        WisdomDrop.user_id == current_user.id
    ).first()
    
    if not wisdom_drop:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wisdom drop not found"
        )
    
    if wisdom_drop.distillation_completed:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Distillation already completed"
        )
    
    # Apply distillation
    wisdom_drop.vibe_words = distillation.vibe_words
    wisdom_drop.personal_connection = distillation.personal_connection
    wisdom_drop.essence = distillation.essence or f"{' + '.join(distillation.vibe_words)} through {distillation.personal_connection[:50]}"
    wisdom_drop.distillation_completed = True
    wisdom_drop.status = "complete"
    wisdom_drop.updated_at = datetime.utcnow()
    
    # Recalculate quality score with distillation bonus
    wisdom_drop.quality_score = wisdom_drop.calculate_quality_score()
    
    # Calculate revenue potential
    wisdom_drop.revenue_potential = calculate_revenue_potential(wisdom_drop)
    
    # Log distillation
    log_audit(db, current_user.id, "WISDOM_DISTILLATION", "update",
             "wisdom_drop", wisdom_id,
             {"vibe_words": distillation.vibe_words},
             request)
    
    db.commit()
    db.close()
    
    return {
        "id": wisdom_id,
        "title": wisdom_drop.title,
        "vibe_words": wisdom_drop.vibe_words,
        "essence": wisdom_drop.essence,
        "quality_score": wisdom_drop.quality_score,
        "revenue_potential": wisdom_drop.revenue_potential,
        "status": wisdom_drop.status,
        "message": "Deep Vibe Distillation complete! Your wisdom drop is ready for publication."
    }

@router.post("/{wisdom_id}/publish")
async def publish_wisdom_drop(
    wisdom_id: str,
    publish_data: WisdomDropPublish,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Publish wisdom drop after Z Protocol validation"""
    
    db = get_session()
    
    # Get wisdom drop
    wisdom_drop = db.query(WisdomDrop).filter(
        WisdomDrop.id == wisdom_id,
        WisdomDrop.user_id == current_user.id
    ).first()
    
    if not wisdom_drop:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wisdom drop not found"
        )
    
    if not wisdom_drop.distillation_completed:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete Deep Vibe Distillation before publishing"
        )
    
    if wisdom_drop.published:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wisdom drop already published"
        )
    
    # Run Z Protocol validation
    validation_result = await validate_with_z_protocol(wisdom_drop, current_user)
    
    # Save validation record
    z_validation = ZProtocolValidation(
        id=f"ZVAL_{secrets.token_hex(8).upper()}",
        wisdom_drop_id=wisdom_id,
        consent_score=validation_result['validation_details'].get('consent', {}).get('score', 0),
        attribution_score=validation_result['validation_details'].get('attribution', {}).get('score', 0),
        authenticity_score=validation_result['validation_details'].get('authenticity', {}).get('score', 0),
        dignity_score=validation_result['validation_details'].get('dignity', {}).get('score', 0),
        transparency_score=validation_result['validation_details'].get('transparency', {}).get('score', 0),
        legal_score=validation_result['validation_details'].get('legal', {}).get('score', 0),
        audit_score=validation_result['validation_details'].get('audit', {}).get('score', 0),
        total_score=validation_result['z_protocol_score'],
        certification_status=validation_result['certification'],
        validation_details=validation_result['validation_details'],
        failures=validation_result.get('failures', []),
        warnings=validation_result.get('warnings', [])
    )
    
    db.add(z_validation)
    
    # Check if validation passed
    if validation_result['z_protocol_score'] < 80:
        db.commit()
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Z Protocol validation failed (Score: {validation_result['z_protocol_score']}/100)",
            headers={"X-Validation-Failures": ", ".join(validation_result.get('failures', []))}
        )
    
    # Publish wisdom drop
    wisdom_drop.published = True
    wisdom_drop.published_at = datetime.utcnow()
    wisdom_drop.status = "published"
    wisdom_drop.moderation_status = "approved"
    wisdom_drop.z_protocol_score = validation_result['z_protocol_score']
    
    # Update user's Z Protocol score (rolling average)
    user = db.query(User).filter(User.id == current_user.id).first()
    current_drops = db.query(WisdomDrop).filter(
        WisdomDrop.user_id == current_user.id,
        WisdomDrop.published == True
    ).count()
    
    if current_drops > 0:
        user.z_protocol_score = (
            (user.z_protocol_score * (current_drops - 1) + wisdom_drop.z_protocol_score) / 
            current_drops
        )
    else:
        user.z_protocol_score = wisdom_drop.z_protocol_score
    
    # Update user tier based on new score
    if user.z_protocol_score >= 95:
        user.z_protocol_tier = "Diamond"
        user.revenue_tier = "Diamond"
        user.revenue_share_percentage = 50.0
    elif user.z_protocol_score >= 85:
        user.z_protocol_tier = "Platinum"
        user.revenue_tier = "Platinum"
        user.revenue_share_percentage = 45.0
    elif user.z_protocol_score >= 75:
        user.z_protocol_tier = "Gold"
        user.revenue_tier = "Gold"
        user.revenue_share_percentage = 40.0
    elif user.z_protocol_score >= 60:
        user.z_protocol_tier = "Silver"
        user.revenue_tier = "Silver"
        user.revenue_share_percentage = 35.0
    
    # Log publication
    log_audit(db, current_user.id, "WISDOM_PUBLISH", "update",
             "wisdom_drop", wisdom_id,
             {"z_protocol_score": validation_result['z_protocol_score']},
             request)
    
    db.commit()
    db.close()
    
    return {
        "id": wisdom_id,
        "title": wisdom_drop.title,
        "published": True,
        "published_at": wisdom_drop.published_at.isoformat(),
        "z_protocol_score": wisdom_drop.z_protocol_score,
        "certification": validation_result['certification'],
        "revenue_potential": wisdom_drop.revenue_potential,
        "attribution_hash": wisdom_drop.attribution_hash[:16] + "...",
        "message": f"Wisdom drop published successfully! Z Protocol Score: {wisdom_drop.z_protocol_score}/100"
    }

@router.get("/my-drops")
async def get_my_wisdom_drops(
    current_user: User = Depends(get_current_user),
    status: Optional[str] = None,
    published: Optional[bool] = None
):
    """Get all wisdom drops for current user"""
    
    db = get_session()
    
    query = db.query(WisdomDrop).filter(WisdomDrop.user_id == current_user.id)
    
    if status:
        query = query.filter(WisdomDrop.status == status)
    
    if published is not None:
        query = query.filter(WisdomDrop.published == published)
    
    wisdom_drops = query.order_by(WisdomDrop.created_at.desc()).all()
    
    db.close()
    
    return {
        "total": len(wisdom_drops),
        "wisdom_drops": [
            {
                "id": drop.id,
                "title": drop.title,
                "status": drop.status,
                "published": drop.published,
                "distillation_completed": drop.distillation_completed,
                "vibe_words": drop.vibe_words,
                "quality_score": drop.quality_score,
                "z_protocol_score": drop.z_protocol_score,
                "revenue_potential": drop.revenue_potential,
                "revenue_generated": drop.revenue_generated,
                "created_at": drop.created_at.isoformat()
            }
            for drop in wisdom_drops
        ]
    }

@router.get("/{wisdom_id}")
async def get_wisdom_drop(
    wisdom_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed wisdom drop information"""
    
    db = get_session()
    
    wisdom_drop = db.query(WisdomDrop).filter(
        WisdomDrop.id == wisdom_id,
        WisdomDrop.user_id == current_user.id
    ).first()
    
    if not wisdom_drop:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wisdom drop not found"
        )
    
    db.close()
    
    return {
        "id": wisdom_drop.id,
        "title": wisdom_drop.title,
        "experience_title": wisdom_drop.experience_title,
        "layers": {
            "narrative": wisdom_drop.layer_narrative,
            "somatic": wisdom_drop.layer_somatic,
            "attention": wisdom_drop.layer_attention,
            "synesthetic": wisdom_drop.layer_synesthetic,
            "temporal_auditory": wisdom_drop.layer_temporal_auditory
        },
        "distillation": {
            "completed": wisdom_drop.distillation_completed,
            "vibe_words": wisdom_drop.vibe_words,
            "personal_connection": wisdom_drop.personal_connection,
            "essence": wisdom_drop.essence
        },
        "cultural_context": wisdom_drop.cultural_context,
        "quality_score": wisdom_drop.quality_score,
        "z_protocol_score": wisdom_drop.z_protocol_score,
        "revenue_potential": wisdom_drop.revenue_potential,
        "revenue_generated": wisdom_drop.revenue_generated,
        "status": wisdom_drop.status,
        "published": wisdom_drop.published,
        "attribution_hash": wisdom_drop.attribution_hash,
        "created_at": wisdom_drop.created_at.isoformat()
    }
