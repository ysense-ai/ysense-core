# models.py
"""
YSense Platform v3.0 Database Models
SQLAlchemy models for all platform entities
"""

from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import hashlib
import json
from typing import Optional

Base = declarative_base()

# ==================== User Model ====================
class User(Base):
    """Enhanced User model with Malaysian PDPA compliance"""
    __tablename__ = "users"
    
    # Primary identifiers
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    crypto_key = Column(String, unique=True, nullable=False)  # Replaced password_hash
    
    # Regional Compliance
    jurisdiction = Column(String, nullable=False, default="Malaysia")
    age_verified = Column(Boolean, default=False)
    age = Column(Integer)
    
    # Consent Management
    consent_signature = Column(String, nullable=False)
    consent_timestamp = Column(DateTime, nullable=False)
    consent_version = Column(String, nullable=False, default="2.0")
    consent_record = Column(JSON, nullable=False)
    
    # Z Protocol
    z_protocol_id = Column(String, unique=True)
    z_protocol_score = Column(Float, default=0.0)
    z_protocol_tier = Column(String, default="Bronze")
    z_protocol_consent_key = Column(String, unique=True)  # Z Protocol consent verification key
    
    # Revenue
    revenue_tier = Column(String, default="Bronze")
    revenue_share_percentage = Column(Float, default=30.0)
    total_earnings = Column(Float, default=0.0)
    pending_earnings = Column(Float, default=0.0)
    
    # Attribution
    attribution_id = Column(String, unique=True)
    attribution_name = Column(String)
    cultural_context = Column(String, default="Global")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Status
    account_status = Column(String, default="active")
    email_verified = Column(Boolean, default=False)
    
    # Relationships
    wisdom_drops = relationship("WisdomDrop", back_populates="user", cascade="all, delete-orphan")
    revenue_records = relationship("RevenueRecord", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username} ({self.jurisdiction})>"

# ==================== Wisdom Drop Model ====================
class WisdomDrop(Base):
    """Wisdom contribution with Five-Layer Perception Toolkit"""
    __tablename__ = "wisdom_drops"
    
    # Identifiers
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    # Content
    title = Column(String, nullable=False)
    experience_title = Column(String)
    
    # Five Layers
    layer_narrative = Column(Text)
    layer_somatic = Column(Text)
    layer_attention = Column(Text)
    layer_synesthetic = Column(Text)
    layer_temporal_auditory = Column(Text)
    
    # Deep Vibe Distillation
    vibe_words = Column(JSON)  # List of 3 words
    vibe_words_explanation = Column(Text)  # User's explanation of why they chose these words
    personal_connection = Column(Text)
    essence = Column(Text)
    distillation_completed = Column(Boolean, default=False)
    
    # Cultural Context
    cultural_context = Column(String, default="Global")
    cultural_multiplier = Column(Float, default=1.0)
    language = Column(String, default="en")
    
    # Quality & Scoring
    quality_score = Column(Float, default=0.0)
    z_protocol_score = Column(Float, default=0.0)
    completeness = Column(JSON)
    
    # Attribution
    attribution_hash = Column(String, unique=True, nullable=False)
    attribution_text = Column(String)
    
    # Revenue
    revenue_potential = Column(Float, default=0.0)
    times_accessed = Column(Integer, default=0)
    revenue_generated = Column(Float, default=0.0)
    
    # Status
    status = Column(String, default="draft")  # draft, awaiting_distillation, complete, published
    moderation_status = Column(String, default="pending")
    published = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="wisdom_drops")
    usage_records = relationship("UsageRecord", back_populates="wisdom_drop")
    
    def calculate_quality_score(self):
        """Calculate quality score based on completeness and distillation"""
        score = 0.0
        
        # Check each layer (60% of score)
        layers = [
            self.layer_narrative,
            self.layer_somatic,
            self.layer_attention,
            self.layer_synesthetic,
            self.layer_temporal_auditory
        ]
        
        for layer in layers:
            if layer and len(layer) > 50:
                score += 12.0
        
        # Distillation bonus (40% of score)
        if self.distillation_completed:
            if self.vibe_words and len(self.vibe_words) == 3:
                score += 20.0
            if self.personal_connection:
                score += 10.0
            if self.essence:
                score += 10.0
        
        return min(score, 100.0)

# ==================== Revenue Record Model ====================
class RevenueRecord(Base):
    """Track revenue generation and distribution"""
    __tablename__ = "revenue_records"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    wisdom_drop_id = Column(String, ForeignKey("wisdom_drops.id"))
    
    # Revenue Details
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
    revenue_type = Column(String)  # usage, licensing, bonus
    
    # Payment
    payment_status = Column(String, default="pending")  # pending, paid, failed
    payment_date = Column(DateTime)
    payment_method = Column(String)
    transaction_id = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="revenue_records")

