# api/revenue.py
"""
YSense Platform v3.0 Revenue Management API
Handles revenue calculation, distribution, and payments
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import secrets

from src.models import User, WisdomDrop, RevenueRecord, UsageRecord, get_session
from api.auth import get_current_user, log_audit
from src.config import Config

router = APIRouter()

# ==================== Pydantic Models ====================

class UsageReport(BaseModel):
    """Report usage of wisdom drop"""
    wisdom_drop_id: str
    usage_type: str  # ai_training, research, commercial
    usage_context: str
    client_id: str
    attribution_included: bool = True
    attribution_format: Optional[str] = None

class RevenueDistribution(BaseModel):
    """Revenue distribution details"""
    user_id: str
    wisdom_drop_id: str
    amount: float
    currency: str = "EUR"
    revenue_type: str  # usage, licensing, bonus

class PaymentRequest(BaseModel):
    """Request payment of pending earnings"""
    payment_method: str  # bank_transfer, paypal, crypto
    payment_details: Dict  # Method-specific details

class RevenueAnalytics(BaseModel):
    """Revenue analytics response"""
    total_earnings: float
    pending_earnings: float
    paid_earnings: float
    revenue_by_type: Dict[str, float]
    revenue_by_drop: List[Dict]
    revenue_trend: List[Dict]
    tier_info: Dict

# ==================== Helper Functions ====================

def calculate_usage_revenue(wisdom_drop: WisdomDrop, usage_type: str, user: User) -> float:
    """Calculate revenue for a specific usage"""
    
    # Base rates by usage type
    base_rates = {
        "ai_training": Config.BASE_RATE_EUR * 2.0,  # €0.20
        "research": Config.BASE_RATE_EUR * 1.5,     # €0.15
        "commercial": Config.BASE_RATE_EUR * 3.0,   # €0.30
        "educational": Config.BASE_RATE_EUR * 1.0,  # €0.10
        "default": Config.BASE_RATE_EUR             # €0.10
    }
    
    base_rate = base_rates.get(usage_type, base_rates["default"])
    
    # Apply quality multiplier
    quality_multiplier = wisdom_drop.quality_score / 100.0
    
    # Apply cultural multiplier
    cultural_multipliers = {
        'Malaysian': 1.6,
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
    
    # Apply Z Protocol tier multiplier
    tier_multipliers = {
        "Diamond": 1.5,
        "Platinum": 1.3,
        "Gold": 1.2,
        "Silver": 1.1,
        "Bronze": 1.0
    }
    
    tier_multiplier = tier_multipliers.get(user.z_protocol_tier, 1.0)
    
    # Calculate gross revenue
    gross_revenue = base_rate * quality_multiplier * cultural_multiplier * tier_multiplier
    
    # Apply user's revenue share percentage
    user_revenue = gross_revenue * (user.revenue_share_percentage / 100.0)
    
    return round(user_revenue, 2)

def calculate_platform_fees(gross_revenue: float) -> Dict[str, float]:
    """Calculate platform and community fees"""
    
    platform_fee = gross_revenue * (Config.PLATFORM_FEE_PERCENTAGE / 100.0)
    community_share = gross_revenue * (Config.COMMUNITY_SHARE_PERCENTAGE / 100.0)
    
    return {
        "platform_fee": round(platform_fee, 2),
        "community_share": round(community_share, 2)
    }

def check_payment_threshold(user: User) -> bool:
    """Check if user has reached payment threshold"""
    
    PAYMENT_THRESHOLD_EUR = 50.0
    return user.pending_earnings >= PAYMENT_THRESHOLD_EUR

# ==================== API Endpoints ====================

@router.post("/report-usage", status_code=status.HTTP_201_CREATED)
async def report_usage(
    usage_data: UsageReport,
    request: Request
):
    """Report usage of wisdom drop (called by AI companies/platforms)"""
    
    db = get_session()
    
    # Get wisdom drop
    wisdom_drop = db.query(WisdomDrop).filter(
        WisdomDrop.id == usage_data.wisdom_drop_id,
        WisdomDrop.published == True
    ).first()
    
    if not wisdom_drop:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wisdom drop not found or not published"
        )
    
    # Get user
    user = db.query(User).filter(User.id == wisdom_drop.user_id).first()
    
    # Calculate revenue
    revenue_amount = calculate_usage_revenue(wisdom_drop, usage_data.usage_type, user)
    
    # Create usage record
    usage_record = UsageRecord(
        id=f"USAGE_{secrets.token_hex(8).upper()}",
        wisdom_drop_id=wisdom_drop.id,
        usage_type=usage_data.usage_type,
        usage_context=usage_data.usage_context,
        client_id=usage_data.client_id,
        attribution_included=usage_data.attribution_included,
        attribution_format=usage_data.attribution_format,
        revenue_generated=revenue_amount
    )
    
    db.add(usage_record)
    
    # Create revenue record
    revenue_record = RevenueRecord(
        id=f"REV_{secrets.token_hex(8).upper()}",
        user_id=user.id,
        wisdom_drop_id=wisdom_drop.id,
        amount=revenue_amount,
        currency="EUR",
        revenue_type=usage_data.usage_type,
        payment_status="pending"
    )
    
    db.add(revenue_record)
    
    # Update wisdom drop metrics
    wisdom_drop.times_accessed += 1
    wisdom_drop.revenue_generated += revenue_amount
    
    # Update user earnings
    user.pending_earnings += revenue_amount
    user.total_earnings += revenue_amount
    
    # Log usage
    log_audit(db, user.id, "REVENUE_GENERATED", "create",
             "usage_record", usage_record.id,
             {"amount": revenue_amount, "usage_type": usage_data.usage_type},
             request)
    
    db.commit()
    
    # Check if attribution was included
    if not usage_data.attribution_included:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attribution is required for all usage"
        )
    
    db.close()
    
    return {
        "usage_id": usage_record.id,
        "revenue_generated": revenue_amount,
        "attribution_text": wisdom_drop.attribution_text,
        "attribution_hash": wisdom_drop.attribution_hash[:16] + "...",
        "message": "Usage recorded successfully"
    }

@router.get("/analytics")
async def get_revenue_analytics(
    current_user: User = Depends(get_current_user),
    days: int = 30
):
    """Get revenue analytics for current user"""
    
    db = get_session()
    
    # Calculate date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get revenue records
    revenue_records = db.query(RevenueRecord).filter(
        RevenueRecord.user_id == current_user.id,
        RevenueRecord.created_at >= start_date
    ).all()
    
    # Calculate revenue by type
    revenue_by_type = {}
    for record in revenue_records:
        if record.revenue_type not in revenue_by_type:
            revenue_by_type[record.revenue_type] = 0.0
        revenue_by_type[record.revenue_type] += record.amount
    
    # Get top performing wisdom drops
    top_drops = db.query(
        WisdomDrop.id,
        WisdomDrop.title,
        func.sum(RevenueRecord.amount).label('total_revenue')
    ).join(
        RevenueRecord
    ).filter(
        WisdomDrop.user_id == current_user.id
    ).group_by(
        WisdomDrop.id
    ).order_by(
        func.sum(RevenueRecord.amount).desc()
    ).limit(5).all()
    
    # Calculate daily revenue trend
    revenue_trend = db.query(
        func.date(RevenueRecord.created_at).label('date'),
        func.sum(RevenueRecord.amount).label('revenue')
    ).filter(
        RevenueRecord.user_id == current_user.id,
        RevenueRecord.created_at >= start_date
    ).group_by(
        func.date(RevenueRecord.created_at)
    ).all()
    
    db.close()
    
    # Get tier information
    tier_info = {
        "current_tier": current_user.z_protocol_tier,
        "revenue_share_percentage": current_user.revenue_share_percentage,
        "z_protocol_score": current_user.z_protocol_score,
        "next_tier_requirements": get_next_tier_requirements(current_user)
    }
    
    return {
        "total_earnings": current_user.total_earnings,
        "pending_earnings": current_user.pending_earnings,
        "paid_earnings": current_user.total_earnings - current_user.pending_earnings,
        "revenue_by_type": revenue_by_type,
        "top_performing_drops": [
            {
                "id": drop.id,
                "title": drop.title,
                "revenue": drop.total_revenue
            }
            for drop in top_drops
        ],
        "revenue_trend": [
            {
                "date": trend.date.isoformat() if trend.date else None,
                "revenue": trend.revenue
            }
            for trend in revenue_trend
        ],
        "tier_info": tier_info,
        "payment_threshold_reached": check_payment_threshold(current_user)
    }

@router.post("/request-payment")
async def request_payment(
    payment_request: PaymentRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Request payment of pending earnings"""
    
    db = get_session()
    
    # Check payment threshold
    if not check_payment_threshold(current_user):
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Minimum payment threshold is €50. Current pending: €{current_user.pending_earnings}"
        )
    
    # Create payment record
    payment_id = f"PAY_{secrets.token_hex(8).upper()}"
    
    # Get all pending revenue records
    pending_records = db.query(RevenueRecord).filter(
        RevenueRecord.user_id == current_user.id,
        RevenueRecord.payment_status == "pending"
    ).all()
    
    total_amount = sum(record.amount for record in pending_records)
    
    # Mark records as processing
    for record in pending_records:
        record.payment_status = "processing"
        record.payment_date = datetime.utcnow()
        record.payment_method = payment_request.payment_method
        record.transaction_id = payment_id
    
    # Update user earnings
    user = db.query(User).filter(User.id == current_user.id).first()
    user.pending_earnings = 0.0
    
    # Log payment request
    log_audit(db, current_user.id, "PAYMENT_REQUEST", "create",
             "payment", payment_id,
             {
                 "amount": total_amount,
                 "method": payment_request.payment_method,
                 "records_count": len(pending_records)
             },
             request)
    
    db.commit()
    db.close()
    
    return {
        "payment_id": payment_id,
        "amount": total_amount,
        "currency": "EUR",
        "payment_method": payment_request.payment_method,
        "status": "processing",
        "estimated_completion": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "message": "Payment request submitted successfully. Processing typically takes 3-5 business days."
    }

