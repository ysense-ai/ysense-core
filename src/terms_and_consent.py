# terms_and_consent.py
"""
Terms of Service and Consent Management System
Must be accepted before registration and contribution
"""

from datetime import datetime
from typing import Dict, Optional
import hashlib
import json

class TermsAndConsent:
    """Manage Terms of Service and Consent Flow"""
    
    def __init__(self):
        self.version = "2.0"
        self.effective_date = "2024-01-01"
        self.minimum_age = 18
        
    def get_terms_of_service(self) -> str:
        """Return current Terms of Service"""
        return """
YSENSE PLATFORM TERMS OF SERVICE
Version 2.0 - Effective January 2024

BY REGISTERING, YOU ACKNOWLEDGE AND AGREE:

1. ELIGIBILITY
   • You are at least 18 years old
   • You have the legal right to enter this agreement
   • You are not prohibited from using this service

2. YOUR WISDOM CONTRIBUTIONS
   • All content must be YOUR original creation
   • You warrant NO copyrighted material included
   • You grant YSense perpetual, worldwide license
   • Attribution will ALWAYS be maintained

3. COPYRIGHT & LIABILITY
   • You are SOLELY responsible for copyright violations
   • You indemnify YSense against ALL claims
   • Fraudulent submissions = immediate termination
   • Legal action may be pursued for violations

4. REVENUE SHARING
   • 30% revenue share on wisdom monetization
   • Payment after €50 minimum threshold
   • Revenue calculated by quality score
   • No guarantee of earnings

5. DATA PROTECTION (GDPR Compliant)
   • We process data under legitimate interest
   • You have right to access your data
   • You can request deletion (except published wisdom)
   • Audit trail kept for 7 years

6. PROHIBITED CONTENT
   • No personal identifying information
   • No harmful or illegal content
   • No discrimination or hate speech
   • No private information about others

7. Z PROTOCOL COMPLIANCE
   • All submissions undergo ethical validation
   • Must achieve 80%+ compliance score
   • Failed validations = submission rejected
   • Multiple violations = account suspension

8. MODIFICATION & TERMINATION
   • We may update terms with 30 days notice
   • You may delete account anytime
   • Published wisdom remains licensed
   • Attribution remains permanent

BY CLICKING "I AGREE", YOU CONFIRM:
- You have READ and UNDERSTOOD these terms
- You ACCEPT full responsibility for your content
- You CONSENT to commercial use with attribution
- You WAIVE claims except as specified herein
"""
    
    def get_consent_checkboxes(self) -> Dict[str, str]:
        """Return required consent checkboxes for registration"""
        return {
            "terms_acceptance": {
                "label": "I have read and accept the Terms of Service",
                "required": True,
                "description": "You must accept terms to proceed"
            },
            "age_verification": {
                "label": "I confirm I am 18 years or older",
                "required": True,
                "description": "Platform restricted to adults"
            },
            "original_content": {
                "label": "I will only submit my original content",
                "required": True,
                "description": "No copyrighted material allowed"
            },
            "commercial_use": {
                "label": "I consent to commercial use with attribution",
                "required": True,
                "description": "Your wisdom may be sold to AI companies"
            },
            "revenue_share": {
                "label": "I accept the 30% revenue sharing model",
                "required": True,
                "description": "You receive 30% of wisdom monetization"
            },
            "data_processing": {
                "label": "I consent to data processing per GDPR",
                "required": True,
                "description": "Required for platform operation"
            },
            "liability_acceptance": {
                "label": "I accept liability for copyright fraud",
                "required": True,
                "description": "You are responsible for content authenticity"
            }
        }
    
    def validate_consent(self, consent_data: Dict) -> Dict:
        """Validate all consents are properly given"""
        
        required_consents = self.get_consent_checkboxes()
        missing = []
        
        for consent_id, consent_info in required_consents.items():
            if consent_info["required"] and not consent_data.get(consent_id):
                missing.append(consent_info["label"])
        
        if missing:
            return {
                "valid": False,
                "missing_consents": missing,
                "message": "All required consents must be accepted"
            }
        
        # Generate consent signature
        consent_signature = self.generate_consent_signature(consent_data)
        
        return {
            "valid": True,
            "consent_signature": consent_signature,
            "timestamp": datetime.now().isoformat(),
            "version": self.version
        }
    
    def generate_consent_signature(self, consent_data: Dict) -> str:
        """Generate cryptographic proof of consent"""
        consent_string = json.dumps(consent_data, sort_keys=True)
        return hashlib.sha256(
            f"{consent_string}:{datetime.now().isoformat()}".encode()
        ).hexdigest()
    
    def get_contribution_agreement(self) -> str:
        """Additional agreement shown before each contribution"""
        return """
WISDOM CONTRIBUTION AGREEMENT

By submitting this wisdom, I confirm:
✓ This is MY original thought/experience
✓ No copyrighted content included
✓ I accept 30% revenue share
✓ Attribution will be permanent
✓ I am liable for any false claims

⚠️ WARNING: Copyright fraud may result in:
- Account termination
- Legal action
- Personal liability for damages
"""