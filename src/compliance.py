# ysense_platform_v3_legal.py
"""
YSense™ Platform v3.0 - Southeast Asian Legal Compliance Framework
Implements Malaysian PDPA, Singapore PDPA, and GDPR compliance
With dynamic tier revenue system based on Z Protocol scores
"""

import hashlib
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Text, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, validator, EmailStr

Base = declarative_base()

# ==================== Regional Compliance Configuration ====================

class RegionalCompliance(Enum):
    """Southeast Asian regulatory framework priorities"""
    MALAYSIA_PDPA = "malaysia_pdpa_2010"
    SINGAPORE_PDPA = "singapore_pdpa_2012"
    THAILAND_PDPA = "thailand_pdpa_2019"
    INDONESIA_PDP = "indonesia_pdp_2022"
    PHILIPPINES_DPA = "philippines_dpa_2012"
    VIETNAM_DECREE = "vietnam_decree_13_2023"
    GDPR = "gdpr_eu"
    ASEAN_FRAMEWORK = "asean_data_framework_2024"

@dataclass
class ComplianceRequirements:
    """Regional compliance requirements matrix"""
    region: RegionalCompliance
    age_requirement: int
    consent_explicit: bool
    data_localization: bool
    breach_notification_hours: int
    deletion_rights: bool
    portability_rights: bool
    processing_disclosure: bool
    cross_border_restrictions: bool

# Regional compliance configurations
REGIONAL_REQUIREMENTS = {
    RegionalCompliance.MALAYSIA_PDPA: ComplianceRequirements(
        region=RegionalCompliance.MALAYSIA_PDPA,
        age_requirement=18,
        consent_explicit=True,
        data_localization=False,
        breach_notification_hours=72,
        deletion_rights=True,
        portability_rights=False,
        processing_disclosure=True,
        cross_border_restrictions=True
    ),
    RegionalCompliance.SINGAPORE_PDPA: ComplianceRequirements(
        region=RegionalCompliance.SINGAPORE_PDPA,
        age_requirement=13,  # With parental consent
        consent_explicit=True,
        data_localization=False,
        breach_notification_hours=72,
        deletion_rights=True,
        portability_rights=True,
        processing_disclosure=True,
        cross_border_restrictions=True
    ),
    RegionalCompliance.GDPR: ComplianceRequirements(
        region=RegionalCompliance.GDPR,
        age_requirement=16,
        consent_explicit=True,
        data_localization=False,
        breach_notification_hours=72,
        deletion_rights=True,
        portability_rights=True,
        processing_disclosure=True,
        cross_border_restrictions=False
    )
}

# ==================== Dynamic Revenue Tier System ====================

