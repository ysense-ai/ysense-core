# api/auth.py
"""
YSense Platform v3.0 Authentication API
Handles user registration, login, and consent management
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import secrets
import jwt
from passlib.context import CryptContext
import bcrypt

from src.models import User, ConsentRecord, AuditLog, get_session, generate_user_id, generate_audit_id
from src.config import Config

router = APIRouter()
# Use a more compatible bcrypt configuration
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__min_rounds=10,
    bcrypt__max_rounds=15
)
security = HTTPBearer()

# ==================== Pydantic Models ====================

class UserRegistration(BaseModel):
    """User registration with comprehensive consent"""
    username: str
    email: EmailStr
    age: int
    jurisdiction: str = "Malaysia"
    cultural_context: str = "Global"
    
    # Consent fields
    consent_data_collection: bool
    consent_commercial_use: bool
    consent_ai_training: bool
    consent_revenue_sharing: bool
    consent_attribution: bool
    consent_terms: bool
    
    # Optional
    attribution_name: Optional[str] = None
    marketing_consent: bool = False
    research_consent: bool = False
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18:
            raise ValueError('Must be at least 18 years old')
        return v

class UserLogin(BaseModel):
    """User login credentials"""
    username_or_email: str
    crypto_key: str

class ConsentUpdate(BaseModel):
    """Update consent preferences"""
    consent_type: str
    consent_given: bool
    consent_text: Optional[str] = None

class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str
    z_protocol_tier: str
    crypto_key: str  # Return the crypto key to the user
    z_protocol_consent_key: str  # Z Protocol consent verification key

# ==================== Helper Functions ====================

def generate_z_protocol_consent_key(user_id: str, consent_data: dict) -> str:
    """Generate a unique Z Protocol consent verification key"""
    import secrets
    import hashlib
    from datetime import datetime
    
    # Create a comprehensive consent signature
    consent_string = f"{user_id}:{datetime.utcnow().isoformat()}:{consent_data['version']}"
    
    # Add all consent types to the signature
    for consent_type, consent_value in consent_data.items():
        if consent_type not in ['timestamp', 'version']:
            consent_string += f":{consent_type}:{consent_value}"
    
    # Add random entropy for uniqueness
    entropy = secrets.token_hex(16)
    consent_string += f":{entropy}"
    
    # Generate a 40-character Z Protocol key
    z_protocol_key = hashlib.sha256(consent_string.encode()).hexdigest()[:40]
    
    # Format as groups of 5 characters for easy reading
    formatted_key = '-'.join([z_protocol_key[i:i+5] for i in range(0, len(z_protocol_key), 5)])
    
    return formatted_key

def generate_crypto_key(username: str) -> str:
    """Generate a unique crypto key for user authentication"""
    import secrets
    import hashlib
    from datetime import datetime
    
    # Create a unique seed based on username and timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    seed = f"{username}_{timestamp}_{secrets.token_hex(8)}"
    
    # Generate a 32-character crypto key
    crypto_key = hashlib.sha256(seed.encode()).hexdigest()[:32]
    
    # Format as groups of 4 characters for easy copying
    formatted_key = '-'.join([crypto_key[i:i+4] for i in range(0, len(crypto_key), 4)])
    
    return formatted_key

def verify_crypto_key(provided_key: str, stored_key: str) -> bool:
    """Verify crypto key (case-insensitive, ignore dashes)"""
    # Normalize both keys: remove dashes and convert to lowercase
    normalized_provided = provided_key.replace('-', '').lower()
    normalized_stored = stored_key.replace('-', '').lower()
    
    return normalized_provided == normalized_stored

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def generate_consent_signature(consent_data: dict) -> str:
    """Generate consent signature for legal proof"""
    consent_string = f"{consent_data['user_id']}:{consent_data['timestamp']}:{consent_data['version']}"
    return hashlib.sha256(consent_string.encode()).hexdigest()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = get_session()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

def log_audit(db: Session, user_id: str, action: str, action_type: str, 
              entity_type: str = None, entity_id: str = None, metadata: dict = None,
              request: Request = None):
    """Create audit log entry for compliance"""
    audit_log = AuditLog(
        id=generate_audit_id(user_id, action),
        user_id=user_id,
        action=action,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        audit_metadata=metadata or {},
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("User-Agent") if request else None,
        request_method=request.method if request else None,
        request_path=str(request.url.path) if request else None
    )
    db.add(audit_log)
    db.commit()

# ==================== API Endpoints ====================

@router.post("/register", response_model=TokenResponse)
async def register_user(registration: UserRegistration, request: Request):
    """Register new user with full consent management"""
    
    db = get_session()
    
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == registration.username) | 
        (User.email == registration.email)
    ).first()
    
    if existing_user:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    # Validate all required consents
    required_consents = [
        registration.consent_data_collection,
        registration.consent_commercial_use,
        registration.consent_ai_training,
        registration.consent_revenue_sharing,
        registration.consent_attribution,
        registration.consent_terms
    ]
    
    if not all(required_consents):
        db.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All required consents must be accepted"
        )
    
    # Create consent record
    consent_record = {
        "data_collection": registration.consent_data_collection,
        "commercial_use": registration.consent_commercial_use,
        "ai_training": registration.consent_ai_training,
        "revenue_sharing": registration.consent_revenue_sharing,
        "attribution": registration.consent_attribution,
        "terms": registration.consent_terms,
        "marketing": registration.marketing_consent,
        "research": registration.research_consent,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0"
    }
    
    # Generate crypto key for user
    crypto_key = generate_crypto_key(registration.username)
    
    # Create user
    user_id = generate_user_id(registration.username)
    
    # Generate Z Protocol consent verification key
    z_protocol_consent_key = generate_z_protocol_consent_key(user_id, consent_record)
    
    user = User(
        id=user_id,
        username=registration.username,
        email=registration.email,
        crypto_key=crypto_key,
        age=registration.age,
        age_verified=True,
        jurisdiction=registration.jurisdiction,
        cultural_context=registration.cultural_context,
        
        # Consent
        consent_signature=generate_consent_signature({
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0"
        }),
        consent_timestamp=datetime.utcnow(),
        consent_version="2.0",
        consent_record=consent_record,
        
        # Attribution
        attribution_id=secrets.token_urlsafe(16),
        attribution_name=registration.attribution_name or registration.username,
        
        # Z Protocol
        z_protocol_id=f"ZP_{secrets.token_hex(8).upper()}",
        z_protocol_score=0.0,
        z_protocol_tier="Bronze",
        z_protocol_consent_key=z_protocol_consent_key,
        
        # Revenue
        revenue_tier="Bronze",
        revenue_share_percentage=30.0
    )
    
    db.add(user)
    
    # Create individual consent records for audit trail
    consent_types = {
        "data_collection": "I consent to YSense collecting my wisdom",
        "commercial_use": "I consent to commercial use with attribution",
        "ai_training": "I consent to ethical AI training use",
        "revenue_sharing": "I accept 30% revenue share terms",
        "attribution": "I understand attribution is permanent",
        "terms": "I have read and accept Terms of Service v2.0"
    }
    
    for consent_type, consent_text in consent_types.items():
        consent = ConsentRecord(
            id=f"CONSENT_{secrets.token_hex(8).upper()}",
            user_id=user_id,
            consent_type=consent_type,
            consent_given=getattr(registration, f"consent_{consent_type}"),
            consent_text=consent_text,
            consent_version="2.0",
            consent_method="checkbox",
            consent_signature=generate_consent_signature({
                "user_id": user_id,
                "consent_type": consent_type,
                "timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"
            }),
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent")
        )
        db.add(consent)
    
    # Log registration
    log_audit(db, user_id, "USER_REGISTRATION", "create", "user", user_id, 
             {"username": registration.username, "jurisdiction": registration.jurisdiction},
             request)
    
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": user_id,
            "username": user.username,
            "z_protocol_tier": user.z_protocol_tier
        }
    )
    
    db.close()
    
    return TokenResponse(
        access_token=access_token,
        expires_in=Config.JWT_EXPIRATION_HOURS * 3600,
        user_id=user_id,
        username=user.username,
        z_protocol_tier=user.z_protocol_tier,
        crypto_key=crypto_key,
        z_protocol_consent_key=z_protocol_consent_key
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin, request: Request):
    """Authenticate user and return JWT token"""
    
    db = get_session()
    
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == credentials.username_or_email) |
        (User.email == credentials.username_or_email)
    ).first()
    
    if not user or not verify_crypto_key(credentials.crypto_key, user.crypto_key):
        db.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or crypto key"
        )
    
    # Check account status
    if user.account_status != "active":
        db.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.account_status}"
        )
    
    # Update last active
    user.last_active = datetime.utcnow()
    
    # Log login
    log_audit(db, user.id, "USER_LOGIN", "access", "user", user.id,
             {"method": "password"}, request)
    
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": user.id,
            "username": user.username,
            "z_protocol_tier": user.z_protocol_tier
        }
    )
    
    db.close()
    
    return TokenResponse(
        access_token=access_token,
        expires_in=Config.JWT_EXPIRATION_HOURS * 3600,
        user_id=user.id,
        username=user.username,
        z_protocol_tier=user.z_protocol_tier,
        crypto_key=user.crypto_key,
        z_protocol_consent_key=user.z_protocol_consent_key
    )

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "jurisdiction": current_user.jurisdiction,
        "cultural_context": current_user.cultural_context,
        "z_protocol_tier": current_user.z_protocol_tier,
        "z_protocol_score": current_user.z_protocol_score,
        "revenue_tier": current_user.revenue_tier,
        "revenue_share_percentage": current_user.revenue_share_percentage,
        "total_earnings": current_user.total_earnings,
        "pending_earnings": current_user.pending_earnings,
        "attribution_id": current_user.attribution_id,
        "created_at": current_user.created_at.isoformat()
    }

@router.post("/consent/update")
async def update_consent(
    consent_update: ConsentUpdate,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Update user consent preferences"""
    
    db = get_session()
    
    # Create new consent record
    consent = ConsentRecord(
        id=f"CONSENT_{secrets.token_hex(8).upper()}",
        user_id=current_user.id,
        consent_type=consent_update.consent_type,
        consent_given=consent_update.consent_given,
        consent_text=consent_update.consent_text,
        consent_version="2.0",
        consent_method="explicit_update",
        consent_signature=generate_consent_signature({
            "user_id": current_user.id,
            "consent_type": consent_update.consent_type,
            "consent_given": consent_update.consent_given,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0"
        }),
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    
    db.add(consent)
    
    # Update user's consent record
    user = db.query(User).filter(User.id == current_user.id).first()
    consent_record = user.consent_record.copy()
    consent_record[consent_update.consent_type] = consent_update.consent_given
    user.consent_record = consent_record
    user.updated_at = datetime.utcnow()
    
    # Log consent update
    log_audit(db, current_user.id, "CONSENT_UPDATE", "update", "consent",
             consent.id, {"consent_type": consent_update.consent_type,
                         "consent_given": consent_update.consent_given}, request)
    
    db.commit()
    db.close()
    
    return {
        "message": "Consent updated successfully",
        "consent_type": consent_update.consent_type,
        "consent_given": consent_update.consent_given,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/consent/lookup/{z_protocol_consent_key}")
async def lookup_user_by_consent_key(z_protocol_consent_key: str):
    """Look up user by Z Protocol consent key for consent management"""
    
    db = get_session()
    
    user = db.query(User).filter(User.z_protocol_consent_key == z_protocol_consent_key).first()
    
    if not user:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this Z Protocol consent key"
        )
    
    # Return only essential information for consent management
    user_info = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "jurisdiction": user.jurisdiction,
        "z_protocol_tier": user.z_protocol_tier,
        "consent_timestamp": user.consent_timestamp.isoformat(),
        "consent_version": user.consent_version,
        "consent_record": user.consent_record,
        "account_status": user.account_status
    }
    
    db.close()
    
    return user_info

