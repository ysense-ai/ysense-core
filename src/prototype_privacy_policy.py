# src/prototype_privacy_policy.py
"""
YSense™ Platform - Prototype Privacy Policy
Simple privacy policy for demonstration phase
"""

from datetime import datetime

class PrototypePrivacyPolicy:
    """Privacy policy for prototype/demo mode"""

    def __init__(self):
        self.version = "Prototype 1.0"
        self.effective_date = "2025-10-05"

    def get_privacy_policy(self) -> str:
        """Get complete privacy policy for prototype mode"""
        return f"""
YSENSE™ PLATFORM - PROTOTYPE PRIVACY POLICY
Version: {self.version}
Effective Date: {self.effective_date}

═══════════════════════════════════════════════════════════════

🚧 PROTOTYPE DEMONSTRATION NOTICE

This privacy policy applies ONLY to the current prototype/demonstration
version of YSense Platform. The production version will have a comprehensive
privacy policy compliant with all applicable laws.

═══════════════════════════════════════════════════════════════

1. WHAT THIS PROTOTYPE IS

   This is a DEMONSTRATION platform to showcase the concept of ethical
   AI attribution infrastructure. It is NOT a production service.

   Purpose:
   • Demonstrate platform concept and vision
   • Test user interface and features
   • Gather interest in the platform idea
   • Educational and research purposes

═══════════════════════════════════════════════════════════════

2. PERSONAL DATA COLLECTION: NONE

   ✅ We DO NOT collect:
   • NO names, emails, or contact information
   • NO government IDs or identity documents
   • NO payment information
   • NO location data or IP addresses (beyond standard web logs)
   • NO user-created accounts or profiles
   • NO passwords (demo account only)
   • NO personal identifiers of any kind

   What we DO collect:
   • Anonymous interest counter (just a number: "X people interested")
   • Basic web server logs (standard for all websites)
   • Anonymous usage statistics (which features are explored)

═══════════════════════════════════════════════════════════════

3. DEMO ACCOUNT INFORMATION

   Access Method:
   • Single shared demo account for all users
   • Username: demo_user
   • Password: ysense_prototype_2025

   What this means:
   • You are NOT creating a personal account
   • Everyone uses the same credentials
   • No individual user identification
   • No personalized data storage

═══════════════════════════════════════════════════════════════

4. DATA STORAGE AND RETENTION

   🎬 LIVE DEMO MODE (AI Analysis Active):
   • Real AI analysis using Anthropic Claude & QWEN APIs
   • Your input text is sent to AI services for analysis
   • AI providers have their own privacy policies
   • Results stored in session ONLY (browser memory)
   • ALL data deleted immediately on page refresh/logout
   • NO permanent database storage of your content
   • NO long-term retention of analysis results

   Demo Data:
   • All demo data resets regularly (daily/weekly)
   • Nothing is permanently stored
   • No backups of demo content
   • No long-term data retention

   Interest Counter:
   • Simple anonymous count only
   • No identification of who clicked
   • Stored as single number
   • No personal association

   ⚠️ AI API DATA PROCESSING:
   When you use the AI Workflow feature:
   • Your story/input is sent to Anthropic (Claude API)
   • Your story/input is sent to Alibaba Cloud (QWEN API)
   • These providers process data according to their policies:
     - Anthropic: https://www.anthropic.com/privacy
     - Alibaba Cloud: https://www.alibabacloud.com/help/en/legal/
   • We do NOT control how AI providers handle data
   • Use for demonstration purposes only
   • Do NOT enter sensitive personal information

═══════════════════════════════════════════════════════════════

5. COOKIES AND TRACKING

   We Use:
   • Essential session cookies (for demo functionality)
   • Streamlit framework default cookies (technical necessity)

   We DO NOT Use:
   • NO advertising cookies
   • NO third-party tracking
   • NO analytics beyond basic Streamlit defaults
   • NO cross-site tracking
   • NO behavioral profiling

   You Can:
   • Use browser in incognito/private mode
   • Clear cookies at any time
   • No impact on demonstration experience

═══════════════════════════════════════════════════════════════

6. THIRD-PARTY SERVICES

   Platform Infrastructure:
   • Hosted on Google Cloud Run (Google Cloud Platform)
   • Subject to Google Cloud's privacy policies
   • Standard web hosting security measures

   AI Analysis Services (Live Demo Mode):
   • Anthropic Claude API - processes your input for analysis
   • Alibaba Cloud QWEN API - processes your input for analysis
   • Data sent to these services is subject to their policies
   • We recommend reviewing their privacy policies before use
   • Session-only processing, no permanent storage by us

   We DO NOT Share Data With:
   • NO advertising networks
   • NO data brokers
   • NO third-party analytics companies beyond AI APIs
   • NO marketing platforms
   • NO data brokers or resellers

═══════════════════════════════════════════════════════════════

7. YOUR RIGHTS (Even for Prototype)

   You Have the Right To:
   • Access: Request what data we have (answer: basically none)
   • Deletion: Request deletion of any data (not applicable)
   • Object: Object to data processing (no processing happening)
   • Withdraw: Leave the platform at any time
   • Questions: Contact us with privacy concerns

   How to Exercise Rights:
   • Email: privacy@ysenseai.org
   • Simply close browser (no data to delete anyway)

═══════════════════════════════════════════════════════════════

8. CHILDREN'S PRIVACY

   Age Restriction:
   • This prototype is intended for adults 18+ only
   • We do not knowingly collect data from children
   • If you are under 18, please do not use this prototype
   • Parents: Contact us if you believe a child accessed this platform

═══════════════════════════════════════════════════════════════

9. SECURITY MEASURES

   Prototype Security:
   • HTTPS encryption for all connections
   • Secure hosting on Google Cloud Platform
   • No sensitive data stored = minimal risk
   • Standard web security practices

   Limitations:
   • This is a demonstration, not production-grade security
   • Do NOT enter any real personal information
   • Do NOT treat this as a secure platform
   • Use demo credentials only

═══════════════════════════════════════════════════════════════

10. CHANGES TO THIS POLICY

    Updates:
    • This policy may be updated during prototype phase
    • Changes will be posted on this page
    • Continued use = acceptance of changes
    • Check back periodically for updates

═══════════════════════════════════════════════════════════════

11. TRANSITION TO PRODUCTION

    When Production Launches:
    • NEW comprehensive privacy policy will be published
    • Full GDPR/CCPA compliance
    • Professional data protection measures
    • Clear user consent mechanisms
    • Secure account creation and management

    You Will Be Notified:
    • Clear announcement of production launch
    • Opportunity to create real account
    • New terms and privacy policy to accept
    • Fresh start with proper data protection

═══════════════════════════════════════════════════════════════

12. LEGAL BASIS (EU Users)

    Prototype Participation:
    • Legal basis: Legitimate interest (demonstration/research)
    • No personal data processing = minimal GDPR application
    • Anonymous interest tracking = not personal data
    • Voluntary participation only

═══════════════════════════════════════════════════════════════

13. INTERNATIONAL DATA TRANSFERS

    Hosting Location:
    • Google Cloud Platform - Asia Southeast region
    • May be accessed from any country
    • No personal data = no transfer concerns
    • Standard internet protocols apply

═══════════════════════════════════════════════════════════════

14. CONTACT INFORMATION

    Privacy Questions:
    • Email: alton@ysenseai.org
    • Subject: "Prototype Privacy Inquiry"

    General Contact:
    • Email: alton@ysenseai.org
    • Website: ysenseai.org

    Response Time:
    • We aim to respond within 7 business days
    • May be longer during prototype phase

═══════════════════════════════════════════════════════════════

15. DISCLAIMERS

    Important Notices:
    • This is NOT a production service
    • Do NOT enter real personal information
    • Do NOT expect data persistence
    • Do NOT treat as legally binding platform
    • For demonstration purposes only

    Your Responsibility:
    • Use demo credentials only
    • Do not share sensitive information
    • Understand this is a prototype
    • Ask questions if uncertain

═══════════════════════════════════════════════════════════════

SUMMARY

✅ No personal data collected
✅ Demo account shared by all users
✅ Anonymous interest counter only
✅ Data resets regularly
✅ HTTPS secure connection
✅ No third-party tracking
✅ Educational demonstration only

⚠️ This is a PROTOTYPE
⚠️ Not production-ready
⚠️ Use demo credentials only
⚠️ No data permanence
⚠️ Production version coming soon

═══════════════════════════════════════════════════════════════

By using this prototype demonstration, you acknowledge:

1. You understand this is NOT a production platform
2. You will NOT enter real personal information
3. You use the shared demo account only
4. You understand data is not permanently stored
5. You accept this privacy policy

═══════════════════════════════════════════════════════════════

Last Updated: {self.effective_date}
YSense™ Platform - Prototype Demonstration
© 2025 YSense AI - All Rights Reserved

═══════════════════════════════════════════════════════════════
"""

    def get_short_privacy_notice(self) -> str:
        """Get short privacy notice for display"""
        return """
**🔒 Privacy Notice (Prototype)**

• NO personal data collected
• Demo account shared by all users
• Anonymous interest tracking only
• All data resets regularly
• For demonstration purposes only

[View Full Privacy Policy](#)
"""

# Global instance
prototype_privacy = PrototypePrivacyPolicy()
