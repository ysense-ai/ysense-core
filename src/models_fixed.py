from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create base
Base = declarative_base()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ysense.db")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    attribution_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class ConsentRecord(Base):
    __tablename__ = "consents"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    consent_type = Column(String)
    granted = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

def generate_user_id():
    import uuid
    return str(uuid.uuid4())

def generate_audit_id():
    import uuid
    return str(uuid.uuid4())
