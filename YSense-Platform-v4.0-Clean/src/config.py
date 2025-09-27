# src/config.py
"""
YSense Platform v3.0 Configuration
Central configuration management with secure environment variable loading
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"⚠️  Warning: .env file not found at {env_path}")

class Config:
    """Platform configuration from environment variables"""
    
    # ==================== Core Settings ====================
    PLATFORM_VERSION = os.getenv('PLATFORM_VERSION', '3.0')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # ==================== API Keys ====================
    # NEVER put actual keys here - they must be in .env file
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # ==================== Security ====================
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', secrets.token_hex(32))
    
    # ==================== Database ====================
    USE_POSTGRESQL = os.getenv('USE_POSTGRESQL', 'false').lower() == 'true'
    if USE_POSTGRESQL:
        DATABASE_URL = os.getenv('DATABASE_URL', 
                                 'postgresql://ysense:password@localhost:5432/ysense_dev')
    else:
        DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ysense_local.db')
    
    # ==================== Redis (Optional) ====================
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    USE_REDIS = os.getenv('USE_REDIS', 'false').lower() == 'true'
    
    # ==================== Revenue Settings ====================
    BASE_RATE_EUR = float(os.getenv('BASE_RATE_EUR', '0.10'))
    PLATFORM_FEE_PERCENTAGE = float(os.getenv('PLATFORM_FEE_PERCENTAGE', '15'))
    COMMUNITY_SHARE_PERCENTAGE = float(os.getenv('COMMUNITY_SHARE_PERCENTAGE', '15'))
    
    # ==================== Z Protocol Configuration ====================
    Z_PROTOCOL_VERSION = os.getenv('Z_PROTOCOL_VERSION', '2.0')
    ENABLE_Z_PROTOCOL = os.getenv('ENABLE_Z_PROTOCOL', 'true').lower() == 'true'
    
    # Z Protocol Tiers with revenue sharing percentages
    Z_PROTOCOL_TIERS = {
        1: {
            "name": "Bronze",
            "multiplier": 1.0,
            "consent_required": True,
            "revenue_share": 30.0
        },
        2: {
            "name": "Silver",
            "multiplier": 1.1,
            "consent_required": True,
            "revenue_share": 35.0
        },
        3: {
            "name": "Gold",
            "multiplier": 1.2,
            "consent_required": True,
            "revenue_share": 40.0
        },
        4: {
            "name": "Platinum",
            "multiplier": 1.3,
            "consent_required": True,
            "revenue_share": 45.0
        },
        5: {
            "name": "Diamond",
            "multiplier": 1.5,
            "consent_required": True,
            "revenue_share": 50.0
        }
    }
    
    # ==================== Defensive Publication ====================
    DEFENSIVE_PUBLICATION_DOI = os.getenv('DEFENSIVE_PUBLICATION_DOI', 
                                          '10.5281/zenodo.17072168')
    
    # ==================== Feature Flags ====================
    ENABLE_MCP_SERVER = os.getenv('ENABLE_MCP_SERVER', 'false').lower() == 'true'
    ENABLE_DUAL_MODEL = os.getenv('ENABLE_DUAL_MODEL', 'true').lower() == 'true'
    ENABLE_AGENT_ORCHESTRATION = os.getenv('ENABLE_AGENT_ORCHESTRATION', 
                                           'false').lower() == 'true'
    
    # ==================== API Settings ====================
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8000'))
    UI_PORT = int(os.getenv('UI_PORT', '8501'))
    CORS_ALLOW_ALL = os.getenv('CORS_ALLOW_ALL', 'true').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',') if not CORS_ALLOW_ALL else ['*']
    
    # ==================== Email Settings (Optional) ====================
    SMTP_HOST = os.getenv('SMTP_HOST')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@ysense.ai')
    
    # ==================== Google Cloud (Future) ====================
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
    GCP_REGION = os.getenv('GCP_REGION', 'asia-southeast1')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
    
    @classmethod
    def validate(cls, strict=False):
        """
        Validate configuration
        Args:
            strict: If True, require all API keys. If False, allow missing for dev
        """
        warnings = []
        errors = []
        
        # Check API keys (warnings in dev mode, errors in production)
        if not cls.QWEN_API_KEY:
            msg = "QWEN API key not configured"
            if strict or cls.ENVIRONMENT == 'production':
                errors.append(msg)
            else:
                warnings.append(msg)
        elif cls.QWEN_API_KEY.startswith('sk-your'):
            errors.append("QWEN API key is still a placeholder")
        
        if not cls.ANTHROPIC_API_KEY:
            msg = "Anthropic API key not configured"
            if strict or cls.ENVIRONMENT == 'production':
                errors.append(msg)
            else:
                warnings.append(msg)
        elif cls.ANTHROPIC_API_KEY.startswith('sk-ant-your'):
            errors.append("Anthropic API key is still a placeholder")
        
        # Check security keys
        if len(cls.SECRET_KEY) < 32:
            warnings.append("SECRET_KEY should be at least 32 characters")
        
        # Display warnings
        if warnings:
            print("\n⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"   - {warning}")
        
        # Display errors
        if errors:
            print("\n❌ Configuration Errors:")
            for error in errors:
                print(f"   - {error}")
            if strict:
                return False
        
        if not warnings and not errors:
            print("✅ Configuration validated successfully!")
        
        return len(errors) == 0
    
    @classmethod
    def display(cls):
        """Display current configuration (hiding sensitive data)"""
        print("\n" + "="*60)
        print("📋 YSense Platform v3.0 Configuration")
        print("="*60)
        
        print("\n🔧 Core Settings:")
        print(f"   Platform Version: {cls.PLATFORM_VERSION}")
        print(f"   Environment: {cls.ENVIRONMENT}")
        print(f"   Debug Mode: {cls.DEBUG}")
        print(f"   Log Level: {cls.LOG_LEVEL}")
        
        print("\n🗄️  Database:")
        print(f"   Type: {'PostgreSQL' if cls.USE_POSTGRESQL else 'SQLite'}")
        print(f"   URL: {cls.DATABASE_URL[:30]}...")
        
        print("\n🔑 API Keys:")
        print(f"   QWEN: {'✅ Configured' if cls.QWEN_API_KEY else '⚠️  Not configured'}")
        print(f"   Anthropic: {'✅ Configured' if cls.ANTHROPIC_API_KEY else '⚠️  Not configured'}")
        
        print("\n🛡️  Security:")
        print(f"   JWT Algorithm: {cls.JWT_ALGORITHM}")
        print(f"   JWT Expiration: {cls.JWT_EXPIRATION_HOURS} hours")
        print(f"   Secret Key: {'✅ Generated' if cls.SECRET_KEY else '❌ Missing'}")
        
        print("\n💰 Revenue Settings:")
        print(f"   Base Rate: €{cls.BASE_RATE_EUR}")
        print(f"   Platform Fee: {cls.PLATFORM_FEE_PERCENTAGE}%")
        print(f"   Community Share: {cls.COMMUNITY_SHARE_PERCENTAGE}%")
        
        print("\n🎯 Z Protocol:")
        print(f"   Version: {cls.Z_PROTOCOL_VERSION}")
        print(f"   Enabled: {cls.ENABLE_Z_PROTOCOL}")
        print(f"   Tiers: {', '.join([tier['name'] for tier in cls.Z_PROTOCOL_TIERS.values()])}")
        
        print("\n📚 Defensive Publication:")
        print(f"   DOI: {cls.DEFENSIVE_PUBLICATION_DOI}")
        
        print("\n🌐 API Settings:")
        print(f"   Host: {cls.API_HOST}:{cls.API_PORT}")
        print(f"   CORS: {'All Origins' if cls.CORS_ALLOW_ALL else 'Restricted'}")
        
        print("\n" + "="*60)
    
    @classmethod
    def get_tier_info(cls, level: int):
        """Get information about a specific Z Protocol tier"""
        return cls.Z_PROTOCOL_TIERS.get(level, cls.Z_PROTOCOL_TIERS[1])
    
    @classmethod
    def is_production(cls):
        """Check if running in production mode"""
        return cls.ENVIRONMENT.lower() == 'production'
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return cls.ENVIRONMENT.lower() == 'development'

# Example usage and testing
if __name__ == "__main__":
    # Display configuration
    Config.display()
    
    # Validate (non-strict for development)
    is_valid = Config.validate(strict=False)
    
    if is_valid:
        print("\n✅ Configuration is ready for development!")
    else:
        print("\n⚠️  Please update your .env file with the required values")