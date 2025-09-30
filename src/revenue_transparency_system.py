"""
YSense™ Revenue Transparency & Anti-Gaming System
Handles revenue distribution, duplicate detection, and contributor analytics
"""

import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import json
import re
from collections import defaultdict

@dataclass
class RevenueShare:
    """Revenue share data class"""
    contributor_id: int
    contributor_email: str
    tier: str
    wisdom_id: int
    wisdom_title: str
    revenue_amount: float
    share_percentage: float
    payment_status: str
    created_at: datetime
    paid_at: Optional[datetime] = None

@dataclass
class ContentFingerprint:
    """Content fingerprint for duplicate detection"""
    content_hash: str
    semantic_hash: str
    wisdom_id: int
    contributor_id: int
    similarity_score: float
    created_at: datetime

class RevenueTransparencySystem:
    """Revenue transparency and anti-gaming protection system"""
    
    def __init__(self, db_path: str = "database/ysense_local.db"):
        self.db_path = db_path
        # Ensure database folder exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.revenue_tiers = {
            "Founding Contributor": 100.0,  # 100% revenue share
            "Partnership": 80.0,            # 80% revenue share
            "Developer": 70.0,              # 70% revenue share
            "Cultural Guardian": 60.0,      # 60% revenue share
            "Standard": 50.0,                # 50% revenue share
            "Basic": 30.0                   # 30% revenue share
        }
        self.init_db()
    
    def init_db(self):
        """Initialize database tables for revenue and anti-gaming"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Revenue shares table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor_id INTEGER NOT NULL,
                contributor_email TEXT NOT NULL,
                tier TEXT NOT NULL,
                wisdom_id INTEGER NOT NULL,
                wisdom_title TEXT NOT NULL,
                revenue_amount REAL NOT NULL,
                share_percentage REAL NOT NULL,
                payment_status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_at TIMESTAMP,
                FOREIGN KEY (contributor_id) REFERENCES users (id),
                FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops (id)
            )
        ''')
        
        # Content fingerprints table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT NOT NULL,
                semantic_hash TEXT NOT NULL,
                wisdom_id INTEGER NOT NULL,
                contributor_id INTEGER NOT NULL,
                similarity_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops (id),
                FOREIGN KEY (contributor_id) REFERENCES users (id)
            )
        ''')
        
        # Contributor analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contributor_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor_id INTEGER NOT NULL,
                total_wisdom_count INTEGER DEFAULT 0,
                total_revenue_earned REAL DEFAULT 0.0,
                total_views INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tier TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contributor_id) REFERENCES users (id)
            )
        ''')
        
        # Anti-gaming violations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anti_gaming_violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contributor_id INTEGER NOT NULL,
                violation_type TEXT NOT NULL,
                violation_description TEXT NOT NULL,
                wisdom_id INTEGER,
                similarity_score REAL,
                penalty_amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (contributor_id) REFERENCES users (id),
                FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_content_fingerprint(self, content: str) -> Tuple[str, str]:
        """Generate content fingerprint for duplicate detection"""
        # Basic hash for exact duplicates
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Semantic hash for similar content detection
        # Remove common words, normalize text, and create semantic fingerprint
        normalized_content = self._normalize_content(content)
        semantic_hash = hashlib.sha256(normalized_content.encode('utf-8')).hexdigest()
        
        return content_hash, semantic_hash
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for semantic comparison"""
        # Convert to lowercase
        content = content.lower()
        
        # Remove common words (stop words)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Remove punctuation and extra whitespace
        content = re.sub(r'[^\w\s]', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Remove stop words
        words = content.split()
        filtered_words = [word for word in words if word not in stop_words]
        
        return ' '.join(filtered_words)
    
    def detect_duplicate_content(self, content: str, contributor_id: int) -> Dict[str, Any]:
        """Detect duplicate or similar content"""
        content_hash, semantic_hash = self.generate_content_fingerprint(content)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for exact duplicates
        cursor.execute('''
            SELECT wisdom_id, contributor_id, created_at
            FROM content_fingerprints 
            WHERE content_hash = ?
        ''', (content_hash,))
        
        exact_duplicates = cursor.fetchall()
        
        # Check for semantic similarities
        cursor.execute('''
            SELECT wisdom_id, contributor_id, similarity_score, created_at
            FROM content_fingerprints 
            WHERE semantic_hash = ? AND contributor_id != ?
        ''', (semantic_hash, contributor_id))
        
        semantic_similarities = cursor.fetchall()
        
        conn.close()
        
        # Calculate similarity score
        similarity_score = 0.0
        if exact_duplicates:
            similarity_score = 100.0
        elif semantic_similarities:
            # Calculate semantic similarity based on content analysis
            similarity_score = self._calculate_semantic_similarity(content, semantic_similarities)
        
        return {
            "is_duplicate": len(exact_duplicates) > 0,
            "is_similar": similarity_score > 70.0,
            "similarity_score": similarity_score,
            "exact_duplicates": exact_duplicates,
            "semantic_similarities": semantic_similarities,
            "content_hash": content_hash,
            "semantic_hash": semantic_hash
        }
    
    def _calculate_semantic_similarity(self, content: str, similarities: List) -> float:
        """Calculate semantic similarity score"""
        # This is a simplified version - in production, you'd use more sophisticated NLP
        base_score = 0.0
        
        for similarity in similarities:
            wisdom_id, contributor_id, existing_score, created_at = similarity
            
            # Check if content is from the same contributor (potential self-plagiarism)
            if contributor_id == contributor_id:
                base_score += 20.0
            
            # Check recency (more recent duplicates are more suspicious)
            if isinstance(created_at, str):
                created_date = datetime.fromisoformat(created_at)
            else:
                created_date = created_at
            
            days_ago = (datetime.now() - created_date).days
            if days_ago < 30:  # Recent content
                base_score += 15.0
            elif days_ago < 90:  # Moderately recent
                base_score += 10.0
        
        return min(base_score, 100.0)
    
    def register_content_fingerprint(self, content: str, wisdom_id: int, contributor_id: int) -> bool:
        """Register content fingerprint for future duplicate detection"""
        try:
            content_hash, semantic_hash = self.generate_content_fingerprint(content)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO content_fingerprints 
                (content_hash, semantic_hash, wisdom_id, contributor_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (content_hash, semantic_hash, wisdom_id, contributor_id, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Register fingerprint error: {e}")
            return False
    
    def calculate_revenue_share(self, wisdom_id: int, contributor_id: int, 
                              total_revenue: float, tier: str) -> Dict[str, Any]:
        """Calculate revenue share for a wisdom contribution"""
        try:
            # Get tier percentage
            share_percentage = self.revenue_tiers.get(tier, 50.0)
            
            # Calculate share amount
            share_amount = (total_revenue * share_percentage) / 100.0
            
            # Get wisdom details
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT title, author_email FROM wisdom_drops WHERE id = ?
            ''', (wisdom_id,))
            
            wisdom_data = cursor.fetchone()
            if not wisdom_data:
                return {"error": "Wisdom not found"}
            
            title, author_email = wisdom_data
            
            # Create revenue share record
            cursor.execute('''
                INSERT INTO revenue_shares 
                (contributor_id, contributor_email, tier, wisdom_id, wisdom_title, 
                 revenue_amount, share_percentage, payment_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (contributor_id, author_email, tier, wisdom_id, title, 
                  share_amount, share_percentage, 'pending', datetime.now()))
            
            revenue_share_id = cursor.lastrowid
            
            # Update contributor analytics
            self._update_contributor_analytics(contributor_id, tier, share_amount)
            
            conn.commit()
            conn.close()
            
            return {
                "revenue_share_id": revenue_share_id,
                "contributor_id": contributor_id,
                "tier": tier,
                "wisdom_id": wisdom_id,
                "share_amount": share_amount,
                "share_percentage": share_percentage,
                "total_revenue": total_revenue,
                "payment_status": "pending"
            }
            
        except Exception as e:
            print(f"Calculate revenue share error: {e}")
            return {"error": str(e)}
    
    def _update_contributor_analytics(self, contributor_id: int, tier: str, revenue_amount: float):
        """Update contributor analytics with new revenue"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if contributor analytics exist
            cursor.execute('''
                SELECT id FROM contributor_analytics WHERE contributor_id = ?
            ''', (contributor_id,))
            
            if cursor.fetchone():
                # Update existing analytics
                cursor.execute('''
                    UPDATE contributor_analytics 
                    SET total_revenue_earned = total_revenue_earned + ?,
                        total_wisdom_count = total_wisdom_count + 1,
                        last_activity = ?,
                        tier = ?
                    WHERE contributor_id = ?
                ''', (revenue_amount, datetime.now(), tier, contributor_id))
            else:
                # Create new analytics record
                cursor.execute('''
                    INSERT INTO contributor_analytics 
                    (contributor_id, total_wisdom_count, total_revenue_earned, 
                     tier, last_activity, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (contributor_id, 1, revenue_amount, tier, datetime.now(), datetime.now()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Update contributor analytics error: {e}")
    
    def process_wisdom_revenue(self, wisdom_id: int, contributor_id: int, 
                             tier: str, base_revenue: float = 10.0) -> Dict[str, Any]:
        """Process revenue for a wisdom contribution with community attribution"""
        try:
            # Calculate revenue based on wisdom performance
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get wisdom performance metrics
            cursor.execute('''
                SELECT views, downloads, created_at FROM wisdom_drops WHERE id = ?
            ''', (wisdom_id,))
            
            wisdom_metrics = cursor.fetchone()
            if not wisdom_metrics:
                return {"error": "Wisdom not found"}
            
            views, downloads, created_at = wisdom_metrics
            
            # Calculate performance multiplier
            performance_multiplier = 1.0
            
            # Views multiplier (more views = more revenue)
            if views > 100:
                performance_multiplier += 0.5
            elif views > 50:
                performance_multiplier += 0.3
            elif views > 20:
                performance_multiplier += 0.1
            
            # Downloads multiplier (downloads indicate high value)
            if downloads > 20:
                performance_multiplier += 0.8
            elif downloads > 10:
                performance_multiplier += 0.5
            elif downloads > 5:
                performance_multiplier += 0.2
            
            # Recency multiplier (newer content gets bonus)
            if isinstance(created_at, str):
                created_date = datetime.fromisoformat(created_at)
            else:
                created_date = created_at
            
            days_ago = (datetime.now() - created_date).days
            if days_ago < 7:  # Within a week
                performance_multiplier += 0.3
            elif days_ago < 30:  # Within a month
                performance_multiplier += 0.1
            
            # Calculate total revenue
            total_revenue = base_revenue * performance_multiplier
            
            # Calculate revenue share
            revenue_result = self.calculate_revenue_share(
                wisdom_id, contributor_id, total_revenue, tier
            )
            
            if "error" not in revenue_result:
                # Update wisdom with revenue information
                cursor.execute('''
                    UPDATE wisdom_drops 
                    SET updated_at = ?
                    WHERE id = ?
                ''', (datetime.now(), wisdom_id))
                
                conn.commit()
            
            conn.close()
            
            return {
                **revenue_result,
                "performance_metrics": {
                    "views": views,
                    "downloads": downloads,
                    "performance_multiplier": performance_multiplier,
                    "base_revenue": base_revenue,
                    "total_revenue": total_revenue
                }
            }
            
        except Exception as e:
            print(f"Process wisdom revenue error: {e}")
            return {"error": str(e)}
    
    def get_contributor_dashboard(self, contributor_id: int) -> Dict[str, Any]:
        """Get comprehensive contributor dashboard data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get contributor analytics
            cursor.execute('''
                SELECT total_wisdom_count, total_revenue_earned, total_views, 
                       total_downloads, tier, last_activity
                FROM contributor_analytics 
                WHERE contributor_id = ?
            ''', (contributor_id,))
            
            analytics = cursor.fetchone()
            
            # Get recent revenue shares
            cursor.execute('''
                SELECT wisdom_title, revenue_amount, share_percentage, 
                       payment_status, created_at, paid_at
                FROM revenue_shares 
                WHERE contributor_id = ?
                ORDER BY created_at DESC
                LIMIT 10
            ''', (contributor_id,))
            
            recent_shares = cursor.fetchall()
            
            # Get monthly revenue breakdown
            cursor.execute('''
                SELECT strftime('%Y-%m', created_at) as month, 
                       SUM(revenue_amount) as total_revenue
                FROM revenue_shares 
                WHERE contributor_id = ? AND payment_status = 'paid'
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY month DESC
                LIMIT 12
            ''', (contributor_id,))
            
            monthly_revenue = cursor.fetchall()
            
            # Get tier information
            cursor.execute('''
                SELECT tier FROM contributor_analytics WHERE contributor_id = ?
            ''', (contributor_id,))
            
            tier_result = cursor.fetchone()
            current_tier = tier_result[0] if tier_result else "Standard"
            
            conn.close()
            
            return {
                "contributor_id": contributor_id,
                "current_tier": current_tier,
                "analytics": {
                    "total_wisdom_count": analytics[0] if analytics else 0,
                    "total_revenue_earned": analytics[1] if analytics else 0.0,
                    "total_views": analytics[2] if analytics else 0,
                    "total_downloads": analytics[3] if analytics else 0,
                    "last_activity": analytics[5] if analytics else None
                },
                "recent_shares": [
                    {
                        "wisdom_title": share[0],
                        "revenue_amount": share[1],
                        "share_percentage": share[2],
                        "payment_status": share[3],
                        "created_at": share[4],
                        "paid_at": share[5]
                    } for share in recent_shares
                ],
                "monthly_revenue": [
                    {
                        "month": month[0],
                        "total_revenue": month[1]
                    } for month in monthly_revenue
                ],
                "tier_benefits": {
                    "current_tier": current_tier,
                    "revenue_percentage": self.revenue_tiers.get(current_tier, 50.0),
                    "next_tier": self._get_next_tier(current_tier),
                    "tier_requirements": self._get_tier_requirements(current_tier)
                }
            }
            
        except Exception as e:
            print(f"Get contributor dashboard error: {e}")
            return {"error": str(e)}
    
    def _get_next_tier(self, current_tier: str) -> Optional[str]:
        """Get next tier for contributor"""
        tier_hierarchy = ["Basic", "Standard", "Cultural Guardian", "Developer", "Partnership", "Founding Contributor"]
        
        try:
            current_index = tier_hierarchy.index(current_tier)
            if current_index < len(tier_hierarchy) - 1:
                return tier_hierarchy[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def _get_tier_requirements(self, tier: str) -> Dict[str, Any]:
        """Get requirements for tier advancement"""
        requirements = {
            "Basic": {"wisdom_count": 0, "revenue_threshold": 0, "quality_score": 0},
            "Standard": {"wisdom_count": 5, "revenue_threshold": 100, "quality_score": 70},
            "Cultural Guardian": {"wisdom_count": 15, "revenue_threshold": 500, "quality_score": 80},
            "Developer": {"wisdom_count": 30, "revenue_threshold": 1000, "quality_score": 85},
            "Partnership": {"wisdom_count": 50, "revenue_threshold": 2500, "quality_score": 90},
            "Founding Contributor": {"wisdom_count": 100, "revenue_threshold": 5000, "quality_score": 95}
        }
        
        return requirements.get(tier, requirements["Standard"])
    
    def report_anti_gaming_violation(self, contributor_id: int, violation_type: str, 
                                    violation_description: str, wisdom_id: int = None,
                                    similarity_score: float = 0.0) -> bool:
        """Report anti-gaming violation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate penalty amount based on violation type
            penalty_amount = 0.0
            if violation_type == "duplicate_content":
                penalty_amount = 50.0
            elif violation_type == "self_plagiarism":
                penalty_amount = 100.0
            elif violation_type == "multiple_accounts":
                penalty_amount = 200.0
            
            cursor.execute('''
                INSERT INTO anti_gaming_violations 
                (contributor_id, violation_type, violation_description, wisdom_id, 
                 similarity_score, penalty_amount, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (contributor_id, violation_type, violation_description, wisdom_id,
                  similarity_score, penalty_amount, 'pending', datetime.now()))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Report violation error: {e}")
            return False
    
    def get_platform_revenue_summary(self) -> Dict[str, Any]:
        """Get platform-wide revenue summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total revenue distributed
            cursor.execute('''
                SELECT SUM(revenue_amount) FROM revenue_shares 
                WHERE payment_status = 'paid'
            ''')
            total_distributed = cursor.fetchone()[0] or 0.0
            
            # Pending payments
            cursor.execute('''
                SELECT SUM(revenue_amount) FROM revenue_shares 
                WHERE payment_status = 'pending'
            ''')
            pending_payments = cursor.fetchone()[0] or 0.0
            
            # Revenue by tier
            cursor.execute('''
                SELECT tier, SUM(revenue_amount) as total_revenue, COUNT(*) as contributor_count
                FROM revenue_shares 
                WHERE payment_status = 'paid'
                GROUP BY tier
                ORDER BY total_revenue DESC
            ''')
            revenue_by_tier = cursor.fetchall()
            
            # Top contributors
            cursor.execute('''
                SELECT contributor_id, contributor_email, SUM(revenue_amount) as total_revenue
                FROM revenue_shares 
                WHERE payment_status = 'paid'
                GROUP BY contributor_id
                ORDER BY total_revenue DESC
                LIMIT 10
            ''')
            top_contributors = cursor.fetchall()
            
            conn.close()
            
            return {
                "total_distributed": total_distributed,
                "pending_payments": pending_payments,
                "revenue_by_tier": [
                    {
                        "tier": tier[0],
                        "total_revenue": tier[1],
                        "contributor_count": tier[2]
                    } for tier in revenue_by_tier
                ],
                "top_contributors": [
                    {
                        "contributor_id": contributor[0],
                        "contributor_email": contributor[1],
                        "total_revenue": contributor[2]
                    } for contributor in top_contributors
                ]
            }
            
        except Exception as e:
            print(f"Get platform revenue summary error: {e}")
            return {"error": str(e)}

# Global instance
revenue_system = RevenueTransparencySystem()
