# api/legal.py
"""
YSense Platform v3.0 Legal Compliance API
Handles Terms of Service, GDPR/PDPA compliance, data requests
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import io
import csv
import secrets

from src.models import User, WisdomDrop, ConsentRecord, AuditLog, get_session
from api.auth import get_current_user, log_audit
from src.compliance import TermsOfServiceV2, ConsentManagementV2

router = APIRouter()
tos_manager = TermsOfServiceV2()
consent_manager = ConsentManagementV2()

# ==================== Pydantic Models ====================

class DataExportRequest(BaseModel):
    """Request data export (GDPR/PDPA compliance)"""
    export_format: str = "json"  # json, csv
    include_wisdom_drops: bool = True
    include_revenue_records: bool = True
    include_audit_logs: bool = False

class DataDeletionRequest(BaseModel):
    """Request data deletion"""
    confirm_deletion: bool
    reason: Optional[str] = None
    keep_published_wisdom: bool = True  # Keep for attribution

class ConsentReviewRequest(BaseModel):
    """Review and update consents"""
    consent_updates: Dict[str, bool]

class ComplianceCheckResponse(BaseModel):
    """Compliance status response"""
    gdpr_compliant: bool
    pdpa_compliant: bool
    consent_valid: bool
    data_retention_compliant: bool
    issues: List[str]
    recommendations: List[str]

# ==================== Helper Functions ====================

def anonymize_user_data(user: User) -> Dict:
    """Anonymize user data for deletion while preserving attribution"""
    
    anonymized_id = f"ANON_{secrets.token_hex(8).upper()}"
    
    return {
        "anonymized_id": anonymized_id,
        "original_id": user.id,
        "anonymization_date": datetime.utcnow().isoformat(),
        "preserved_attribution": user.attribution_name,
        "cultural_context": user.cultural_context
    }

def generate_data_export(user: User, db: Session, export_format: str, 
                        include_wisdom: bool, include_revenue: bool, 
                        include_audit: bool) -> str:
    """Generate complete data export for user"""
    
    export_data = {
        "export_date": datetime.utcnow().isoformat(),
        "user_data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "jurisdiction": user.jurisdiction,
            "cultural_context": user.cultural_context,
            "z_protocol_tier": user.z_protocol_tier,
            "revenue_tier": user.revenue_tier,
            "total_earnings": user.total_earnings,
            "created_at": user.created_at.isoformat()
        }
    }
    
    # Export wisdom drops
    if include_wisdom:
        from src.models import WisdomDrop
        wisdom_drops = db.query(WisdomDrop).filter(
            WisdomDrop.user_id == user.id
        ).all()
        
        export_data["wisdom_drops"] = [
            {
                "id": drop.id,
                "title": drop.title,
                "layers": {
                    "narrative": drop.layer_narrative,
                    "somatic": drop.layer_somatic,
                    "attention": drop.layer_attention,
                    "synesthetic": drop.layer_synesthetic,
                    "temporal_auditory": drop.layer_temporal_auditory
                },
                "vibe_words": drop.vibe_words,
                "essence": drop.essence,
                "quality_score": drop.quality_score,
                "revenue_generated": drop.revenue_generated,
                "published": drop.published,
                "created_at": drop.created_at.isoformat()
            }
            for drop in wisdom_drops
        ]
    
    # Export revenue records
    if include_revenue:
        from src.models import RevenueRecord
        revenue_records = db.query(RevenueRecord).filter(
            RevenueRecord.user_id == user.id
        ).all()
        
        export_data["revenue_records"] = [
            {
                "id": record.id,
                "amount": record.amount,
                "currency": record.currency,
                "revenue_type": record.revenue_type,
                "payment_status": record.payment_status,
                "created_at": record.created_at.isoformat()
            }
            for record in revenue_records
        ]
    
    # Export audit logs
    if include_audit:
        audit_logs = db.query(AuditLog).filter(
            AuditLog.user_id == user.id
        ).order_by(AuditLog.created_at.desc()).limit(1000).all()
        
        export_data["audit_logs"] = [
            {
                "id": log.id,
                "action": log.action,
                "action_type": log.action_type,
                "created_at": log.created_at.isoformat()
            }
            for log in audit_logs
        ]
    
    # Format export
    if export_format == "csv":
        # Flatten for CSV export
        output = io.StringIO()
        writer = csv.writer(output)
        
        # User data
        writer.writerow(["User Data"])
        writer.writerow(["Field", "Value"])
        for key, value in export_data["user_data"].items():
            writer.writerow([key, value])
        
        writer.writerow([])
        
        # Wisdom drops
        if include_wisdom and "wisdom_drops" in export_data:
            writer.writerow(["Wisdom Drops"])
            if export_data["wisdom_drops"]:
                headers = ["id", "title", "quality_score", "revenue_generated", 
                          "published", "created_at"]
                writer.writerow(headers)
                for drop in export_data["wisdom_drops"]:
                    writer.writerow([
                        drop["id"], drop["title"], drop["quality_score"],
                        drop["revenue_generated"], drop["published"], 
                        drop["created_at"]
                    ])
        
        return output.getvalue()
    else:
        # JSON format
        return json.dumps(export_data, indent=2)

# ==================== API Endpoints ====================

@router.get("/terms-of-service")
async def get_terms_of_service(
    jurisdiction: str = "Malaysia"
):
    """Get current Terms of Service"""
    
    terms = tos_manager.get_regional_terms(jurisdiction)
    
    return {
        "version": tos_manager.version,
        "effective_date": tos_manager.effective_date,
        "jurisdiction": jurisdiction,
        "terms_text": terms,
        "consent_required": True
    }

@router.get("/consent-requirements")
async def get_consent_requirements(
    jurisdiction: str = "Malaysia"
):
    """Get required consents for jurisdiction"""
    
    consent_form = consent_manager.generate_consent_form(jurisdiction)
    
    return {
        "version": consent_manager.version,
        "jurisdiction": jurisdiction,
        "required_consents": [c for c in consent_form if c["required"]],
        "optional_consents": [c for c in consent_form if not c["required"]],
        "total_required": sum(1 for c in consent_form if c["required"])
    }

@router.get("/my-consents")
async def get_my_consents(
    current_user: User = Depends(get_current_user)
):
    """Get current user's consent records"""
    
    db = get_session()
    
    # Get all consent records
    consent_records = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == current_user.id
    ).order_by(ConsentRecord.given_at.desc()).all()
    
    # Group by consent type (latest only)
    latest_consents = {}
    for record in consent_records:
        if record.consent_type not in latest_consents:
            latest_consents[record.consent_type] = {
                "consent_given": record.consent_given,
                "given_at": record.given_at.isoformat() if record.given_at else None,
                "withdrawn_at": record.withdrawn_at.isoformat() if record.withdrawn_at else None,
                "version": record.consent_version
            }
    
    db.close()
    
    return {
        "user_id": current_user.id,
        "consent_version": current_user.consent_version,
        "consent_timestamp": current_user.consent_timestamp.isoformat(),
        "current_consents": latest_consents,
        "consent_valid": all(c.get("consent_given") for c in latest_consents.values())
    }