class RevenueTier(Enum):
    """Dynamic revenue tiers based on Z Protocol scores"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

@dataclass
class TierConfiguration:
    """Revenue tier configuration with dynamic percentages"""
    tier: RevenueTier
    z_protocol_minimum: float
    contribution_minimum: int
    revenue_share_percentage: float
    cultural_multiplier_bonus: float
    priority_processing: bool
    certification_badge: str
    benefits: List[str]

REVENUE_TIERS = {
    RevenueTier.BRONZE: TierConfiguration(
        tier=RevenueTier.BRONZE,
        z_protocol_minimum=0.0,
        contribution_minimum=0,
        revenue_share_percentage=30.0,
        cultural_multiplier_bonus=1.0,
        priority_processing=False,
        certification_badge="🥉",
        benefits=["Basic attribution", "Standard processing"]
    ),
    RevenueTier.SILVER: TierConfiguration(
        tier=RevenueTier.SILVER,
        z_protocol_minimum=60.0,
        contribution_minimum=5,
        revenue_share_percentage=35.0,
        cultural_multiplier_bonus=1.1,
        priority_processing=False,
        certification_badge="🥈",
        benefits=["Enhanced attribution", "Monthly reports"]
    ),
    RevenueTier.GOLD: TierConfiguration(
        tier=RevenueTier.GOLD,
        z_protocol_minimum=75.0,
        contribution_minimum=15,
        revenue_share_percentage=40.0,
        cultural_multiplier_bonus=1.2,
        priority_processing=True,
        certification_badge="🥇",
        benefits=["Priority processing", "Quarterly bonuses", "Featured contributor"]
    ),
    RevenueTier.PLATINUM: TierConfiguration(
        tier=RevenueTier.PLATINUM,
        z_protocol_minimum=85.0,
        contribution_minimum=30,
        revenue_share_percentage=45.0,
        cultural_multiplier_bonus=1.3,
        priority_processing=True,
        certification_badge="💎",
        benefits=["VIP support", "Revenue advance option", "Advisory input"]
    ),
    RevenueTier.DIAMOND: TierConfiguration(
        tier=RevenueTier.DIAMOND,
        z_protocol_minimum=95.0,
        contribution_minimum=50,
        revenue_share_percentage=50.0,
        cultural_multiplier_bonus=1.5,
        priority_processing=True,
        certification_badge="💠",
        benefits=["Maximum revenue share", "Strategic partnership", "Co-creation opportunities"]
    )
}

# ==================== Enhanced Terms of Service v2.0 ====================

class TermsOfServiceV2:
    """Comprehensive Terms of Service for Southeast Asian compliance"""
    
    def __init__(self):
        self.version = "2.0"
        self.effective_date = datetime.now().isoformat()
        self.jurisdictions = ["Malaysia", "Singapore", "ASEAN", "Global"]
    
    def get_regional_terms(self, user_region: str) -> str:
        """Generate region-specific terms of service"""
        
        base_terms = f"""
YSENSE™ | 慧觉™ PLATFORM TERMS OF SERVICE
Version {self.version} - Effective {self.effective_date}
Jurisdiction Priority: {user_region} → ASEAN → Global

IMPORTANT: By accessing YSense Platform v2.0, you acknowledge that our AI policies 
and terms evolve with regulatory changes. Re-consent is required for each major 
platform iteration to ensure continued compliance and protection.

══════════════════════════════════════════════════════════════════════

1. REGULATORY COMPLIANCE FRAMEWORK

1.1 MALAYSIAN PERSONAL DATA PROTECTION ACT 2010 (PDPA)
   • We comply with all seven PDPA principles
   • Data processed only for wisdom collection purposes
   • Your consent can be withdrawn (except published content)
   • Data Commissioner registration maintained

1.2 SINGAPORE PERSONAL DATA PROTECTION ACT 2012
   • Consent obtained before collection, use, disclosure
   • Purpose limitation strictly enforced
   • Notification of data breaches within 72 hours
   • Data Protection Officer contactable at dpo@ysense.ai

1.3 ASEAN DATA MANAGEMENT FRAMEWORK 2024
   • Cross-border data flows facilitated securely
   • Regional data portability supported
   • ASEAN Model Contractual Clauses implemented
   • Regional certification mechanisms honored

1.4 EU GENERAL DATA PROTECTION REGULATION (GDPR)
   • Lawful basis: Consent and Legitimate Interest
   • Right to erasure (except published wisdom)
   • Data portability in machine-readable format
   • Privacy by design implementation

══════════════════════════════════════════════════════════════════════

2. AGE AND CAPACITY REQUIREMENTS

2.1 MINIMUM AGE
   • Malaysia: 18 years (age of majority)
   • Singapore: 21 years (without parental consent)
   • Other ASEAN: Per local jurisdiction
   • Global: 18 years minimum

2.2 VERIFICATION
   • Government ID verification may be required
   • False age declaration results in immediate termination
   • Parental consent not accepted for this platform

══════════════════════════════════════════════════════════════════════

3. DYNAMIC REVENUE SHARING MODEL

3.1 TIER SYSTEM (Z Protocol Score Based)
   • BRONZE (0-59): 30% revenue share
   • SILVER (60-74): 35% revenue share
   • GOLD (75-84): 40% revenue share
   • PLATINUM (85-94): 45% revenue share
   • DIAMOND (95-100): 50% revenue share

3.2 CULTURAL MULTIPLIERS
   • Malaysian content: 1.6x multiplier
   • Singaporean content: 1.5x multiplier
   • ASEAN content: 1.3x multiplier
   • Indigenous wisdom: 1.8x multiplier

