"""
YSense™ Attribution Engine
Generates attribution documents for wisdom drops
"""

import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
import sqlite3

@dataclass
class AttributionDocument:
    """Attribution document data class"""
    id: int
    wisdom_id: int
    document_hash: str
    content: str
    created_at: datetime
    download_count: int = 0

class AttributionEngine:
    """Attribution engine for YSense platform"""
    
    def __init__(self, db_path: str = "ysense_local.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create attribution_documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attribution_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wisdom_id INTEGER NOT NULL,
                document_hash TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                download_count INTEGER DEFAULT 0,
                FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_attribution(self, wisdom_id: int) -> Optional[AttributionDocument]:
        """Generate attribution document for wisdom drop"""
        try:
            # Get wisdom drop details
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, content, author_email, author_id, category, 
                       tags, created_at, views, downloads
                FROM wisdom_drops WHERE id = ?
            ''', (wisdom_id,))
            
            wisdom_row = cursor.fetchone()
            if not wisdom_row:
                conn.close()
                return None
            
            (id, title, content, author_email, author_id, category, 
             tags_json, created_at, views, downloads) = wisdom_row
            
            # Generate attribution content
            attribution_content = self._create_attribution_content(
                title, content, author_email, category, tags_json, 
                created_at, views, downloads
            )
            
            # Generate document hash
            document_hash = hashlib.sha256(attribution_content.encode()).hexdigest()
            
            # Check if attribution already exists
            cursor.execute('''
                SELECT id FROM attribution_documents WHERE document_hash = ?
            ''', (document_hash,))
            
            if cursor.fetchone():
                conn.close()
                return None  # Attribution already exists
            
            # Insert attribution document
            cursor.execute('''
                INSERT INTO attribution_documents 
                (wisdom_id, document_hash, content, created_at)
                VALUES (?, ?, ?, ?)
            ''', (wisdom_id, document_hash, attribution_content, datetime.now()))
            
            attribution_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return AttributionDocument(
                id=attribution_id,
                wisdom_id=wisdom_id,
                document_hash=document_hash,
                content=attribution_content,
                created_at=datetime.now()
            )
            
        except Exception as e:
            print(f"Generate attribution error: {e}")
            return None
    
    def _create_attribution_content(self, title: str, content: str, author_email: str,
                                   category: str, tags_json: str, created_at: str,
                                   views: int, downloads: int) -> str:
        """Create attribution document content"""
        tags = json.loads(tags_json) if tags_json else []
        
        attribution_content = f"""
YSense™ AI Attribution Infrastructure
=====================================

Wisdom Drop Attribution Document
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

WISDOM DROP DETAILS:
-------------------
Title: {title}
Author: {author_email}
Category: {category}
Tags: {', '.join(tags) if tags else 'None'}
Created: {created_at}
Views: {views}
Downloads: {downloads}

CONTENT:
--------
{content}

ATTRIBUTION STATEMENT:
----------------------
This wisdom drop is part of the YSense™ AI Attribution Infrastructure,
a platform dedicated to preserving and attributing human wisdom in the
age of artificial intelligence.

The content above represents original human wisdom and insight,
contributed by {author_email} to the YSense™ platform.

This attribution document serves as:
1. Proof of original human contribution
2. Protection against AI misattribution
3. Foundation for revenue sharing
4. Cultural preservation record

YSense™ Platform Information:
- Platform: YSense™ v4.1 | 慧觉™
- Mission: The Genesis of Human-AI Wisdom Collaboration
- Attribution Engine: Z Protocol v2.0
- Document Hash: {hashlib.sha256(f"{title}{author_email}{created_at}".encode()).hexdigest()[:16]}

LEGAL NOTICE:
-------------
This document is generated by the YSense™ Attribution Engine and
provides cryptographic proof of human wisdom contribution. Any
unauthorized use or misattribution of this content violates the
YSense™ Terms of Service and may result in legal action.

For questions or concerns about this attribution, please contact:
support@ysense.ai

---
Generated by YSense™ Attribution Engine v4.1
The Genesis of Human-AI Wisdom Collaboration
        """.strip()
        
        return attribution_content
    
    def get_attribution_by_wisdom_id(self, wisdom_id: int) -> Optional[AttributionDocument]:
        """Get attribution document by wisdom ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, wisdom_id, document_hash, content, created_at, download_count
                FROM attribution_documents WHERE wisdom_id = ?
            ''', (wisdom_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            id, wisdom_id, document_hash, content, created_at, download_count = row
            
            return AttributionDocument(
                id=id,
                wisdom_id=wisdom_id,
                document_hash=document_hash,
                content=content,
                created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                download_count=download_count
            )
            
        except Exception as e:
            print(f"Get attribution error: {e}")
            return None
    
    def download_attribution(self, wisdom_id: int) -> Optional[str]:
        """Download attribution document and increment counter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get attribution document
            cursor.execute('''
                SELECT content FROM attribution_documents WHERE wisdom_id = ?
            ''', (wisdom_id,))
            
            row = cursor.fetchone()
            if not row:
                conn.close()
                return None
            
            content = row[0]
            
            # Increment download count
            cursor.execute('''
                UPDATE attribution_documents SET download_count = download_count + 1 
                WHERE wisdom_id = ?
            ''', (wisdom_id,))
            
            conn.commit()
            conn.close()
            
            return content
            
        except Exception as e:
            print(f"Download attribution error: {e}")
            return None
    
    def get_attribution_stats(self) -> Dict[str, Any]:
        """Get attribution statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total attributions
            cursor.execute('SELECT COUNT(*) FROM attribution_documents')
            total_attributions = cursor.fetchone()[0]
            
            # Total downloads
            cursor.execute('SELECT SUM(download_count) FROM attribution_documents')
            total_downloads = cursor.fetchone()[0] or 0
            
            # Recent attributions (last 30 days)
            cursor.execute('''
                SELECT COUNT(*) FROM attribution_documents 
                WHERE created_at >= datetime('now', '-30 days')
            ''')
            recent_attributions = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_attributions': total_attributions,
                'total_downloads': total_downloads,
                'recent_attributions': recent_attributions,
                'average_downloads_per_attribution': total_downloads / total_attributions if total_attributions > 0 else 0
            }
            
        except Exception as e:
            print(f"Get attribution stats error: {e}")
            return {
                'total_attributions': 0,
                'total_downloads': 0,
                'recent_attributions': 0,
                'average_downloads_per_attribution': 0
            }





