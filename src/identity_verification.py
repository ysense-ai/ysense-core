# identity_verification.py
"""
YSense™ Identity Verification & Anti-Fraud System
Prevents duplicate accounts and content gaming
"""

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import secrets
import string
from difflib import SequenceMatcher
import numpy as np

class YSenseIdentityManager:
    """
    Manages user identity, prevents fraud, and tracks revenue attribution
    """
    
    def __init__(self, db_path: str = "ysense_identity.db"):
        self.db_path = db_path
        self._initialize_identity_database()
        
        # Content similarity threshold (80% similar = likely duplicate)
        self.SIMILARITY_THRESHOLD = 0.80
        
        # Device fingerprint components
        self.fingerprint_components = [
            'user_agent', 'screen_resolution', 'timezone', 
            'language', 'platform', 'hardware_concurrency'
        ]
    
    def _initialize_identity_database(self):
        """Create identity and anti-fraud tables"""
        with sqlite3.connect(self.db_path) as conn:
            # User identity table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_identities (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    email_verified INTEGER DEFAULT 0,
                    phone TEXT,
                    phone_verified INTEGER DEFAULT 0,
                    
                    -- Identity verification
                    full_name TEXT NOT NULL,
                    name_hash TEXT NOT NULL,
                    ic_hash TEXT,  -- Hashed IC/passport for Malaysian context
                    country TEXT,
                    
                    -- Device fingerprints
                    primary_device_fingerprint TEXT,
                    known_devices TEXT,  -- JSON array of device fingerprints
                    
                    -- Behavioral patterns
                    writing_style_signature TEXT,
                    avg_session_duration INTEGER,
                    typical_submission_time TEXT,
                    
                    -- Revenue tracking
                    total_revenue REAL DEFAULT 0,
                    total_wisdom_drops INTEGER DEFAULT 0,
                    quality_average REAL DEFAULT 0,
                    
                    -- Security
                    auth_token TEXT,
                    last_login TEXT,
                    login_count INTEGER DEFAULT 0,
                    suspicious_activity_score REAL DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    ban_reason TEXT,
                    
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Content fingerprint table (for duplicate detection)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS content_fingerprints (
                    fingerprint_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    wisdom_id TEXT NOT NULL,
                    
                    -- Content signatures
                    content_hash TEXT NOT NULL,
                    semantic_hash TEXT,
                    structure_hash TEXT,
                    
                    -- Layer hashes (5-Prompt specific)
                    narrative_hash TEXT,
                    somatic_hash TEXT,
                    attention_hash TEXT,
                    synesthetic_hash TEXT,
                    temporal_hash TEXT,
                    
                    -- Metadata
                    word_count INTEGER,
                    unique_words INTEGER,
                    submission_time TEXT,
                    
                    FOREIGN KEY (user_id) REFERENCES user_identities(user_id),
                    UNIQUE(content_hash, user_id)
                )
            ''')
            
            # Fraud detection log
            conn.execute('''
                CREATE TABLE IF NOT EXISTS fraud_detection_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    detection_type TEXT,  -- duplicate_content, multiple_accounts, etc.
                    severity TEXT,  -- low, medium, high, critical
                    details TEXT,  -- JSON with specifics
                    action_taken TEXT,  -- warned, blocked, banned
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # IP and device tracking
            conn.execute('''
                CREATE TABLE IF NOT EXISTS device_tracking (
                    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    ip_address TEXT,
                    device_fingerprint TEXT,
                    browser_fingerprint TEXT,
                    session_id TEXT,
                    location_estimate TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES user_identities(user_id)
                )
            ''')
            
            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_email ON user_identities(email)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_content_hash ON content_fingerprints(content_hash)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_content ON content_fingerprints(user_id)')
            
            conn.commit()
    
    def register_user(self, 
                      email: str,
                      full_name: str,
                      phone: Optional[str] = None,
                      ic_number: Optional[str] = None,
                      country: str = "Malaysia",
                      device_info: Dict = None) -> Tuple[bool, str, str]:
        """
        Register a new user with identity verification
        Returns: (success, user_id/error_message, auth_token)
        """
        
        # Check for existing accounts
        existing = self._check_existing_identity(email, full_name, ic_number)
        if existing:
            return False, f"Account already exists: {existing}", ""
        
        # Generate secure user ID and auth token
        user_id = self._generate_user_id(email, full_name)
        auth_token = self._generate_auth_token()
        
        # Hash sensitive information
        name_hash = hashlib.sha256(full_name.lower().encode()).hexdigest()
        ic_hash = hashlib.sha256(ic_number.encode()).hexdigest() if ic_number else None
        
        # Create device fingerprint
        device_fingerprint = self._create_device_fingerprint(device_info) if device_info else None
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO user_identities (
                        user_id, email, full_name, name_hash,
                        phone, ic_hash, country,
                        primary_device_fingerprint, known_devices,
                        auth_token
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, email, full_name, name_hash,
                    phone, ic_hash, country,
                    device_fingerprint,
                    json.dumps([device_fingerprint] if device_fingerprint else []),
                    auth_token
                ))
                conn.commit()
                
                return True, user_id, auth_token
                
        except sqlite3.IntegrityError as e:
            return False, f"Registration failed: {str(e)}", ""
    
    def verify_user_identity(self, 
                            auth_token: str,
                            device_info: Dict = None) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Verify user identity and check for suspicious activity
        Returns: (is_valid, user_id, user_data)
        """
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM user_identities 
                WHERE auth_token = ? AND is_banned = 0
            ''', (auth_token,))
            
            user = cursor.fetchone()
            
            if not user:
                return False, None, None
            
            user_id = user['user_id']
            
            # Check device fingerprint
            if device_info:
                device_fingerprint = self._create_device_fingerprint(device_info)
                known_devices = json.loads(user['known_devices'] or '[]')
                
                if device_fingerprint not in known_devices:
                    # New device - log it
                    self._log_device_activity(user_id, device_info, device_fingerprint)
                    
                    # Add to known devices if not suspicious
                    if len(known_devices) < 5:  # Allow up to 5 devices
                        known_devices.append(device_fingerprint)
                        conn.execute('''
                            UPDATE user_identities 
                            SET known_devices = ?, updated_at = ?
                            WHERE user_id = ?
                        ''', (json.dumps(known_devices), datetime.now().isoformat(), user_id))
            
            # Update last login
            conn.execute('''
                UPDATE user_identities 
                SET last_login = ?, login_count = login_count + 1
                WHERE user_id = ?
            ''', (datetime.now().isoformat(), user_id))
            
            conn.commit()
            
            return True, user_id, dict(user)
    
    def check_content_duplicate(self, 
                               user_id: str,
                               content: str,
                               layers: Dict[str, str]) -> Tuple[bool, float, Optional[str]]:
        """
        Check if content is duplicate or too similar to existing
        Returns: (is_duplicate, similarity_score, matching_wisdom_id)
        """
        
        # Generate content fingerprints
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Generate layer hashes
        layer_hashes = {
            f"{layer}_hash": hashlib.md5(text.encode()).hexdigest()[:16]
            for layer, text in layers.items() if text
        }
        
        with sqlite3.connect(self.db_path) as conn:
            # Check for exact duplicate
            cursor = conn.execute('''
                SELECT wisdom_id FROM content_fingerprints 
                WHERE content_hash = ?
            ''', (content_hash,))
            
            exact_match = cursor.fetchone()
            if exact_match:
                # Log fraud attempt
                self._log_fraud_attempt(
                    user_id, 
                    'duplicate_content', 
                    'high',
                    {'wisdom_id': exact_match[0], 'type': 'exact_duplicate'}
                )
                return True, 1.0, exact_match[0]
            
            # Check for similar content (fuzzy matching)
            cursor = conn.execute('''
                SELECT cf.wisdom_id, cf.content_hash, wd.raw_story
                FROM content_fingerprints cf
                JOIN wisdom_drops wd ON cf.wisdom_id = wd.id
                WHERE cf.user_id = ? OR cf.user_id != ?
                ORDER BY cf.submission_time DESC
                LIMIT 100
            ''', (user_id, user_id))
            
            for row in cursor:
                if 'raw_story' in row:
                    similarity = self._calculate_similarity(content, row['raw_story'])
                    
                    if similarity > self.SIMILARITY_THRESHOLD:
                        # Too similar - likely duplicate
                        self._log_fraud_attempt(
                            user_id,
                            'similar_content',
                            'medium' if row['user_id'] == user_id else 'high',
                            {
                                'wisdom_id': row['wisdom_id'],
                                'similarity': similarity,
                                'is_same_user': row['user_id'] == user_id
                            }
                        )
                        return True, similarity, row['wisdom_id']
        
        return False, 0.0, None
    
    def save_content_fingerprint(self, 
                                user_id: str,
                                wisdom_id: str,
                                content: str,
                                layers: Dict[str, str]):
        """Save content fingerprint for future duplicate detection"""
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        word_count = len(content.split())
        unique_words = len(set(content.lower().split()))
        
        fingerprint_id = f"FP_{wisdom_id}"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO content_fingerprints (
                    fingerprint_id, user_id, wisdom_id,
                    content_hash, word_count, unique_words,
                    narrative_hash, somatic_hash, attention_hash,
                    synesthetic_hash, temporal_hash,
                    submission_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fingerprint_id, user_id, wisdom_id,
                content_hash, word_count, unique_words,
                hashlib.md5(layers.get('narrative', '').encode()).hexdigest()[:16],
                hashlib.md5(layers.get('somatic', '').encode()).hexdigest()[:16],
                hashlib.md5(layers.get('attention', '').encode()).hexdigest()[:16],
                hashlib.md5(layers.get('synesthetic', '').encode()).hexdigest()[:16],
                hashlib.md5(layers.get('temporal_auditory', '').encode()).hexdigest()[:16],
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def check_multiple_accounts(self, 
                              email: str,
                              full_name: str,
                              device_info: Dict = None) -> List[str]:
        """
        Check if user has multiple accounts
        Returns list of suspected linked account IDs
        """
        
        linked_accounts = []
        
        with sqlite3.connect(self.db_path) as conn:
            # Check by email domain and name similarity
            email_domain = email.split('@')[1]
            name_parts = full_name.lower().split()
            
            cursor = conn.execute('''
                SELECT user_id, email, full_name, primary_device_fingerprint
                FROM user_identities
                WHERE email LIKE ? OR name_hash = ?
            ''', (f'%@{email_domain}', hashlib.sha256(full_name.lower().encode()).hexdigest()))
            
            for row in cursor:
                # Check name similarity
                name_similarity = self._calculate_similarity(
                    full_name.lower(), 
                    row['full_name'].lower()
                )
                
                if name_similarity > 0.85:
                    linked_accounts.append(row['user_id'])
            
            # Check by device fingerprint
            if device_info and linked_accounts:
                device_fingerprint = self._create_device_fingerprint(device_info)
                
                cursor = conn.execute('''
                    SELECT DISTINCT user_id 
                    FROM device_tracking
                    WHERE device_fingerprint = ?
                ''', (device_fingerprint,))
                
                for row in cursor:
                    if row['user_id'] not in linked_accounts:
                        linked_accounts.append(row['user_id'])
        
        return linked_accounts
    
    def get_user_revenue_summary(self, user_id: str) -> Dict:
        """Get complete revenue summary for a user"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get user data
            cursor = conn.execute('''
                SELECT * FROM user_identities WHERE user_id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            
            if not user:
                return {}
            
            # Get wisdom drops from main database
            from database_manager import YSenseDatabase
            wisdom_db = YSenseDatabase()
            all_drops = wisdom_db.get_all_wisdom_drops()
            
            # Filter by author (assuming author field matches full_name)
            user_drops = [d for d in all_drops 
                         if d.get('author', '').lower() == user['full_name'].lower()]
            
            total_revenue = sum(d.get('revenue_potential', 0) for d in user_drops)
            total_drops = len(user_drops)
            avg_quality = sum(d.get('quality_score', 0) for d in user_drops) / max(total_drops, 1)
            
            # Update user record
            conn.execute('''
                UPDATE user_identities 
                SET total_revenue = ?, total_wisdom_drops = ?, quality_average = ?
                WHERE user_id = ?
            ''', (total_revenue, total_drops, avg_quality, user_id))
            
            return {
                'user_id': user_id,
                'full_name': user['full_name'],
                'email': user['email'],
                'total_revenue': total_revenue,
                'total_wisdom_drops': total_drops,
                'average_quality': avg_quality,
                'is_verified': bool(user['email_verified']),
                'member_since': user['created_at'],
                'suspicious_score': user['suspicious_activity_score']
            }
    
    def _check_existing_identity(self, email: str, full_name: str, ic_number: str = None) -> Optional[str]:
        """Check if identity already exists"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Check by email
            cursor = conn.execute('SELECT user_id FROM user_identities WHERE email = ?', (email,))
            if cursor.fetchone():
                return "Email already registered"
            
            # Check by IC hash if provided
            if ic_number:
                ic_hash = hashlib.sha256(ic_number.encode()).hexdigest()
                cursor = conn.execute('SELECT user_id FROM user_identities WHERE ic_hash = ?', (ic_hash,))
                if cursor.fetchone():
                    return "IC number already registered"
            
            # Check by name hash (exact match)
            name_hash = hashlib.sha256(full_name.lower().encode()).hexdigest()
            cursor = conn.execute('SELECT user_id FROM user_identities WHERE name_hash = ?', (name_hash,))
            if cursor.fetchone():
                return "Name already registered"
        
        return None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity score (0-1)"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _create_device_fingerprint(self, device_info: Dict) -> str:
        """Create unique device fingerprint"""
        if not device_info:
            return ""
        
        fingerprint_data = []
        for component in self.fingerprint_components:
            fingerprint_data.append(str(device_info.get(component, 'unknown')))
        
        fingerprint_string = '|'.join(fingerprint_data)
        return hashlib.md5(fingerprint_string.encode()).hexdigest()
    
    def _generate_user_id(self, email: str, full_name: str) -> str:
        """Generate unique user ID"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{email}_{full_name}_{timestamp}"
        return f"USER_{hashlib.sha256(unique_string.encode()).hexdigest()[:12].upper()}"
    
    def _generate_auth_token(self) -> str:
        """Generate secure authentication token"""
        return secrets.token_urlsafe(32)
    
    def _log_fraud_attempt(self, user_id: str, detection_type: str, severity: str, details: Dict):
        """Log potential fraud attempt"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO fraud_detection_log (
                    user_id, detection_type, severity, details, action_taken
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id, detection_type, severity, 
                json.dumps(details), 'logged'
            ))
            
            # Update user's suspicious activity score
            if severity == 'high':
                score_increase = 0.5
            elif severity == 'medium':
                score_increase = 0.3
            else:
                score_increase = 0.1
            
            conn.execute('''
                UPDATE user_identities 
                SET suspicious_activity_score = suspicious_activity_score + ?
                WHERE user_id = ?
            ''', (score_increase, user_id))
            
            # Auto-ban if score too high
            cursor = conn.execute('''
                SELECT suspicious_activity_score FROM user_identities
                WHERE user_id = ?
            ''', (user_id,))
            
            score = cursor.fetchone()[0]
            if score >= 2.0:  # Ban threshold
                conn.execute('''
                    UPDATE user_identities 
                    SET is_banned = 1, ban_reason = ?
                    WHERE user_id = ?
                ''', ('Excessive suspicious activity', user_id))
            
            conn.commit()
    
    def _log_device_activity(self, user_id: str, device_info: Dict, fingerprint: str):
        """Log device access for security tracking"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO device_tracking (
                    user_id, ip_address, device_fingerprint,
                    browser_fingerprint, session_id
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                device_info.get('ip_address', ''),
                fingerprint,
                device_info.get('browser', ''),
                device_info.get('session_id', '')
            ))
            conn.commit()


# Integration with main platform
class SecureWisdomProcessor:
    """
    Wrapper that adds identity verification to wisdom processing
    """
    
    def __init__(self):
        self.identity_manager = YSenseIdentityManager()
        from database_manager import YSenseDatabase
        self.wisdom_db = YSenseDatabase()
    
    def submit_wisdom_with_verification(self,
                                       auth_token: str,
                                       content: str,
                                       layers: Dict,
                                       device_info: Dict = None) -> Tuple[bool, str]:
        """
        Submit wisdom with full identity and fraud checking
        """
        
        # Verify user identity
        is_valid, user_id, user_data = self.identity_manager.verify_user_identity(
            auth_token, device_info
        )
        
        if not is_valid:
            return False, "Invalid authentication or account banned"
        
        # Check for duplicate content
        is_duplicate, similarity, matching_id = self.identity_manager.check_content_duplicate(
            user_id, content, layers
        )
        
        if is_duplicate:
            return False, f"Content too similar to existing wisdom (similarity: {similarity:.1%})"
        
        # Process wisdom (your existing logic)
        # ... create wisdom drop ...
        
        # Save content fingerprint
        wisdom_id = "generated_wisdom_id"  # From your wisdom creation
        self.identity_manager.save_content_fingerprint(
            user_id, wisdom_id, content, layers
        )
        
        return True, wisdom_id


# Example usage
if __name__ == "__main__":
    manager = YSenseIdentityManager()
    
    # Register user
    success, user_id, token = manager.register_user(
        email="alton@ysense.org",
        full_name="Alton Lee Wei Bin",
        ic_number="123456789012",  # Hashed, never stored in plain
        country="Malaysia",
        device_info={
            'user_agent': 'Mozilla/5.0...',
            'screen_resolution': '1920x1080',
            'timezone': 'Asia/Kuala_Lumpur'
        }
    )
    
    if success:
        print(f"✅ User registered: {user_id}")
        print(f"🔑 Auth token: {token}")
        
        # Get revenue summary
        summary = manager.get_user_revenue_summary(user_id)
        print(f"💰 Revenue: €{summary['total_revenue']:.2f}")