@router.post("/consent/withdraw")
async def withdraw_consent(
    z_protocol_consent_key: str,
    request: Request
):
    """Withdraw user consent using Z Protocol consent key"""
    
    db = get_session()
    
    user = db.query(User).filter(User.z_protocol_consent_key == z_protocol_consent_key).first()
    
    if not user:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this Z Protocol consent key"
        )
    
    # Log consent withdrawal
    log_audit(db, user.id, "CONSENT_WITHDRAWAL", "update", "consent",
             z_protocol_consent_key, {"withdrawal_method": "z_protocol_key"}, request)
    
    # Update user consent record to mark as withdrawn
    consent_record = user.consent_record.copy()
    consent_record["withdrawn"] = True
    consent_record["withdrawal_timestamp"] = datetime.utcnow().isoformat()
    user.consent_record = consent_record
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.close()
    
    return {
        "message": "Consent successfully withdrawn",
        "user_id": user.id,
        "username": user.username,
        "withdrawal_timestamp": datetime.utcnow().isoformat()
    }

@router.post("/logout")
async def logout_user(request: Request, current_user: User = Depends(get_current_user)):
    """Logout user (mainly for audit trail)"""
    
    db = get_session()
    
    # Log logout
    log_audit(db, current_user.id, "USER_LOGOUT", "access", "user",
             current_user.id, {}, request)
    
    db.commit()
    db.close()
    
    return {"message": "Logged out successfully"}

@router.delete("/account")
async def delete_account(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Delete user account (GDPR/PDPA compliance)"""
    
    db = get_session()
    
    # Log deletion request
    log_audit(db, current_user.id, "ACCOUNT_DELETION", "delete", "user",
             current_user.id, {"reason": "user_requested"}, request)
    
    # Soft delete (mark as deleted but keep for legal compliance)
    user = db.query(User).filter(User.id == current_user.id).first()
    user.account_status = "deleted"
    user.email = f"deleted_{user.id}@deleted.com"
    user.username = f"deleted_{user.id}"
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.close()
    
    return {"message": "Account marked for deletion. Data will be retained for legal compliance."}