@router.post("/withdraw-consent")
async def withdraw_consent(
    consent_type: str,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Withdraw specific consent"""
    
    # Check if this is a required consent
    required_consents = [
        "data_collection", "commercial_use", "ai_training",
        "revenue_sharing", "attribution", "terms"
    ]
    
    if consent_type in required_consents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot withdraw required consent '{consent_type}'. This would require account closure."
        )
    
    db = get_session()
    
    # Create withdrawal record
    consent = ConsentRecord(
        id=f"CONSENT_{secrets.token_hex(8).upper()}",
        user_id=current_user.id,
        consent_type=consent_type,
        consent_given=False,
        consent_text=f"Withdrawal of {consent_type} consent",
        consent_version="2.0",
        consent_method="explicit_withdrawal",
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        withdrawn_at=datetime.utcnow()
    )
    
    db.add(consent)
    
    # Update user's consent record
    user = db.query(User).filter(User.id == current_user.id).first()
    consent_record = user.consent_record.copy()
    consent_record[consent_type] = False
    user.consent_record = consent_record
    
    # Log withdrawal
    log_audit(db, current_user.id, "CONSENT_WITHDRAWAL", "update",
             "consent", consent.id,
             {"consent_type": consent_type}, request)
    
    db.commit()
    db.close()
    
    return {
        "message": f"Consent '{consent_type}' withdrawn successfully",
        "withdrawn_at": datetime.utcnow().isoformat(),
        "implications": get_consent_implications(consent_type)
    }

@router.post("/data-export")
async def request_data_export(
    export_request: DataExportRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Export all user data (GDPR/PDPA compliance)"""
    
    db = get_session()
    
    # Generate export
    export_data = generate_data_export(
        current_user,
        db,
        export_request.export_format,
        export_request.include_wisdom_drops,
        export_request.include_revenue_records,
        export_request.include_audit_logs
    )
    
    # Log export request
    log_audit(db, current_user.id, "DATA_EXPORT", "access",
             "user_data", current_user.id,
             {"format": export_request.export_format}, request)
    
    db.commit()
    db.close()
    
    # Prepare response
    if export_request.export_format == "csv":
        return Response(
            content=export_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=ysense_data_export_{current_user.id}.csv"
            }
        )
    else:
        return Response(
            content=export_data,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=ysense_data_export_{current_user.id}.json"
            }
        )

