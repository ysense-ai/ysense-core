# 🔑 YSense Platform v4.0 - Key Recovery API Implementation

from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import secrets
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.models import User, get_session
from src.config import Config
from api.auth import get_current_user

router = APIRouter()

# ==================== Pydantic Models ====================

class KeyRecoveryRequest(BaseModel):
    email: EmailStr
    recovery_type: str  # "crypto_key", "z_protocol_key", "both"

class KeyRecoveryResponse(BaseModel):
    success: bool
    message: str
    recovery_id: Optional[str] = None

class AccountRecoveryInfo(BaseModel):
    email: str
    username: str
    account_status: str
    recovery_enabled: bool
    last_recovery_attempt: Optional[datetime] = None
    available_recovery_methods: list

# ==================== Email Service ====================

class EmailRecoveryService:
    """Service for sending key recovery emails"""
    
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.smtp_username = Config.SMTP_USERNAME
        self.smtp_password = Config.SMTP_PASSWORD
        self.from_email = Config.FROM_EMAIL
    
    def send_crypto_key_recovery(self, user: User, crypto_key: str) -> bool:
        """Send crypto key recovery email"""
        try:
            subject = "YSense Platform - Crypto Key Recovery"
            body = f"""
Dear {user.username},

You requested recovery of your crypto key for your YSense account.

Your Crypto Key: {crypto_key}

IMPORTANT SECURITY NOTES:
- This key is unique to your account
- Keep it secure and don't share it
- You can use this key to log in to your account
- Consider generating a new key for enhanced security

If you didn't request this recovery, please contact support immediately.

Best regards,
YSense Platform Team
            """
            
            return self._send_email(user.email, subject, body)
        except Exception as e:
            print(f"Error sending crypto key recovery email: {e}")
            return False
    
    def send_z_protocol_key_recovery(self, user: User, z_protocol_key: str) -> bool:
        """Send Z Protocol key recovery email"""
        try:
            subject = "YSense Platform - Z Protocol Key Recovery"
            body = f"""
Dear {user.username},

You requested recovery of your Z Protocol consent key for your YSense account.

Your Z Protocol Consent Key: {z_protocol_key}

IMPORTANT SECURITY NOTES:
- This key is unique to your account
- Keep it secure and don't share it
- You can use this key for consent management
- Consider generating a new key for enhanced security

If you didn't request this recovery, please contact support immediately.

Best regards,
YSense Platform Team
            """
            
            return self._send_email(user.email, subject, body)
        except Exception as e:
            print(f"Error sending Z Protocol key recovery email: {e}")
            return False
    
    def send_both_keys_recovery(self, user: User, crypto_key: str, z_protocol_key: str) -> bool:
        """Send both keys recovery email"""
        try:
            subject = "YSense Platform - Complete Key Recovery"
            body = f"""
Dear {user.username},

You requested recovery of all your keys for your YSense account.

Your Crypto Key: {crypto_key}
Your Z Protocol Consent Key: {z_protocol_key}

IMPORTANT SECURITY NOTES:
- These keys are unique to your account
- Keep them secure and don't share them
- You can use these keys to access your account
- Consider generating new keys for enhanced security

If you didn't request this recovery, please contact support immediately.

Best regards,
YSense Platform Team
            """
            
            return self._send_email(user.email, subject, body)
        except Exception as e:
            print(f"Error sending both keys recovery email: {e}")
            return False
    
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False

# ==================== Recovery Logging ====================

def log_recovery_attempt(db: Session, user_id: str, recovery_type: str, 
                        recovery_method: str, success: bool, request: Request):
    """Log recovery attempt for audit trail"""
    try:
        from src.models import AuditLog
        
        audit_log = AuditLog(
            id=f"RECOVERY_{secrets.token_hex(8).upper()}",
            user_id=user_id,
            action="KEY_RECOVERY",
            action_type="access",
            entity_type="user",
            entity_id=user_id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", ""),
            request_method="POST",
            request_path="/api/v4/auth/recover-keys",
            audit_metadata={
                "recovery_type": recovery_type,
                "recovery_method": recovery_method,
                "success": success
            }
        )
        
        db.add(audit_log)
        db.commit()
    except Exception as e:
        print(f"Error logging recovery attempt: {e}")

