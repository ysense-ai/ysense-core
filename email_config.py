# 📧 YSense Platform v4.0 - Email Configuration

# Add to src/config.py

class Config:
    # ... existing configuration ...
    
    # Email Configuration for Key Recovery
    SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
    SMTP_PORT = 587
    SMTP_USERNAME = "your-email@gmail.com"  # Change to your email
    SMTP_PASSWORD = "your-app-password"  # Change to your app password
    FROM_EMAIL = "noreply@ysense.ai"  # Change to your from email
    
    # Recovery Settings
    MAX_RECOVERY_ATTEMPTS_PER_HOUR = 3
    RECOVERY_EMAIL_COOLDOWN_MINUTES = 60
    RECOVERY_ENABLED = True
    
    # Email Templates
    RECOVERY_EMAIL_TEMPLATE = """
    Dear {username},
    
    You requested recovery of your {key_type} for your YSense account.
    
    Your {key_type}: {key_value}
    
    IMPORTANT SECURITY NOTES:
    - This key is unique to your account
    - Keep it secure and don't share it
    - You can use this key to access your account
    - Consider generating a new key for enhanced security
    
    If you didn't request this recovery, please contact support immediately.
    
    Best regards,
    YSense Platform Team
    """
    
    # Security Settings
    KEY_ROTATION_ENABLED = True
    KEY_EXPIRY_DAYS = 365
    FORCE_KEY_ROTATION = False



