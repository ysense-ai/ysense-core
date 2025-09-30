"""
YSense™ Authentication Manager
Handles user registration, login, and session management
"""

import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass
import jwt
import os

@dataclass
class User:
    """User data class"""
    id: int
    email: str
    password_hash: str
    tier: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

class AuthManager:
    """Authentication manager for YSense platform"""
    
    def __init__(self, db_path: str = "ysense_local.db"):
        self.db_path = db_path
        self.secret_key = os.getenv('SECRET_KEY', 'ysense-secret-key-change-in-production')
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                tier TEXT DEFAULT 'Standard',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                email_verified BOOLEAN DEFAULT 0
            )
        ''')
        
        # Create password reset tokens table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create email verification tokens table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_verification_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_part = password_hash.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
        except:
            return False
    
    def register_user(self, email: str, password: str, tier: str = "Standard") -> Optional[User]:
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                conn.close()
                return None
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (email, password_hash, tier, created_at)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, tier, datetime.now()))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return User(
                id=user_id,
                email=email,
                password_hash=password_hash,
                tier=tier,
                created_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Registration error: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user
            cursor.execute('''
                SELECT id, email, password_hash, tier, created_at, last_login, is_active
                FROM users WHERE email = ? AND is_active = 1
            ''', (email,))
            
            row = cursor.fetchone()
            if not row:
                conn.close()
                return None
            
            user_id, user_email, password_hash, tier, created_at, last_login, is_active = row
            
            # Verify password
            if not self.verify_password(password, password_hash):
                conn.close()
                return None
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            conn.close()
            
            return User(
                id=user_id,
                email=user_email,
                password_hash=password_hash,
                tier=tier,
                created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                last_login=datetime.now(),
                is_active=bool(is_active)
            )
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, password_hash, tier, created_at, last_login, is_active
                FROM users WHERE id = ? AND is_active = 1
            ''', (user_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            user_id, user_email, password_hash, tier, created_at, last_login, is_active = row
            
            return User(
                id=user_id,
                email=user_email,
                password_hash=password_hash,
                tier=tier,
                created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                last_login=datetime.fromisoformat(last_login) if last_login and isinstance(last_login, str) else last_login,
                is_active=bool(is_active)
            )
            
        except Exception as e:
            print(f"Get user error: {e}")
            return None
    
    def generate_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'tier': user.tier,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def update_user_tier(self, user_id: int, new_tier: str) -> bool:
        """Update user tier"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET tier = ? WHERE id = ?
            ''', (new_tier, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Update tier error: {e}")
            return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET is_active = 0 WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Deactivate user error: {e}")
            return False
    
    def generate_password_reset_token(self, email: str) -> Optional[str]:
        """Generate password reset token"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE email = ? AND is_active = 1', (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return None
            
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)  # 1 hour expiry
            
            # Store reset token
            cursor.execute('''
                INSERT OR REPLACE INTO password_reset_tokens 
                (user_id, token, expires_at, created_at)
                VALUES (?, ?, ?, ?)
            ''', (user[0], reset_token, expires_at, datetime.now()))
            
            conn.commit()
            conn.close()
            
            return reset_token
            
        except Exception as e:
            print(f"Generate reset token error: {e}")
            return None
    
    def verify_password_reset_token(self, token: str) -> Optional[int]:
        """Verify password reset token and return user_id"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id FROM password_reset_tokens 
                WHERE token = ? AND expires_at > ? AND used = 0
            ''', (token, datetime.now()))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"Verify reset token error: {e}")
            return None
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password using token"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verify token
            user_id = self.verify_password_reset_token(token)
            if not user_id:
                conn.close()
                return False
            
            # Hash new password
            password_hash = self.hash_password(new_password)
            
            # Update password
            cursor.execute('''
                UPDATE users SET password_hash = ? WHERE id = ?
            ''', (password_hash, user_id))
            
            # Mark token as used
            cursor.execute('''
                UPDATE password_reset_tokens SET used = 1 WHERE token = ?
            ''', (token,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Reset password error: {e}")
            return False