# ==================== Usage Record Model ====================
class UsageRecord(Base):
    """Track how wisdom drops are used"""
    __tablename__ = "usage_records"
    
    id = Column(String, primary_key=True)
    wisdom_drop_id = Column(String, ForeignKey("wisdom_drops.id"))
    
    # Usage Details
    usage_type = Column(String)  # ai_training, research, commercial
    usage_context = Column(String)
    client_id = Column(String)
    
    # Attribution
    attribution_included = Column(Boolean, default=True)
    attribution_format = Column(Text)
    
    # Revenue
    revenue_generated = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wisdom_drop = relationship("WisdomDrop", back_populates="usage_records")

# ==================== Audit Log Model ====================
class AuditLog(Base):
    """Comprehensive audit trail for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    # Action Details
    action = Column(String, nullable=False)
    action_type = Column(String)  # create, update, delete, consent, access
    entity_type = Column(String)
    entity_id = Column(String)
    
    # Request Details
    ip_address = Column(String)
    user_agent = Column(String)
    request_method = Column(String)
    request_path = Column(String)
    
    # Data
    old_value = Column(JSON)
    new_value = Column(JSON)
    audit_metadata = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

# ==================== Z Protocol Validation Model ====================
class ZProtocolValidation(Base):
    """Z Protocol validation records"""
    __tablename__ = "z_protocol_validations"
    
    id = Column(String, primary_key=True)
    wisdom_drop_id = Column(String, ForeignKey("wisdom_drops.id"))
    
    # Validation Scores
    consent_score = Column(Float, default=0.0)
    attribution_score = Column(Float, default=0.0)
    authenticity_score = Column(Float, default=0.0)
    dignity_score = Column(Float, default=0.0)
    transparency_score = Column(Float, default=0.0)
    legal_score = Column(Float, default=0.0)
    audit_score = Column(Float, default=0.0)
    
    # Overall
    total_score = Column(Float, default=0.0)
    certification_status = Column(String)  # APPROVED, CONDITIONAL, REJECTED
    
    # Details
    validation_details = Column(JSON)
    failures = Column(JSON)
    warnings = Column(JSON)
    
    # Timestamps
    validated_at = Column(DateTime, default=datetime.utcnow)
    validator_version = Column(String, default="2.0")

# ==================== Consent Record Model ====================
class ConsentRecord(Base):
    """Detailed consent tracking for GDPR/PDPA compliance"""
    __tablename__ = "consent_records"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    # Consent Details
    consent_type = Column(String)  # data_collection, commercial_use, ai_training, etc.
    consent_given = Column(Boolean)
    consent_text = Column(Text)
    consent_version = Column(String)
    
    # Verification
    consent_method = Column(String)  # checkbox, explicit, imported
    consent_signature = Column(String)
    
    # Metadata
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Timestamps
    given_at = Column(DateTime, default=datetime.utcnow)
    withdrawn_at = Column(DateTime)
    expires_at = Column(DateTime)

# ==================== Database Functions ====================

def create_tables(database_url: str = None):
    """Create all tables in the database"""
    from src.config import Config
    
    db_url = database_url or Config.DATABASE_URL
    engine = create_engine(db_url, echo=Config.DEBUG)
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database tables created at {db_url}")
    return engine

def get_session(engine=None):
    """Get database session"""
    from src.config import Config
    
    if not engine:
        engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_database():
    """Initialize database with default data"""
    engine = create_tables()
    session = get_session(engine)
    
    # Check if already initialized
    user_count = session.query(User).count()
    if user_count > 0:
        print("ℹ️ Database already initialized")
        return
    
    print("🚀 Database initialized successfully!")
    session.close()

# Helper functions for generating IDs
def generate_wisdom_id(user_id: str, title: str) -> str:
    """Generate unique wisdom drop ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_string = f"{user_id}_{title}_{timestamp}"
    hash_suffix = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    return f"DROP_{hash_suffix.upper()}"

def generate_user_id(username: str) -> str:
    """Generate unique user ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_string = f"{username}_{timestamp}"
    hash_suffix = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    return f"USER_{hash_suffix.upper()}"

def generate_audit_id(user_id: str, action: str) -> str:
    """Generate unique audit log ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_string = f"{user_id}_{action}_{timestamp}"
    hash_suffix = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    return f"AUDIT_{hash_suffix.upper()}"

if __name__ == "__main__":
    # Test database creation
    init_database()
