# src/terms_consent_system.py
"""
YSense™ Platform v4.1 - Complete Terms of Service & Consent Management
Z Protocol v2.0 Compliant Legal Framework
"""

from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import json

class TermsConsentSystem:
    """Complete terms of service and consent management system"""
    
    def __init__(self):
        self.version = "4.1"
        self.effective_date = "2025-09-28"
        self.z_protocol_version = "2.0"
        
    def get_terms(self) -> str:
        """Get terms of service (alias for compatibility)"""
        return self.get_complete_terms_of_service()
    
    def get_complete_terms_of_service(self) -> str:
        """Complete Terms of Service for YSense Platform v4.1"""
        return f"""
YSENSE™ PLATFORM TERMS OF SERVICE
Version {self.version} - Effective Date: {self.effective_date}
Z Protocol v{self.z_protocol_version} Compliant

🎯 REVOLUTIONARY AI ATTRIBUTION PLATFORM
YSense is the world's first platform ensuring permanent attribution and fair revenue sharing for human wisdom used in AI training.

═══════════════════════════════════════════════════════════════

1. ELIGIBILITY & REGISTRATION
   ✓ Must be 18+ years old (government ID verification required)
   ✓ Legal capacity to enter binding agreements
   ✓ Not prohibited from using this service in your jurisdiction
   ✓ One account per person (identity verification prevents duplicates)

2. YOUR WISDOM CONTRIBUTIONS - ORIGINAL CONTENT ONLY
   🚨 CRITICAL: All content must be YOUR original creation
   
   ✓ YOU WARRANT: No copyrighted material included
   ✓ YOU WARRANT: No plagiarized or stolen content
   ✓ YOU WARRANT: You have full rights to submit this wisdom
   ✓ YOU GRANT: Perpetual, worldwide, non-exclusive license to YSense
   ✓ GUARANTEED: Attribution will ALWAYS be maintained

3. COPYRIGHT FRAUD LIABILITY - YOU ARE RESPONSIBLE
   🚨 WARNING: You are SOLELY liable for copyright violations
   
   • You indemnify YSense against ALL legal claims
   • Fraudulent submissions = immediate account termination
   • Legal action will be pursued for copyright fraud
   • Personal liability for all damages and legal fees

4. REVENUE SHARING MODELS - 100% TRANSPARENT
   
   🏆 FOUNDING CONTRIBUTOR (First 100 users): 100% revenue share
   • Zero platform fees - you keep everything
   • Guaranteed €100/month minimum after 6 months
   • Lifetime founding status with voting rights
   
   🤝 FOUNDING PARTNERSHIP (First 500 users): 70% + equity
   • Partnership agreement with institutional benefits
   • Co-marketing and research collaboration opportunities
   
   💻 FOUNDING DEVELOPER: 50% + platform tokens
   • Technical contribution rewards and API access
   
   🌍 CULTURAL GUARDIAN: 60% + community fund
   • Cultural preservation mandate and advisory role
   
   ⭐ STANDARD TIERS:
   • Gold: 40% revenue share
   • Silver: 30% revenue share  
   • Bronze: 20% revenue share
   • Community: 10% revenue share

5. CULTURAL MULTIPLIERS - BONUS REVENUE
   • Indigenous Knowledge: 200% multiplier
   • Traditional Wisdom: 180% multiplier
   • Cultural Heritage: 160% multiplier
   • Regional Expertise: 140% multiplier
   • Linguistic Diversity: 130% multiplier

6. PAYMENT TERMS
   • Monthly payments after €50 minimum threshold
   • Detailed revenue tracking dashboard provided
   • No hidden fees or surprise deductions
   • Cultural and quality bonuses clearly calculated

7. Z PROTOCOL v2.0 ETHICAL COMPLIANCE
   🛡️ All wisdom undergoes comprehensive ethical validation:
   
   ✓ Consent Validation (25% of score)
   ✓ Attribution Chain (20% of score)
   ✓ Authenticity Verification (15% of score)
   ✓ Dignity Preservation (15% of score)
   ✓ Transparency Requirements (10% of score)
   ✓ Legal Compliance (10% of score)
   ✓ Audit Trail (5% of score)
   
   • Minimum 80% compliance score required
   • Failed validations = submission rejected
   • Multiple violations = account suspension

8. DATA PROTECTION - GDPR/PDPA COMPLIANT
   ✓ You have the right to access your data
   ✓ You have the right to correct inaccurate data
   ✓ You have the right to delete your account
   ✓ Published wisdom remains licensed (cannot be deleted)
   ✓ Attribution remains permanent and immutable
   ✓ Audit trail maintained for 7 years

9. PROHIBITED CONTENT - ZERO TOLERANCE
   🚫 Personal identifying information (names, addresses, emails)
   🚫 Harmful, illegal, or discriminatory content
   🚫 Hate speech or harassment
   🚫 Private information about others
   🚫 Medical advice or dangerous instructions
   🚫 Copyrighted material without permission

10. WISDOM LIBRARY & ATTRIBUTION ENGINE
    • Public wisdom available for community discovery
    • Attribution documents generated for all usage
    • Download tracking and revenue calculation
    • Cultural preservation and research priority

11. DEFENSIVE PUBLICATION PROTECTION
    • Your wisdom protected from patent theft
    • Prior art establishment for legal protection
    • Permanent record of your contributions
    • Legal standing in intellectual property disputes

12. PLATFORM MODIFICATIONS
    • 30 days notice for terms changes
    • Continued use implies acceptance
    • Major changes require explicit consent
    • Founding contributors have voting rights

13. ACCOUNT TERMINATION
    • You may delete your account anytime
    • Published wisdom remains licensed
    • Attribution remains permanent
    • Revenue sharing continues for existing licenses

14. DISPUTE RESOLUTION
    • Good faith negotiation required first
    • Mediation through agreed arbitrator
    • Malaysian law governs (Teluk Intan jurisdiction)
    • Founding contributors have special dispute process

15. LIMITATION OF LIABILITY
    • Platform provided "as is" without warranties
    • YSense not liable for content accuracy
    • Maximum liability limited to revenue earned
    • Force majeure events excluded

═══════════════════════════════════════════════════════════════

🎯 FOUNDING CONTRIBUTOR EXCLUSIVE BENEFITS
If you qualify as a Founding Contributor (first 100 users):

✓ 100% revenue share (zero platform fees)
✓ Guaranteed minimum €100/month after 6 months
✓ Lifetime founding status
✓ Platform governance voting rights
✓ Priority customer support
✓ Beta access to all new features
✓ Annual founder's meeting invitation
✓ Direct leadership communication channel

BY CLICKING "I ACCEPT THESE TERMS":
• You confirm you have READ and UNDERSTOOD all terms
• You ACCEPT full responsibility for your content authenticity
• You CONSENT to commercial use with permanent attribution
• You ACKNOWLEDGE copyright fraud liability
• You AGREE to Z Protocol v2.0 ethical validation
• You COMMIT to building ethical AI through human wisdom

═══════════════════════════════════════════════════════════════

This agreement represents a revolutionary approach to ethical AI development.
Your wisdom matters. Your attribution is permanent. Your revenue is guaranteed.

Join us in building the future of human-AI collaboration! 🚀
"""

    def get_required_consents(self) -> Dict[str, Dict]:
        """Get all required consent checkboxes with detailed descriptions"""
        return {
            "terms_acceptance": {
                "label": "✅ I have read and accept the complete Terms of Service",
                "required": True,
                "description": "You must accept all terms to proceed with registration",
                "legal_weight": "BINDING_AGREEMENT"
            },
            
            "age_verification": {
                "label": "✅ I confirm I am 18 years or older",
                "required": True,
                "description": "Platform restricted to adults only - ID verification required",
                "legal_weight": "ELIGIBILITY_REQUIREMENT"
            },
            
            "original_content_warranty": {
                "label": "✅ I warrant all my content will be original and not copyrighted",
                "required": True,
                "description": "You are legally liable for any copyright violations",
                "legal_weight": "LIABILITY_ACCEPTANCE"
            },
            
            "commercial_use_consent": {
                "label": "✅ I consent to commercial use of my wisdom with permanent attribution",
                "required": True,
                "description": "Your wisdom may be licensed to AI companies with attribution",
                "legal_weight": "COMMERCIAL_LICENSE"
            },
            
            "revenue_sharing_acceptance": {
                "label": "✅ I accept the transparent revenue sharing model",
                "required": True,
                "description": "Revenue share based on your contributor tier",
                "legal_weight": "FINANCIAL_AGREEMENT"
            },
            
            "z_protocol_compliance": {
                "label": "✅ I consent to Z Protocol v2.0 ethical validation",
                "required": True,
                "description": "All wisdom undergoes ethical AI compliance validation",
                "legal_weight": "ETHICAL_COMPLIANCE"
            },
            
            "attribution_permanence": {
                "label": "✅ I understand attribution will be permanent and immutable",
                "required": True,
                "description": "Your name/ID will always be linked to your wisdom",
                "legal_weight": "ATTRIBUTION_CONSENT"
            },
            
            "data_processing_gdpr": {
                "label": "✅ I consent to data processing per GDPR/PDPA regulations",
                "required": True,
                "description": "Required for platform operation and revenue distribution",
                "legal_weight": "DATA_PROCESSING"
            },
            
            "copyright_fraud_liability": {
                "label": "✅ I accept full liability for copyright fraud and will indemnify YSense",
                "required": True,
                "description": "You are responsible for any legal claims from copyright violations",
                "legal_weight": "INDEMNIFICATION"
            },
            
            "wisdom_library_participation": {
                "label": "✅ I consent to wisdom library participation and public discovery",
                "required": True,
                "description": "Your public wisdom can be discovered and attributed to others",
                "legal_weight": "PLATFORM_PARTICIPATION"
            },
            
            # Optional consents
            "marketing_communications": {
                "label": "📧 I agree to receive marketing communications (Optional)",
                "required": False,
                "description": "Platform updates, new features, and partnership opportunities",
                "legal_weight": "MARKETING_CONSENT"
            },
            
            "research_participation": {
                "label": "🔬 I consent to academic research participation (Optional)",
                "required": False,
                "description": "Your wisdom may be used in academic research with attribution",
                "legal_weight": "RESEARCH_CONSENT"
            },
            
            "founding_contributor_interest": {
                "label": "🏆 I am interested in Founding Contributor status (if eligible)",
                "required": False,
                "description": "100% revenue share for first 100 qualified users",
                "legal_weight": "TIER_SELECTION"
            }
        }

    def validate_all_consents(self, consent_data: Dict) -> Dict:
        """Validate all required consents are properly given"""
        required_consents = self.get_required_consents()
        missing_required = []
        consent_summary = {
            "required_consents": {},
            "optional_consents": {},
            "missing_required": [],
            "legal_weight_summary": {}
        }
        
        for consent_id, consent_info in required_consents.items():
            is_given = consent_data.get(consent_id, False)
            
            if consent_info["required"]:
                consent_summary["required_consents"][consent_id] = is_given
                if not is_given:
                    missing_required.append(consent_info["label"])
            else:
                consent_summary["optional_consents"][consent_id] = is_given
            
            # Track legal weight
            legal_weight = consent_info["legal_weight"]
            if legal_weight not in consent_summary["legal_weight_summary"]:
                consent_summary["legal_weight_summary"][legal_weight] = []
            consent_summary["legal_weight_summary"][legal_weight].append({
                "consent_id": consent_id,
                "given": is_given,
                "required": consent_info["required"]
            })
        
        consent_summary["missing_required"] = missing_required
        
        if missing_required:
            return {
                "valid": False,
                "consent_summary": consent_summary,
                "message": f"Missing required consents: {', '.join(missing_required)}",
                "action_required": "Please accept all required consents to proceed"
            }
        
        # Generate consent signature for legal proof
        consent_signature = self.generate_consent_signature(consent_data)
        
        return {
            "valid": True,
            "consent_summary": consent_summary,
            "consent_signature": consent_signature,
            "timestamp": datetime.now().isoformat(),
            "z_protocol_version": self.z_protocol_version,
            "terms_version": self.version,
            "legal_status": "BINDING_AGREEMENT_EXECUTED"
        }

    def generate_consent_signature(self, consent_data: Dict) -> str:
        """Generate cryptographic proof of consent for legal purposes"""
        consent_record = {
            "consents": consent_data,
            "timestamp": datetime.now().isoformat(),
            "terms_version": self.version,
            "z_protocol_version": self.z_protocol_version,
            "ip_address": "recorded_separately",  # Would be filled by API
            "user_agent": "recorded_separately"   # Would be filled by API
        }
        
        consent_string = json.dumps(consent_record, sort_keys=True)
        return hashlib.sha256(consent_string.encode()).hexdigest()

    def get_contribution_agreement(self) -> str:
        """Agreement shown before each wisdom contribution"""
        return """
🎯 WISDOM CONTRIBUTION AGREEMENT
Z Protocol v2.0 Ethical Validation

Before submitting your wisdom, please confirm:

✅ AUTHENTICITY DECLARATION
   • This is MY original thought, experience, or insight
   • No copyrighted content is included
   • I have not plagiarized or stolen this content
   • I accept full liability for authenticity claims

✅ COMMERCIAL USE CONSENT
   • I consent to commercial licensing with attribution
   • I accept revenue sharing per my contributor tier
   • Attribution will be permanent and immutable
   • I understand this may be used for AI training

✅ ETHICAL STANDARDS
   • Content respects human dignity and privacy
   • No personal identifying information included
   • Culturally sensitive and appropriate
   • Complies with Z Protocol v2.0 standards

✅ LEGAL ACKNOWLEDGMENT
   • I am liable for any copyright violations
   • I indemnify YSense against legal claims
   • I accept Z Protocol ethical validation
   • Fraudulent content results in account termination

⚠️ WARNING: Copyright fraud consequences:
• Immediate account termination
• Legal action and personal liability
• Responsibility for all damages and legal fees
• Permanent ban from platform

🏆 FOUNDING CONTRIBUTOR REMINDER:
If you're a Founding Contributor, you receive 100% revenue share from this wisdom with full attribution protection!

By clicking "Submit Wisdom", I confirm all above declarations.
"""

    def get_privacy_policy_summary(self) -> str:
        """GDPR/PDPA compliant privacy policy summary"""
        return """
🛡️ PRIVACY POLICY SUMMARY
GDPR/PDPA Compliant Data Processing

DATA WE COLLECT:
• Registration information (name, email, location)
• Wisdom contributions and metadata
• Usage analytics and platform interactions
• Payment information for revenue sharing
• Identity verification documents (if required)

HOW WE USE YOUR DATA:
• Platform operation and wisdom attribution
• Revenue calculation and distribution
• Z Protocol v2.0 ethical validation
• Legal compliance and audit trails
• Communication about your account

YOUR RIGHTS:
✓ Access: View all data we have about you
✓ Correction: Fix any inaccurate information
✓ Deletion: Delete your account (except published wisdom)
✓ Portability: Export your data in JSON format
✓ Restriction: Limit how we process your data

DATA SHARING:
• Attribution information shared with wisdom users
• Revenue data shared with payment processors
• Legal compliance data shared with authorities if required
• Research data shared with academic partners (anonymized)

DATA RETENTION:
• Account data: Until deletion requested
• Published wisdom: Permanent (for attribution)
• Audit trails: 7 years (legal requirement)
• Payment records: 10 years (tax compliance)

SECURITY:
• End-to-end encryption for sensitive data
• Regular security audits and updates
• Blockchain attribution for immutability
• GDPR-compliant data processing agreements

Contact: privacy@ysenseai.org for data requests
"""

# Global terms and consent system
terms_consent_system = TermsConsentSystem()