@router.get("/payment-history")
async def get_payment_history(
    current_user: User = Depends(get_current_user),
    limit: int = 10
):
    """Get payment history for current user"""
    
    db = get_session()
    
    # Get unique payment transactions
    payments = db.query(
        RevenueRecord.transaction_id,
        func.sum(RevenueRecord.amount).label('amount'),
        func.min(RevenueRecord.payment_date).label('payment_date'),
        func.min(RevenueRecord.payment_method).label('payment_method'),
        func.min(RevenueRecord.payment_status).label('payment_status')
    ).filter(
        RevenueRecord.user_id == current_user.id,
        RevenueRecord.transaction_id != None
    ).group_by(
        RevenueRecord.transaction_id
    ).order_by(
        func.min(RevenueRecord.payment_date).desc()
    ).limit(limit).all()
    
    db.close()
    
    return {
        "payments": [
            {
                "transaction_id": payment.transaction_id,
                "amount": payment.amount,
                "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
                "payment_method": payment.payment_method,
                "status": payment.payment_status
            }
            for payment in payments
        ],
        "total_paid": current_user.total_earnings - current_user.pending_earnings,
        "pending_amount": current_user.pending_earnings
    }

@router.get("/tier-progress")
async def get_tier_progress(
    current_user: User = Depends(get_current_user)
):
    """Get progress towards next revenue tier"""
    
    db = get_session()
    
    # Count published wisdom drops
    published_drops = db.query(WisdomDrop).filter(
        WisdomDrop.user_id == current_user.id,
        WisdomDrop.published == True
    ).count()
    
    db.close()
    
    # Define tier requirements
    tier_requirements = {
        "Bronze": {"min_score": 0, "min_drops": 0, "revenue_share": 30},
        "Silver": {"min_score": 60, "min_drops": 5, "revenue_share": 35},
        "Gold": {"min_score": 75, "min_drops": 15, "revenue_share": 40},
        "Platinum": {"min_score": 85, "min_drops": 30, "revenue_share": 45},
        "Diamond": {"min_score": 95, "min_drops": 50, "revenue_share": 50}
    }
    
    current_tier = current_user.z_protocol_tier
    tier_order = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
    current_index = tier_order.index(current_tier)
    
    next_tier_info = None
    if current_index < len(tier_order) - 1:
        next_tier = tier_order[current_index + 1]
        next_requirements = tier_requirements[next_tier]
        
        next_tier_info = {
            "tier_name": next_tier,
            "requirements": {
                "z_protocol_score_needed": next_requirements["min_score"],
                "wisdom_drops_needed": next_requirements["min_drops"],
                "revenue_share": next_requirements["revenue_share"]
            },
            "current_progress": {
                "z_protocol_score": current_user.z_protocol_score,
                "wisdom_drops": published_drops
            },
            "progress_percentage": min(
                (current_user.z_protocol_score / next_requirements["min_score"]) * 50 +
                (published_drops / next_requirements["min_drops"]) * 50,
                100
            )
        }
    
    return {
        "current_tier": current_tier,
        "revenue_share_percentage": current_user.revenue_share_percentage,
        "z_protocol_score": current_user.z_protocol_score,
        "published_drops": published_drops,
        "total_earnings": current_user.total_earnings,
        "next_tier": next_tier_info
    }

def get_next_tier_requirements(user: User) -> Dict:
    """Helper function to get next tier requirements"""
    
    tier_order = ["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
    tier_requirements = {
        "Silver": {"min_score": 60, "min_drops": 5},
        "Gold": {"min_score": 75, "min_drops": 15},
        "Platinum": {"min_score": 85, "min_drops": 30},
        "Diamond": {"min_score": 95, "min_drops": 50}
    }
    
    current_index = tier_order.index(user.z_protocol_tier)
    
    if current_index >= len(tier_order) - 1:
        return {"message": "Maximum tier achieved!"}
    
    next_tier = tier_order[current_index + 1]
    return tier_requirements.get(next_tier, {})