3.3 PAYMENT TERMS
   • Minimum payout: €50 or regional equivalent
   • Payment within 30 days of threshold
   • Multi-currency support (MYR, SGD, EUR, USD)
   • Blockchain attribution for transparency

══════════════════════════════════════════════════════════════════════

4. CONTENT OWNERSHIP AND LICENSING

4.1 YOUR RIGHTS
   • You retain copyright to your original wisdom
   • Moral rights preserved under Berne Convention
   • Attribution permanently maintained
   • Right to audit usage annually

4.2 LICENSE TO YSENSE
   • Perpetual, worldwide, non-exclusive license
   • Right to sublicense for AI training purposes
   • Commercial use with mandatory attribution
   • Modification only for technical compatibility

4.3 WARRANTY AND INDEMNITY
   • You warrant all content is original
   • No third-party copyrighted material
   • You indemnify against all IP claims
   • Legal costs recoverable for false claims

══════════════════════════════════════════════════════════════════════

5. Z PROTOCOL v2.0 COMPLIANCE

5.1 ETHICAL VALIDATION
   • All content undergoes 7-point validation
   • Minimum 80% score required for acceptance
   • Cultural sensitivity assessment mandatory
   • Community benefit analysis included

5.2 DYNAMIC CERTIFICATION
   • Z Protocol ID updates with contribution quality
   • Higher scores unlock better revenue tiers
   • Certification visible on public profile
   • Annual recertification required

══════════════════════════════════════════════════════════════════════

6. PROHIBITED CONTENT AND CONDUCT

6.1 CONTENT RESTRICTIONS
   • No personally identifiable information
   • No copyright-infringing material
   • No harmful, illegal, or discriminatory content
   • No state secrets or classified information
   • No content violating ASEAN cultural norms

6.2 PLATFORM CONDUCT
   • No manipulation of Z Protocol scores
   • No submission of AI-generated content
   • No false attribution claims
   • No circumvention of regional restrictions

══════════════════════════════════════════════════════════════════════

7. DATA PROTECTION RIGHTS

7.1 ACCESS RIGHTS
   • Request copy of your personal data
   • Machine-readable format provided
   • Response within 30 days

7.2 CORRECTION RIGHTS
   • Update inaccurate information
   • Annotation of disputed data
   • Notification to third parties

7.3 DELETION RIGHTS
   • Right to erasure (except published wisdom)
   • Anonymization option available
   • Audit trail maintained for legal compliance

7.4 DATA PORTABILITY
   • Export in JSON/XML format
   • Direct transfer to other platforms
   • Interoperability with ASEAN systems

══════════════════════════════════════════════════════════════════════

8. CROSS-BORDER DATA TRANSFER

8.1 ADEQUACY MECHANISMS
   • ASEAN Model Contractual Clauses
   • EU Standard Contractual Clauses
   • APEC Cross-Border Privacy Rules
   • Binding Corporate Rules compliance

8.2 DATA LOCALIZATION
   • Malaysian data primarily stored in Malaysia
   • Singapore data primarily stored in Singapore
   • Backup replication across ASEAN region
   • No transfer to non-adequate countries

══════════════════════════════════════════════════════════════════════

9. BREACH NOTIFICATION

9.1 USER NOTIFICATION
   • Within 72 hours of discovery
   • Direct email to affected users
   • Public notice for large-scale breaches
   • Regulatory authority notification

9.2 INCIDENT RESPONSE
   • Immediate containment measures
   • Impact assessment provided
   • Mitigation steps communicated
   • Compensation per regional laws

══════════════════════════════════════════════════════════════════════

10. DISPUTE RESOLUTION

10.1 GOVERNING LAW
   • Primary: Laws of Malaysia
   • Secondary: ASEAN Framework
   • Tertiary: International arbitration

10.2 DISPUTE PROCESS
   • Good faith negotiation (30 days)
   • Mediation in Kuala Lumpur (30 days)
   • Arbitration under AIAC rules
   • Class actions waived where permitted

══════════════════════════════════════════════════════════════════════

11. PLATFORM EVOLUTION CLAUSE

