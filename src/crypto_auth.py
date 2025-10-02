"""
YSense™ Cryptographic Authentication System
Z Protocol v2.0 Compliant - Crypto Key Based Authentication
"""

import secrets
import hashlib
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import sqlite3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class CryptoAuthManager:
    """Cryptographic authentication manager for YSense™"""
    
    def __init__(self, db_path: str = "ysense_v41.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables for crypto authentication"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create crypto_users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                crypto_key_hash TEXT NOT NULL,
                public_key TEXT NOT NULL,
                private_key_encrypted TEXT NOT NULL,
                tier TEXT DEFAULT 'Standard',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                attribution_count INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0.0
            )
        ''')
        
        # Create crypto_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES crypto_users (id)
            )
        ''')
        
        # Create attribution_keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attribution_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                wisdom_id INTEGER,
                attribution_key TEXT UNIQUE NOT NULL,
                signature TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES crypto_users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_crypto_keypair(self) -> Tuple[str, str]:
        """Generate a new cryptographic keypair"""
        # Generate a random private key (32 bytes)
        private_key = secrets.token_bytes(32)
        
        # Generate public key from private key (simplified approach)
        public_key = hashlib.sha256(private_key).digest()
        
        # Encode keys as base64 strings
        private_key_b64 = base64.b64encode(private_key).decode('utf-8')
        public_key_b64 = base64.b64encode(public_key).decode('utf-8')
        
        return private_key_b64, public_key_b64
    
    def hash_crypto_key(self, crypto_key: str) -> str:
        """Hash crypto key for storage"""
        return hashlib.sha256(crypto_key.encode('utf-8')).hexdigest()
    
    def encrypt_private_key(self, private_key: str, password: str) -> str:
        """Encrypt private key with password"""
        # Generate salt
        salt = secrets.token_bytes(16)
        
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Encrypt private key
        fernet = Fernet(key)
        encrypted_key = fernet.encrypt(private_key.encode())
        
        # Combine salt and encrypted key
        combined = salt + encrypted_key
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt_private_key(self, encrypted_private_key: str, password: str) -> Optional[str]:
        """Decrypt private key with password"""
        try:
            # Decode combined data
            combined = base64.b64decode(encrypted_private_key.encode())
            
            # Extract salt and encrypted key
            salt = combined[:16]
            encrypted_key = combined[16:]
            
            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            # Decrypt private key
            fernet = Fernet(key)
            decrypted_key = fernet.decrypt(encrypted_key)
            
            return decrypted_key.decode('utf-8')
            
        except Exception as e:
            print(f"Decrypt error: {e}")
            return None
    
    def create_user(self, username: str, password: str, tier: str = "Standard") -> Dict[str, Any]:
        """Create new crypto user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if username exists
            cursor.execute('SELECT id FROM crypto_users WHERE username = ?', (username,))
            if cursor.fetchone():
                conn.close()
                return {"success": False, "error": "Username already exists"}
            
            # Generate crypto keypair
            private_key, public_key = self.generate_crypto_keypair()
            
            # Encrypt private key
            encrypted_private_key = self.encrypt_private_key(private_key, password)
            
            # Hash crypto key for storage
            crypto_key_hash = self.hash_crypto_key(private_key)
            
            # Insert user
            cursor.execute('''
                INSERT INTO crypto_users 
                (username, crypto_key_hash, public_key, private_key_encrypted, tier)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, crypto_key_hash, public_key, encrypted_private_key, tier))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "user_id": user_id,
                "username": username,
                "private_key": private_key,  # Return private key for user to save
                "public_key": public_key,
                "tier": tier,
                "message": "User created successfully! Save your private key securely."
            }
            
        except Exception as e:
            return {"success": False, "error": f"Create user error: {e}"}
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with crypto key"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user data
            cursor.execute('''
                SELECT id, username, crypto_key_hash, public_key, private_key_encrypted, 
                       tier, is_active, attribution_count, total_revenue
                FROM crypto_users WHERE username = ? AND is_active = 1
            ''', (username,))
            
            user_data = cursor.fetchone()
            if not user_data:
                conn.close()
                return None
            
            user_id, username, crypto_key_hash, public_key, encrypted_private_key, tier, is_active, attribution_count, total_revenue = user_data
            
            # Decrypt private key to verify password
            decrypted_private_key = self.decrypt_private_key(encrypted_private_key, password)
            if not decrypted_private_key:
                conn.close()
                return None
            
            # Verify crypto key hash
            if self.hash_crypto_key(decrypted_private_key) != crypto_key_hash:
                conn.close()
                return None
            
            # Update last login
            cursor.execute('''
                UPDATE crypto_users SET last_login = ? WHERE id = ?
            ''', (datetime.now(), user_id))
            
            conn.commit()
            conn.close()
            
            return {
                "id": user_id,
                "username": username,
                "public_key": public_key,
                "private_key": decrypted_private_key,
                "tier": tier,
                "attribution_count": attribution_count,
                "total_revenue": total_revenue
            }
            
        except Exception as e:
            print(f"Authenticate error: {e}")
            return None
    
    def generate_session_token(self, user_id: int) -> str:
        """Generate session token for user"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)  # 24 hour expiry
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clean up old sessions
        cursor.execute('DELETE FROM crypto_sessions WHERE expires_at < ?', (datetime.now(),))
        
        # Create new session
        cursor.execute('''
            INSERT INTO crypto_sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, session_token, expires_at))
        
        conn.commit()
        conn.close()
        
        return session_token
    
    def verify_session_token(self, session_token: str) -> Optional[int]:
        """Verify session token and return user_id"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id FROM crypto_sessions 
                WHERE session_token = ? AND expires_at > ?
            ''', (session_token, datetime.now()))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"Verify session error: {e}")
            return None
    
    def generate_attribution_key(self, user_id: int, wisdom_content: str) -> Dict[str, Any]:
        """Generate attribution key for wisdom content"""
        try:
            # Generate unique attribution key
            attribution_key = secrets.token_urlsafe(16)
            
            # Create signature using user's private key
            signature = self._create_signature(user_id, wisdom_content, attribution_key)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store attribution key
            cursor.execute('''
                INSERT INTO attribution_keys 
                (user_id, attribution_key, signature)
                VALUES (?, ?, ?)
            ''', (user_id, attribution_key, signature))
            
            # Update user attribution count
            cursor.execute('''
                UPDATE crypto_users SET attribution_count = attribution_count + 1 
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "attribution_key": attribution_key,
                "signature": signature,
                "message": "Attribution key generated successfully"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Generate attribution key error: {e}"}
    
    def _create_signature(self, user_id: int, content: str, attribution_key: str) -> str:
        """Create cryptographic signature for attribution"""
        try:
            # Get user's private key
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT private_key_encrypted FROM crypto_users WHERE id = ?', (user_id,))
            encrypted_private_key = cursor.fetchone()[0]
            conn.close()
            
            # For now, create a simple signature
            # In production, use proper cryptographic signing
            signature_data = f"{user_id}:{content}:{attribution_key}:{datetime.now().isoformat()}"
            signature = hashlib.sha256(signature_data.encode()).hexdigest()
            
            return signature
            
        except Exception as e:
            print(f"Create signature error: {e}")
            return ""
    
    def verify_attribution(self, attribution_key: str, signature: str) -> bool:
        """Verify attribution key and signature"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, signature FROM attribution_keys 
                WHERE attribution_key = ?
            ''', (attribution_key,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False
            
            stored_signature = result[1]
            return signature == stored_signature
            
        except Exception as e:
            print(f"Verify attribution error: {e}")
            return False
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT username, tier, attribution_count, total_revenue, created_at
                FROM crypto_users WHERE id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {}
            
            username, tier, attribution_count, total_revenue, created_at = result
            
            return {
                "username": username,
                "tier": tier,
                "attribution_count": attribution_count,
                "total_revenue": total_revenue,
                "created_at": created_at,
                "member_since": created_at
            }
            
        except Exception as e:
            print(f"Get user stats error: {e}")
            return {}
    
    def update_user_tier(self, user_id: int, new_tier: str) -> bool:
        """Update user tier"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE crypto_users SET tier = ? WHERE id = ?
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
                UPDATE crypto_users SET is_active = 0 WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Deactivate user error: {e}")
            return False