@router.post("/data-deletion")
async def request_data_deletion(
    deletion_request: DataDeletionRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Request data deletion (right to be forgotten)"""
    
    if not deletion_request.confirm_deletion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please confirm deletion request"
        )
    
    db = get_session()
    
    # Anonymize user data
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if deletion_request.keep_published_wisdom:
        # Anonymize user but keep wisdom for attribution
        anonymization_data = anonymize_user_data(user)
        
        # Update wisdom drops with anonymized attribution
        wisdom_drops = db.query(WisdomDrop).filter(
            WisdomDrop.user_id == current_user.id,
            WisdomDrop.published == True
        ).all()
        
        for drop in wisdom_drops:
            drop.user_id = anonymization_data["anonymized_id"]
            drop.attribution_text = f"Wisdom by {anonymization_data['preserved_attribution']} (Anonymized)"
        
        # Mark user as deleted
        user.account_status = "deleted"
        user.email = f"deleted_{user.id}@deleted.com"
        user.username = f"deleted_{user.id}"
        
        message = "Account anonymized. Published wisdom retained for attribution."
    else:
        # Full deletion including wisdom
        db.query(WisdomDrop).filter(WisdomDrop.user_id == current_user.id).delete()
        
        # Mark user as deleted
        user.account_status = "deleted"
        user.email = f"deleted_{user.id}@deleted.com"
        user.username = f"deleted_{user.id}"
        
        message = "Account and all data marked for deletion."
    
    # Log deletion
    log_audit(db, current_user.id, "DATA_DELETION_REQUEST", "delete",
             "user", current_user.id,
             {"reason": deletion_request.reason,
              "keep_wisdom": deletion_request.keep_published_wisdom},
             request)
    
    db.commit()
    db.close()
    
    return {
        "message": message,
        "deletion_date": datetime.utcnow().isoformat(),
        "retention_notice": "Some data retained for legal compliance (7 years)"
    }

@router.get("/compliance-check")
async def check_compliance_status(
    current_user: User = Depends(get_current_user)
):
    """Check user's compliance status"""
    
    db = get_session()
    
    issues = []
    recommendations = []
    
    # Check consent validity
    consent_valid = all(
        current_user.consent_record.get(consent, False)
        for consent in ["data_collection", "commercial_use", "ai_training", 
                        "revenue_sharing", "attribution", "terms"]
    )
    
    if not consent_valid:
        issues.append("Missing required consents")
        recommendations.append("Review and accept all required consents")
    
    # Check age verification
    if not current_user.age_verified or current_user.age < 18:
        issues.append("Age verification incomplete or underage")
        recommendations.append("Complete age verification")
    
    # Check consent age
    consent_age = (datetime.utcnow() - current_user.consent_timestamp).days
    if consent_age > 365:
        recommendations.append("Consider reviewing consent (over 1 year old)")
    
    # Check data retention
    oldest_audit = db.query(AuditLog).filter(
        AuditLog.user_id == current_user.id
    ).order_by(AuditLog.created_at.asc()).first()
    
    if oldest_audit:
        retention_years = (datetime.utcnow() - oldest_audit.created_at).days / 365
        if retention_years > 7:
            issues.append("Audit data exceeds 7-year retention period")
            recommendations.append("Request audit data cleanup")
    
    db.close()
    
    return {
        "gdpr_compliant": len(issues) == 0 and current_user.jurisdiction == "EU",
        "pdpa_compliant": len(issues) == 0 and current_user.jurisdiction in ["Malaysia", "Singapore"],
        "consent_valid": consent_valid,
        "data_retention_compliant": "Audit data exceeds 7-year retention period" not in issues,
        "issues": issues,
        "recommendations": recommendations,
        "last_consent_update": current_user.consent_timestamp.isoformat(),
        "jurisdiction": current_user.jurisdiction
    }

@router.get("/audit-trail")
async def get_audit_trail(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    action_type: Optional[str] = None
):
    """Get user's audit trail"""
    
    db = get_session()
    
    query = db.query(AuditLog).filter(AuditLog.user_id == current_user.id)
    
    if action_type:
        query = query.filter(AuditLog.action_type == action_type)
    
    audit_logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    db.close()
    
    return {
        "total_records": len(audit_logs),
        "audit_trail": [
            {
                "id": log.id,
                "action": log.action,
                "action_type": log.action_type,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat()
            }
            for log in audit_logs
        ]
    }

def get_consent_implications(consent_type: str) -> List[str]:
    """Get implications of withdrawing consent"""
    
    implications = {
        "marketing": ["You will no longer receive marketing communications"],
        "research": ["Your data will not be used for academic research"],
        "community": ["You cannot participate in community features"]
    }
    
    return implications.get(consent_type, ["No specific implications"])