# ==================== API Endpoints ====================

@router.post("/recover-crypto-key", response_model=KeyRecoveryResponse)
async def recover_crypto_key(recovery_request: KeyRecoveryRequest, request: Request):
    """Recover crypto key via email"""
    
    db = get_session()
    
    try:
        # Find user by email
        user = db.query(User).filter(User.email == recovery_request.email).first()
        
        if not user:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No account found with this email address"
            )
        
        # Check if recovery is enabled
        if not getattr(user, 'recovery_enabled', True):
            db.close()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Key recovery is disabled for this account"
            )
        
        # Check rate limiting (max 3 attempts per hour)
        recent_attempts = db.query(AuditLog).filter(
            AuditLog.user_id == user.id,
            AuditLog.action == "KEY_RECOVERY",
            AuditLog.created_at >= datetime.utcnow() - timedelta(hours=1)
        ).count()
        
        if recent_attempts >= 3:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many recovery attempts. Please wait before trying again."
            )
        
        # Send recovery email
        email_service = EmailRecoveryService()
        
        if recovery_request.recovery_type == "crypto_key":
            success = email_service.send_crypto_key_recovery(user, user.crypto_key)
        elif recovery_request.recovery_type == "z_protocol_key":
            success = email_service.send_z_protocol_key_recovery(user, user.z_protocol_consent_key)
        elif recovery_request.recovery_type == "both":
            success = email_service.send_both_keys_recovery(
                user, user.crypto_key, user.z_protocol_consent_key
            )
        else:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid recovery type"
            )
        
        # Log recovery attempt
        log_recovery_attempt(
            db, user.id, recovery_request.recovery_type, 
            "email", success, request
        )
        
        if success:
            db.close()
            return KeyRecoveryResponse(
                success=True,
                message="Recovery email sent successfully. Check your inbox.",
                recovery_id=f"RECOVERY_{secrets.token_hex(8).upper()}"
            )
        else:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send recovery email. Please try again later."
            )
    
    except HTTPException:
        raise
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recovery failed: {str(e)}"
        )

@router.get("/account-recovery/{email}", response_model=AccountRecoveryInfo)
async def get_account_recovery_info(email: str):
    """Get account recovery information"""
    
    db = get_session()
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No account found with this email address"
            )
        
        # Get last recovery attempt
        last_recovery = db.query(AuditLog).filter(
            AuditLog.user_id == user.id,
            AuditLog.action == "KEY_RECOVERY"
        ).order_by(AuditLog.created_at.desc()).first()
        
        db.close()
        
        return AccountRecoveryInfo(
            email=user.email,
            username=user.username,
            account_status=user.account_status,
            recovery_enabled=getattr(user, 'recovery_enabled', True),
            last_recovery_attempt=last_recovery.created_at if last_recovery else None,
            available_recovery_methods=["email"]  # Can be extended
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recovery info: {str(e)}"
        )

@router.post("/generate-new-keys")
async def generate_new_keys(current_user: User = Depends(get_current_user)):
    """Generate new crypto and Z Protocol keys for current user"""
    
    db = get_session()
    
    try:
        # Generate new crypto key
        new_crypto_key = generate_crypto_key(current_user.username)
        
        # Generate new Z Protocol key
        new_z_protocol_key = generate_z_protocol_consent_key(
            current_user.id, current_user.consent_record
        )
        
        # Update user with new keys
        current_user.crypto_key = new_crypto_key
        current_user.z_protocol_consent_key = new_z_protocol_key
        current_user.updated_at = datetime.utcnow()
        
        db.commit()
        db.close()
        
        return {
            "success": True,
            "message": "New keys generated successfully",
            "crypto_key": new_crypto_key,
            "z_protocol_consent_key": new_z_protocol_key
        }
    
    except Exception as e:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate new keys: {str(e)}"
        )
