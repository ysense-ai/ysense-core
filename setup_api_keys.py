# API Configuration Script for YSense™ v4.1
# Run this script to set up your API keys

import os
import sys

def create_env_file():
    """Create .env file with API keys"""
    
    print("🔧 YSense™ v4.1 API Configuration")
    print("=" * 50)
    
    # Get API keys from user
    print("\n📋 Please enter your API keys:")
    
    # QWEN API Key
    qwen_key = input("\n🔑 QWEN API Key (from Alibaba Cloud): ").strip()
    if not qwen_key:
        print("⚠️ QWEN API Key is required!")
        return False
    
    # Anthropic API Key  
    anthropic_key = input("🔑 Anthropic API Key (from Claude Console): ").strip()
    if not anthropic_key:
        print("⚠️ Anthropic API Key is required!")
        return False
    
    # Create .env content
    env_content = f"""# YSense™ Platform v4.1 Environment Configuration
# Generated on {os.popen('date').read().strip()}

# =============================================================================
# AI API KEYS
# =============================================================================

# QWEN API (Alibaba Cloud)
QWEN_API_KEY={qwen_key}
QWEN_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
QWEN_MODEL=qwen-turbo

# Anthropic API (Claude)
ANTHROPIC_API_KEY={anthropic_key}
ANTHROPIC_MODEL=claude-3-sonnet

# =============================================================================
# SECURITY KEYS
# =============================================================================

# JWT Secret Key
JWT_SECRET_KEY=ysense_jwt_secret_key_2025_v41_secure_random_string

# Encryption Key
ENCRYPTION_KEY=ysense_encryption_key_2025_v41_secure_random_string

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Database Path
DATABASE_PATH=ysense_v41.db

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# SMTP Configuration (for future use)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=contact@ysenseai.org
SMTP_PASSWORD=your_email_password_here

# Email Addresses
FROM_EMAIL=contact@ysenseai.org
SUPPORT_EMAIL=support@ysenseai.org
ADMIN_EMAIL=admin@ysenseai.org

# =============================================================================
# PLATFORM CONFIGURATION
# =============================================================================

# Platform URL
PLATFORM_URL=https://ysenseai.org

# Debug Mode
DEBUG=True
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print("📁 Location: YSense-Platform-v4.1-Fresh/.env")
        
        # Test API keys
        print("\n🧪 Testing API keys...")
        test_api_keys(qwen_key, anthropic_key)
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_api_keys(qwen_key, anthropic_key):
    """Test API keys"""
    
    # Test QWEN API
    try:
        import httpx
        headers = {
            'Authorization': f'Bearer {qwen_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [{"role": "user", "content": "Hello"}]
            }
        }
        
        response = httpx.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ QWEN API Key: Valid")
        else:
            print(f"❌ QWEN API Key: Invalid (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ QWEN API Key: Error testing - {e}")
    
    # Test Anthropic API
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Simple test message
        message = client.messages.create(
            model="claude-3-sonnet",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        print("✅ Anthropic API Key: Valid")
        
    except Exception as e:
        print(f"❌ Anthropic API Key: Error testing - {e}")

def main():
    """Main function"""
    print("🚀 YSense™ v4.1 API Configuration Tool")
    print("This will create a .env file with your API keys")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("\n⚠️ .env file already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("❌ Configuration cancelled")
            return
    
    # Create .env file
    if create_env_file():
        print("\n🎉 Configuration complete!")
        print("\n📋 Next steps:")
        print("1. Restart the YSense platform")
        print("2. Go to AI Workflow")
        print("3. Test with a story/idea")
        print("4. Should now use real APIs!")
    else:
        print("\n❌ Configuration failed!")

if __name__ == "__main__":
    main()





