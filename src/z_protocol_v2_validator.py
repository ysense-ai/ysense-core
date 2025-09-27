# 🔐 YSense Platform v4.0 - Z Protocol v2.0 Validator

"""
Z Protocol v2.0 Compliance Validator for YSense Platform v4.0
Ensures ethical AI training and proper attribution
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib
import json

class ZProtocolV2Validator:
    """Z Protocol v2.0 compliance validator"""
    
    def __init__(self):
        self.protocol_version = "2.0"
        self.compliance_standards = {
            "attribution": True,
            "consent": True,
            "revenue_sharing": True,
            "data_protection": True,
            "ethical_ai": True,
            "cultural_sensitivity": True
        }
    
    def validate_user_consent(self, user_data: Dict) -> Dict[str, Any]:
        """Validate user consent compliance"""
        required_consents = [
            "consent_data_collection",
            "consent_commercial_use", 
            "consent_ai_training",
            "consent_revenue_sharing",
            "consent_attribution",
            "consent_terms"
        ]
        
        consent_status = {}
        for consent in required_consents:
            consent_status[consent] = user_data.get(consent, False)
        
        all_consented = all(consent_status.values())
        
        return {
            "compliant": all_consented,
            "consent_status": consent_status,
            "missing_consents": [k for k, v in consent_status.items() if not v],
            "z_protocol_score": 100 if all_consented else 0
        }
    
    def validate_wisdom_drop(self, wisdom_data: Dict, user_data: Dict) -> Dict[str, Any]:
        """Validate wisdom drop for Z Protocol v2.0 compliance"""
        
        # Check attribution
        attribution_valid = bool(wisdom_data.get("attribution_hash")) and bool(wisdom_data.get("attribution_text"))
        
        # Check consent compliance
        consent_check = self.validate_user_consent(user_data)
        
        # Check cultural sensitivity
        cultural_context = wisdom_data.get("cultural_context", "Global")
        cultural_multiplier = wisdom_data.get("cultural_multiplier", 1.0)
        cultural_compliant = cultural_multiplier is not None and cultural_multiplier >= 1.0
        
        # Check quality standards
        quality_score = wisdom_data.get("quality_score", 0)
        quality_compliant = quality_score is not None and quality_score >= 0.7  # 70% minimum quality
        
        # Check completeness
        completeness = wisdom_data.get("completeness", {})
        completeness_score = completeness.get("overall", 0) if isinstance(completeness, dict) else 0
        completeness_compliant = completeness_score is not None and completeness_score >= 0.8  # 80% minimum completeness
        
        # Calculate Z Protocol score
        z_protocol_score = 0
        if attribution_valid:
            z_protocol_score += 25
        if consent_check["compliant"]:
            z_protocol_score += 25
        if cultural_compliant:
            z_protocol_score += 20
        if quality_compliant:
            z_protocol_score += 15
        if completeness_compliant:
            z_protocol_score += 15
        
        return {
            "compliant": z_protocol_score >= 80,  # 80% minimum for compliance
            "z_protocol_score": z_protocol_score,
            "attribution_valid": attribution_valid,
            "consent_compliant": consent_check["compliant"],
            "cultural_compliant": cultural_compliant,
            "quality_compliant": quality_compliant,
            "completeness_compliant": completeness_compliant,
            "violations": self._identify_violations(
                attribution_valid, consent_check["compliant"], 
                cultural_compliant, quality_compliant, completeness_compliant
            ),
            "recommendations": self._generate_recommendations(
                attribution_valid, consent_check["compliant"],
                cultural_compliant, quality_compliant, completeness_compliant
            )
        }
    
    def _identify_violations(self, attribution: bool, consent: bool, 
                           cultural: bool, quality: bool, completeness: bool) -> List[str]:
        """Identify Z Protocol v2.0 violations"""
        violations = []
        
        if not attribution:
            violations.append("Missing or invalid attribution")
        if not consent:
            violations.append("Insufficient consent compliance")
        if not cultural:
            violations.append("Cultural sensitivity issues")
        if not quality:
            violations.append("Quality standards not met")
        if not completeness:
            violations.append("Incomplete wisdom drop")
        
        return violations
    
    def _generate_recommendations(self, attribution: bool, consent: bool,
                                cultural: bool, quality: bool, completeness: bool) -> List[str]:
        """Generate recommendations for Z Protocol v2.0 compliance"""
        recommendations = []
        
        if not attribution:
            recommendations.append("Ensure proper attribution hash and text are generated")
        if not consent:
            recommendations.append("Verify all required consents are obtained")
        if not cultural:
            recommendations.append("Review cultural context and sensitivity")
        if not quality:
            recommendations.append("Improve wisdom drop quality (minimum 70%)")
        if not completeness:
            recommendations.append("Complete all required fields (minimum 80%)")
        
        return recommendations
    
    def generate_attribution_hash(self, user_id: str, wisdom_id: str, content: str) -> str:
        """Generate attribution hash for Z Protocol v2.0 compliance"""
        attribution_string = f"{user_id}:{wisdom_id}:{content}:{self.protocol_version}"
        return hashlib.sha256(attribution_string.encode()).hexdigest()
    
    def generate_attribution_text(self, user_data: Dict) -> str:
        """Generate attribution text for Z Protocol v2.0 compliance"""
        username = user_data.get("username", "Unknown")
        user_id = user_data.get("id", "Unknown")
        return f"Attribution: {username} ({user_id}) - Z Protocol v2.0 Compliant"
    
    def audit_compliance(self, action: str, user_id: str, wisdom_id: str, 
                        compliance_data: Dict) -> Dict[str, Any]:
        """Audit Z Protocol v2.0 compliance for logging"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "wisdom_id": wisdom_id,
            "protocol_version": self.protocol_version,
            "compliance_score": compliance_data.get("z_protocol_score", 0),
            "compliant": compliance_data.get("compliant", False),
            "violations": compliance_data.get("violations", []),
            "recommendations": compliance_data.get("recommendations", [])
        }

# Global validator instance
z_protocol_validator = ZProtocolV2Validator()
