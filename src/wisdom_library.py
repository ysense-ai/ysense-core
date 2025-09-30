"""
YSense™ Wisdom Library Manager
Handles wisdom drops, search, filtering, and management
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class WisdomDrop:
    """Wisdom drop data class"""
    id: int
    title: str
    content: str
    author_email: str
    author_id: int
    category: str
    tags: List[str]
    views: int
    downloads: int
    created_at: datetime
    updated_at: datetime
    is_public: bool = True
    attribution_hash: Optional[str] = None

class WisdomLibrary:
    """Wisdom library manager for YSense platform"""
    
    def __init__(self, db_path: str = "database/ysense_local.db"):
        self.db_path = db_path
        # Ensure database folder exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cursor = conn.cursor()
        
        # Create wisdom_drops table (without foreign key constraint for now)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wisdom_drops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_email TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                category TEXT DEFAULT 'General',
                tags TEXT DEFAULT '[]',
                views INTEGER DEFAULT 0,
                downloads INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_public BOOLEAN DEFAULT 1,
                attribution_hash TEXT
            )
        ''')
        
        # Check if required columns exist, if not add them
        cursor.execute("PRAGMA table_info(wisdom_drops)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # List of required columns with their definitions
        required_columns = {
            'content': 'TEXT NOT NULL DEFAULT ""',
            'author_email': 'TEXT NOT NULL DEFAULT "user@ysenseai.org"',
            'author_id': 'INTEGER NOT NULL DEFAULT 1',
            'category': 'TEXT DEFAULT "General"',
            'tags': 'TEXT DEFAULT "[]"',
            'views': 'INTEGER DEFAULT 0',
            'downloads': 'INTEGER DEFAULT 0',
            'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'is_public': 'BOOLEAN DEFAULT 1',
            'attribution_hash': 'TEXT'
        }
        
        # Add missing columns
        for column_name, column_definition in required_columns.items():
            if column_name not in columns:
                try:
                    cursor.execute(f'ALTER TABLE wisdom_drops ADD COLUMN {column_name} {column_definition}')
                    print(f"✅ Added missing '{column_name}' column to wisdom_drops table")
                except Exception as e:
                    print(f"⚠️ Could not add column '{column_name}': {e}")
        
        conn.commit()
        conn.close()
    
    def create_wisdom(self, title: str, content: str, author_email: str, 
                     author_id: int, category: str = "General", 
                     tags: List[str] = None, is_public: bool = True) -> Optional[WisdomDrop]:
        """Create a new wisdom drop"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tags_json = json.dumps(tags or [])
            
            cursor.execute('''
                INSERT INTO wisdom_drops 
                (title, content, author_email, author_id, category, tags, is_public, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, content, author_email, author_id, category, tags_json, 
                  is_public, datetime.now(), datetime.now()))
            
            wisdom_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return WisdomDrop(
                id=wisdom_id,
                title=title,
                content=content,
                author_email=author_email,
                author_id=author_id,
                category=category,
                tags=tags or [],
                views=0,
                downloads=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_public=is_public
            )
            
        except Exception as e:
            print(f"Create wisdom error: {e}")
            return None
    
    def get_wisdom_by_id(self, wisdom_id: int) -> Optional[WisdomDrop]:
        """Get wisdom drop by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, content, author_email, author_id, category, tags,
                       views, downloads, created_at, updated_at, is_public, attribution_hash
                FROM wisdom_drops WHERE id = ?
            ''', (wisdom_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            (id, title, content, author_email, author_id, category, tags_json,
             views, downloads, created_at, updated_at, is_public, attribution_hash) = row
            
            return WisdomDrop(
                id=id,
                title=title,
                content=content,
                author_email=author_email,
                author_id=author_id,
                category=category,
                tags=json.loads(tags_json) if tags_json else [],
                views=views,
                downloads=downloads,
                created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else updated_at,
                is_public=bool(is_public),
                attribution_hash=attribution_hash
            )
            
        except Exception as e:
            print(f"Get wisdom error: {e}")
            return None
    
    def get_all_wisdom(self, limit: int = 100, offset: int = 0) -> List[WisdomDrop]:
        """Get all public wisdom drops"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, content, author_email, author_id, category, tags,
                       views, downloads, created_at, updated_at, is_public, attribution_hash
                FROM wisdom_drops 
                WHERE is_public = 1
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            wisdom_drops = []
            for row in rows:
                (id, title, content, author_email, author_id, category, tags_json,
                 views, downloads, created_at, updated_at, is_public, attribution_hash) = row
                
                wisdom_drops.append(WisdomDrop(
                    id=id,
                    title=title,
                    content=content,
                    author_email=author_email,
                    author_id=author_id,
                    category=category,
                    tags=json.loads(tags_json) if tags_json else [],
                    views=views,
                    downloads=downloads,
                    created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                    updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else updated_at,
                    is_public=bool(is_public),
                    attribution_hash=attribution_hash
                ))
            
            return wisdom_drops
            
        except Exception as e:
            print(f"Get all wisdom error: {e}")
            return []
    
    def get_user_wisdom(self, user_id: int) -> List[WisdomDrop]:
        """Get all wisdom drops by a specific user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, content, author_email, author_id, category, tags,
                       views, downloads, created_at, updated_at, is_public, attribution_hash
                FROM wisdom_drops 
                WHERE author_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            wisdom_drops = []
            for row in rows:
                (id, title, content, author_email, author_id, category, tags_json,
                 views, downloads, created_at, updated_at, is_public, attribution_hash) = row
                
                wisdom_drops.append(WisdomDrop(
                    id=id,
                    title=title,
                    content=content,
                    author_email=author_email,
                    author_id=author_id,
                    category=category,
                    tags=json.loads(tags_json) if tags_json else [],
                    views=views,
                    downloads=downloads,
                    created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                    updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else updated_at,
                    is_public=bool(is_public),
                    attribution_hash=attribution_hash
                ))
            
            return wisdom_drops
            
        except Exception as e:
            print(f"Get user wisdom error: {e}")
            return []
    
    def search_wisdom(self, query: str, category: str = None) -> List[WisdomDrop]:
        """Search wisdom drops by query"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category and category != "All":
                cursor.execute('''
                    SELECT id, title, content, author_email, author_id, category, tags,
                           views, downloads, created_at, updated_at, is_public, attribution_hash
                    FROM wisdom_drops 
                    WHERE is_public = 1 AND category = ? AND 
                          (title LIKE ? OR content LIKE ?)
                    ORDER BY created_at DESC
                ''', (category, f'%{query}%', f'%{query}%'))
            else:
                cursor.execute('''
                    SELECT id, title, content, author_email, author_id, category, tags,
                           views, downloads, created_at, updated_at, is_public, attribution_hash
                    FROM wisdom_drops 
                    WHERE is_public = 1 AND 
                          (title LIKE ? OR content LIKE ?)
                    ORDER BY created_at DESC
                ''', (f'%{query}%', f'%{query}%'))
            
            rows = cursor.fetchall()
            conn.close()
            
            wisdom_drops = []
            for row in rows:
                (id, title, content, author_email, author_id, category, tags_json,
                 views, downloads, created_at, updated_at, is_public, attribution_hash) = row
                
                wisdom_drops.append(WisdomDrop(
                    id=id,
                    title=title,
                    content=content,
                    author_email=author_email,
                    author_id=author_id,
                    category=category,
                    tags=json.loads(tags_json) if tags_json else [],
                    views=views,
                    downloads=downloads,
                    created_at=datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at,
                    updated_at=datetime.fromisoformat(updated_at) if isinstance(updated_at, str) else updated_at,
                    is_public=bool(is_public),
                    attribution_hash=attribution_hash
                ))
            
            return wisdom_drops
            
        except Exception as e:
            print(f"Search wisdom error: {e}")
            return []
    
    def increment_views(self, wisdom_id: int) -> bool:
        """Increment view count for wisdom drop"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE wisdom_drops SET views = views + 1 WHERE id = ?
            ''', (wisdom_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Increment views error: {e}")
            return False
    
    def increment_downloads(self, wisdom_id: int) -> bool:
        """Increment download count for wisdom drop"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE wisdom_drops SET downloads = downloads + 1 WHERE id = ?
            ''', (wisdom_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Increment downloads error: {e}")
            return False
    
    def update_wisdom(self, wisdom_id: int, title: str = None, content: str = None, 
                     category: str = None, tags: List[str] = None) -> bool:
        """Update wisdom drop"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if title:
                updates.append("title = ?")
                params.append(title)
            
            if content:
                updates.append("content = ?")
                params.append(content)
            
            if category:
                updates.append("category = ?")
                params.append(category)
            
            if tags:
                updates.append("tags = ?")
                params.append(json.dumps(tags))
            
            updates.append("updated_at = ?")
            params.append(datetime.now())
            params.append(wisdom_id)
            
            query = f"UPDATE wisdom_drops SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Update wisdom error: {e}")
            return False
    
    def delete_wisdom(self, wisdom_id: int, user_id: int) -> bool:
        """Delete wisdom drop (only by author)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM wisdom_drops WHERE id = ? AND author_id = ?
            ''', (wisdom_id, user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Delete wisdom error: {e}")
            return False
    
    def create_wisdom_drop(self, title: str, content: str, category: str = "General",
                         tags: List[str] = None, user_id: int = 1, tier: str = "Standard",
                         metadata: Dict = None) -> Optional[int]:
        """Create a new wisdom drop (alias for create_wisdom with different parameters)"""
        try:
            # Use a default email for now (can be enhanced later)
            author_email = f"user_{user_id}@ysenseai.org"
            
            # Create wisdom using existing method
            wisdom_drop = self.create_wisdom(
                title=title,
                content=content,
                author_email=author_email,
                author_id=user_id,
                category=category,
                tags=tags or [],
                is_public=True
            )
            
            if wisdom_drop:
                # Store additional metadata if provided
                if metadata:
                    # For now, we'll store metadata in a simple way
                    # In a real implementation, you might want a separate metadata table
                    print(f"Metadata stored for wisdom {wisdom_drop.id}: {metadata}")
                
                return wisdom_drop.id
            else:
                return None
                
        except Exception as e:
            print(f"Create wisdom drop error: {e}")
            return None