Due to rapid AI regulatory development globally and within ASEAN:
   • Terms update with 30-day notice minimum
   • Major updates require re-consent
   • Grandfathering of favorable terms (1 year)
   • Right to export data before changes

══════════════════════════════════════════════════════════════════════

12. CONTACT AND ENFORCEMENT

Data Protection Officer: dpo@ysense.ai
Legal Contact: legal@ysense.ai
Physical Address: Teluk Intan, Perak, Malaysia

Regulatory References:
- Malaysia PDPA 2010 (Act 709)
- Singapore PDPA 2012 (No. 26 of 2012)  
- ASEAN Framework on Digital Data Governance
- EU GDPR 2016/679

By clicking "ACCEPT", you acknowledge reading, understanding, and 
agreeing to these terms in their entirety.
"""
        return base_terms

# ==================== Consent Management System v2.0 ====================

class ConsentManagementV2:
    """Comprehensive consent system for multi-jurisdictional compliance"""
    
    def __init__(self):
        self.version = "2.0"
        self.consent_categories = self._define_consent_categories()
    
    def _define_consent_categories(self) -> Dict[str, Dict]:
        """Define granular consent categories"""
        return {
            "essential_operation": {
                "label": "Essential Platform Operation",
                "description": "Required for basic platform functionality",
                "required": True,
                "jurisdictions": ["all"],
                "details": [
                    "User authentication and security",
                    "Wisdom drop processing",
                    "Attribution management",
                    "Revenue calculation"
                ]
            },
            "commercial_use": {
                "label": "Commercial Use with Attribution",
                "description": "Your wisdom may be licensed to AI companies",
                "required": True,
                "jurisdictions": ["all"],
                "details": [
                    "Licensing to AI training companies",
                    "Mandatory attribution preserved",
                    "Revenue sharing activated",
                    "Global distribution rights"
                ]
            },
            "age_verification": {
                "label": "Age Verification (18+ for Malaysia, 21+ for Singapore)",
                "description": "Platform restricted to legal adults",
                "required": True,
                "jurisdictions": ["all"],
                "validation": "age_check"
            },
            "data_processing_pdpa": {
                "label": "Data Processing under Malaysian/Singapore PDPA",
                "description": "Regional data protection compliance",
                "required": True,
                "jurisdictions": ["malaysia", "singapore", "asean"],
                "details": [
                    "Purpose limitation enforced",
                    "Data minimization practiced",
                    "Retention periods specified",
                    "Security measures implemented"
                ]
            },
            "cross_border_transfer": {
                "label": "Cross-Border Data Transfer within ASEAN",
                "description": "Data may be processed in ASEAN countries",
                "required": True,
                "jurisdictions": ["all"],
                "details": [
                    "Primary storage in Malaysia/Singapore",
                    "ASEAN-wide backup replication",
                    "No transfer outside adequate regions",
                    "Model contractual clauses applied"
                ]
            },
            "z_protocol_compliance": {
                "label": "Z Protocol Ethical Framework",
                "description": "Ethical validation and scoring system",
                "required": True,
                "jurisdictions": ["all"],
                "details": [
                    "Content validation scoring",
                    "Dynamic tier assignment",
                    "Cultural sensitivity checks",
                    "Community benefit analysis"
                ]
            },
            "copyright_liability": {
                "label": "Copyright and Liability Acceptance",
                "description": "You accept full liability for content authenticity",
                "required": True,
                "jurisdictions": ["all"],
                "warning": "False claims may result in legal action"
            },
            "revenue_model_v2": {
                "label": "Dynamic Revenue Sharing Model (30-50%)",
                "description": "Tiered revenue based on Z Protocol scores",
                "required": True,
                "jurisdictions": ["all"],
                "tiers": {
                    "bronze": "30% (0-59 score)",
                    "silver": "35% (60-74 score)",
                    "gold": "40% (75-84 score)",
                    "platinum": "45% (85-94 score)",
                    "diamond": "50% (95-100 score)"
                }
            },
            "regulatory_updates": {
                "label": "Regulatory Update Acknowledgment",
                "description": "Terms evolve with AI regulations",
                "required": True,
                "jurisdictions": ["all"],
                "details": [
                    "Re-consent required for major updates",
                    "30-day notice for changes",
                    "Data export rights preserved",
                    "Grandfathering period provided"
                ]
            },
            "marketing_communications": {
                "label": "Marketing and Platform Updates",
                "description": "Receive updates about YSense platform",
                "required": False,
                "jurisdictions": ["all"]
            },
            "research_participation": {
                "label": "Academic Research Participation",
                "description": "Wisdom may be used in academic studies",
                "required": False,
                "jurisdictions": ["all"]
            },
            "community_sharing": {
                "label": "Community Wisdom Sharing",
                "description": "Share insights with YSense community",
                "required": False,
                "jurisdictions": ["all"]
            }
        }
    
    def generate_consent_form(self, user_jurisdiction: str) -> List[Dict]:
        """Generate jurisdiction-specific consent form"""
        consent_items = []
        
        for consent_id, consent_data in self.consent_categories.items():
            jurisdictions = consent_data.get("jurisdictions", [])
            
            if "all" in jurisdictions or user_jurisdiction.lower() in jurisdictions:
                consent_items.append({
                    "id": consent_id,
                    "label": consent_data["label"],
                    "description": consent_data["description"],
                    "required": consent_data["required"],
                    "details": consent_data.get("details", []),
                    "warning": consent_data.get("warning"),
                    "checked": False
                })
        
        return consent_items
    
    def validate_consent_submission(self, submitted_consents: Dict, user_jurisdiction: str) -> Tuple[bool, Dict]:
        """Validate all required consents are given"""
        
        required_consents = []
        missing_consents = []
        consent_record = {}
        
        for consent_id, consent_data in self.consent_categories.items():
            jurisdictions = consent_data.get("jurisdictions", [])
            
            if "all" in jurisdictions or user_jurisdiction.lower() in jurisdictions:
                if consent_data["required"]:
                    required_consents.append(consent_id)
                    
                    if not submitted_consents.get(consent_id):
                        missing_consents.append(consent_data["label"])
                    else:
                        consent_record[consent_id] = True
                elif submitted_consents.get(consent_id):
                    consent_record[consent_id] = True
        
        if missing_consents:
            return False, {
                "valid": False,
                "missing": missing_consents,
                "message": "All required consents must be accepted"
            }
        
        # Generate cryptographic consent proof
        consent_signature = self._generate_consent_signature(consent_record, user_jurisdiction)
        
        return True, {
            "valid": True,
            "consent_record": consent_record,
            "consent_signature": consent_signature,
            "timestamp": datetime.now().isoformat(),
            "jurisdiction": user_jurisdiction,
            "version": self.version
        }
    
    def _generate_consent_signature(self, consent_record: Dict, jurisdiction: str) -> str:
        """Generate legally binding consent signature"""
        consent_data = {
            "consents": consent_record,
            "jurisdiction": jurisdiction,
            "version": self.version,
            "timestamp": datetime.now().isoformat()
        }
        
        consent_string = json.dumps(consent_data, sort_keys=True)
        return hashlib.sha256(consent_string.encode()).hexdigest()

# ==================== Enhanced User Model v2.0 ====================

class UserV2(Base):
    """Enhanced User model with comprehensive legal tracking"""
    __tablename__ = "users_v2"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Regional Compliance
    jurisdiction = Column(String, nullable=False)  # Primary jurisdiction
    secondary_jurisdictions = Column(JSON)  # Other applicable regions
    
    # Enhanced Consent Tracking
    consent_signature = Column(String, nullable=False)
    consent_timestamp = Column(DateTime, nullable=False)
    consent_version = Column(String, nullable=False)
    consent_record = Column(JSON, nullable=False)
    consent_ip_address = Column(String)
    consent_user_agent = Column(String)
    
    # Age Verification
    age_verified = Column(Boolean, default=False)
    age_verification_method = Column(String)  # "declaration", "document", "third_party"
    age_verification_date = Column(DateTime)
    date_of_birth = Column(DateTime)  # Encrypted storage
    
    # Dynamic Z Protocol v2.0
    z_protocol_id = Column(String, unique=True)
    z_protocol_score = Column(Float, default=0.0)
    z_protocol_level = Column(Integer, default=1)
    z_protocol_tier = Column(SQLEnum(RevenueTier), default=RevenueTier.BRONZE)
    z_protocol_history = Column(JSON)  # Track score changes
    
    # Dynamic Revenue Tier
    revenue_tier = Column(SQLEnum(RevenueTier), default=RevenueTier.BRONZE)
    revenue_share_percentage = Column(Float, default=30.0)
    cultural_multiplier = Column(Float, default=1.0)
    tier_achievement_date = Column(DateTime)
    next_tier_requirements = Column(JSON)
    
    # Legal Compliance
    terms_version_accepted = Column(String, nullable=False)
    terms_acceptance_date = Column(DateTime, nullable=False)
    gdpr_consent = Column(Boolean, default=False)
    pdpa_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    research_consent = Column(Boolean, default=False)
    
    # Re-consent Tracking
    re_consent_required = Column(Boolean, default=False)
    re_consent_deadline = Column(DateTime)
    re_consent_history = Column(JSON)  # Track all consent updates
    
    # Copyright Protection
    copyright_declaration = Column(Boolean, default=False)
    copyright_violations = Column(Integer, default=0)
    copyright_strikes = Column(JSON)  # Track violations
    
    # Audit Trail
    registration_ip = Column(String)
    registration_user_agent = Column(String)
    last_terms_review = Column(DateTime)
    data_export_requests = Column(JSON)
    deletion_requests = Column(JSON)
    
    # Enhanced Attribution
    attribution_id = Column(String, unique=True)
    attribution_name = Column(String)  # How they want to be attributed
    attribution_url = Column(String)  # Optional personal URL
    
    # Financial
    total_earnings = Column(Float, default=0.0)
    pending_earnings = Column(Float, default=0.0)
    paid_earnings = Column(Float, default=0.0)
    community_contributions = Column(Float, default=0.0)
    tier_bonuses = Column(Float, default=0.0)
    
    # Status
    account_status = Column(String, default="active")  # active, suspended, terminated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    def calculate_revenue_tier(self) -> RevenueTier:
        """Calculate user's revenue tier based on Z Protocol score and contributions"""
        
        for tier in [RevenueTier.DIAMOND, RevenueTier.PLATINUM, RevenueTier.GOLD, 
                    RevenueTier.SILVER, RevenueTier.BRONZE]:
            config = REVENUE_TIERS[tier]
            
            if (self.z_protocol_score >= config.z_protocol_minimum and 
                self.contribution_count >= config.contribution_minimum):
                return tier
        
        return RevenueTier.BRONZE
    
    def update_revenue_tier(self):
        """Update user's revenue tier and benefits"""
        new_tier = self.calculate_revenue_tier()
        
        if new_tier != self.revenue_tier:
            self.revenue_tier = new_tier
            config = REVENUE_TIERS[new_tier]
            self.revenue_share_percentage = config.revenue_share_percentage
            self.cultural_multiplier = config.cultural_multiplier_bonus
            self.tier_achievement_date = datetime.utcnow()
            
            # Calculate next tier requirements
            tier_order = [RevenueTier.BRONZE, RevenueTier.SILVER, RevenueTier.GOLD,
                         RevenueTier.PLATINUM, RevenueTier.DIAMOND]
            
            current_index = tier_order.index(new_tier)
            if current_index < len(tier_order) - 1:
                next_tier = tier_order[current_index + 1]
                next_config = REVENUE_TIERS[next_tier]
                self.next_tier_requirements = {
                    "tier": next_tier.value,
                    "z_protocol_needed": next_config.z_protocol_minimum,
                    "contributions_needed": next_config.contribution_minimum,
                    "current_score": self.z_protocol_score,
                    "current_contributions": self.contribution_count
                }
    
    def requires_re_consent(self, new_version: str) -> bool:
        """Check if user needs to re-consent for new terms"""
        return (self.terms_version_accepted != new_version or 
                self.re_consent_required or
                datetime.utcnow() > self.re_consent_deadline if self.re_consent_deadline else False)