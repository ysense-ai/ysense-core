# database_manager.py
"""
YSense™ Persistent Storage Manager
Protects wisdom drops from data loss with SQLite + JSON backup
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

class YSenseDatabase:
    def __init__(self, db_path: str = "ysense_wisdom.db"):
        self.db_path = db_path
        self.backup_dir = "wisdom_backups"
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
        self._ensure_backup_directory()
    
    def _initialize_database(self):
        """Create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS wisdom_drops (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    author TEXT NOT NULL,
                    cultural_context TEXT,
                    
                    -- Five Layers
                    surface_layer TEXT,
                    emotional_layer TEXT,
                    contextual_layer TEXT,
                    wisdom_layer TEXT,
                    cultural_layer TEXT,
                    
                    -- Attribution & Revenue
                    quality_score REAL,
                    revenue_potential REAL,
                    consent_verified INTEGER,
                    attribution_hash TEXT,
                    
                    -- Z Protocol
                    z_protocol_version TEXT,
                    usage_rights TEXT,
                    
                    -- Metadata
                    embedding_vector TEXT,  -- JSON array of floats
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS revenue_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wisdom_id TEXT NOT NULL,
                    transaction_date TEXT,
                    amount_eur REAL,
                    quality_multiplier REAL,
                    cultural_bonus REAL,
                    institution TEXT,
                    payment_status TEXT,
                    FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops(id)
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_author 
                ON wisdom_drops(author)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_quality 
                ON wisdom_drops(quality_score)
            ''')
            
            conn.commit()
            self.logger.info(f"Database initialized at {self.db_path}")
    
    def _ensure_backup_directory(self):
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def save_wisdom_drop(self, wisdom_drop: Dict) -> bool:
        """Save a wisdom drop to database with automatic backup"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Prepare embedding as JSON string
                embedding = json.dumps(wisdom_drop.get('embedding', []))
                
                conn.execute('''
                    INSERT OR REPLACE INTO wisdom_drops (
                        id, timestamp, author, cultural_context,
                        surface_layer, emotional_layer, contextual_layer,
                        wisdom_layer, cultural_layer,
                        quality_score, revenue_potential, consent_verified,
                        attribution_hash, z_protocol_version, usage_rights,
                        embedding_vector, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    wisdom_drop['id'],
                    wisdom_drop['timestamp'],
                    wisdom_drop['author'],
                    wisdom_drop.get('cultural_context', ''),
                    
                    wisdom_drop['layers'].get('surface', ''),
                    wisdom_drop['layers'].get('emotional', ''),
                    wisdom_drop['layers'].get('contextual', ''),
                    wisdom_drop['layers'].get('wisdom', ''),
                    wisdom_drop['layers'].get('cultural', ''),
                    
                    wisdom_drop['quality_score'],
                    wisdom_drop['revenue_potential'],
                    1 if wisdom_drop.get('consent_verified', False) else 0,
                    wisdom_drop.get('attribution_hash', ''),
                    wisdom_drop.get('z_protocol_version', 'v2.0'),
                    json.dumps(wisdom_drop.get('usage_rights', {})),
                    
                    embedding,
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                
                # Auto-backup after each save
                self._create_json_backup([wisdom_drop])
                
                self.logger.info(f"Saved wisdom drop {wisdom_drop['id']} - Revenue: €{wisdom_drop['revenue_potential']:.2f}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to save wisdom drop: {e}")
            return False
    
    def get_all_wisdom_drops(self) -> List[Dict]:
        """Retrieve all wisdom drops from database"""
        wisdom_drops = []
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM wisdom_drops 
                ORDER BY quality_score DESC, created_at DESC
            ''')
            
            for row in cursor:
                wisdom_drop = {
                    'id': row['id'],
                    'timestamp': row['timestamp'],
                    'author': row['author'],
                    'cultural_context': row['cultural_context'],
                    'layers': {
                        'surface': row['surface_layer'],
                        'emotional': row['emotional_layer'],
                        'contextual': row['contextual_layer'],
                        'wisdom': row['wisdom_layer'],
                        'cultural': row['cultural_layer']
                    },
                    'quality_score': row['quality_score'],
                    'revenue_potential': row['revenue_potential'],
                    'consent_verified': bool(row['consent_verified']),
                    'attribution_hash': row['attribution_hash'],
                    'z_protocol_version': row['z_protocol_version'],
                    'usage_rights': json.loads(row['usage_rights'] or '{}'),
                    'embedding': json.loads(row['embedding_vector'] or '[]')
                }
                wisdom_drops.append(wisdom_drop)
        
        return wisdom_drops
    
    def search_by_author(self, author: str) -> List[Dict]:
        """Search wisdom drops by author"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM wisdom_drops 
                WHERE author LIKE ? 
                ORDER BY quality_score DESC
            ''', (f'%{author}%',))
            
            return [self._row_to_dict(row) for row in cursor]
    
    def get_revenue_summary(self) -> Dict:
        """Calculate total revenue potential"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as total_drops,
                    SUM(revenue_potential) as total_revenue,
                    AVG(quality_score) as avg_quality,
                    MAX(revenue_potential) as max_revenue
                FROM wisdom_drops
                WHERE consent_verified = 1
            ''')
            
            row = cursor.fetchone()
            return {
                'total_wisdom_drops': row[0] or 0,
                'total_revenue_potential': row[1] or 0.0,
                'average_quality_score': row[2] or 0.0,
                'highest_revenue_drop': row[3] or 0.0
            }
    
    def _create_json_backup(self, wisdom_drops: List[Dict]):
        """Create timestamped JSON backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'wisdom_backup_{timestamp}.json')
        
        # Keep only last 10 backups
        self._cleanup_old_backups()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'version': 'YSense v2.0',
                'total_drops': len(wisdom_drops),
                'wisdom_drops': wisdom_drops
            }, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Backup created: {backup_file}")
    
    def _cleanup_old_backups(self):
        """Keep only the 10 most recent backups"""
        backup_files = sorted([
            f for f in os.listdir(self.backup_dir) 
            if f.startswith('wisdom_backup_')
        ])
        
        if len(backup_files) > 10:
            for old_file in backup_files[:-10]:
                os.remove(os.path.join(self.backup_dir, old_file))
    
    def export_to_json(self, filepath: str = None) -> str:
        """Export all wisdom drops to JSON file"""
        if not filepath:
            filepath = f'ysense_export_{datetime.now().strftime("%Y%m%d")}.json'
        
        wisdom_drops = self.get_all_wisdom_drops()
        revenue_summary = self.get_revenue_summary()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'platform': 'YSense™ | 慧觉™',
            'version': '2.0',
            'doi': '10.5281/zenodo.17072168',
            'revenue_summary': revenue_summary,
            'wisdom_drops': wisdom_drops
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Exported {len(wisdom_drops)} wisdom drops to {filepath}")
        return filepath
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert database row to wisdom drop dictionary"""
        return {
            'id': row['id'],
            'timestamp': row['timestamp'],
            'author': row['author'],
            'cultural_context': row['cultural_context'],
            'layers': {
                'surface': row['surface_layer'],
                'emotional': row['emotional_layer'],
                'contextual': row['contextual_layer'],
                'wisdom': row['wisdom_layer'],
                'cultural': row['cultural_layer']
            },
            'quality_score': row['quality_score'],
            'revenue_potential': row['revenue_potential'],
            'consent_verified': bool(row['consent_verified']),
            'attribution_hash': row['attribution_hash']
        }
    
    def track_revenue(self, wisdom_id: str, amount: float, institution: str):
        """Track actual revenue transactions"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO revenue_tracking (
                    wisdom_id, transaction_date, amount_eur, 
                    institution, payment_status
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                wisdom_id,
                datetime.now().isoformat(),
                amount,
                institution,
                'pending'
            ))
            conn.commit()
            self.logger.info(f"Revenue tracked: €{amount} from {institution} for wisdom {wisdom_id}")


# Integration with existing wisdom_rag.py
class WisdomLibraryRAG:
    def __init__(self):
        # Initialize with persistent database
        self.db = YSenseDatabase()
        
        # Load existing wisdom drops from database
        self.wisdom_store = self.db.get_all_wisdom_drops()
        
        # Rest of your existing initialization...
        self.layers = [
            "surface",
            "emotional", 
            "contextual",
            "wisdom",
            "cultural"
        ]
    
    async def add_wisdom(self, wisdom_drop: Dict) -> Dict:
        """Add wisdom with automatic persistence"""
        # Your existing processing...
        
        # Save to database
        if self.db.save_wisdom_drop(wisdom_drop):
            # Add to in-memory store
            self.wisdom_store.append(wisdom_drop)
            
            # Check revenue milestone
            summary = self.db.get_revenue_summary()
            if summary['total_revenue_potential'] >= 15000:
                print(f"🎯 Q1 2026 Target Achieved: €{summary['total_revenue_potential']:.2f}")
        
        return wisdom_drop


# Usage Example
if __name__ == "__main__":
    # Initialize database
    db = YSenseDatabase()
    
    # Example wisdom drop
    wisdom_drop = {
        'id': 'wisdom_001',
        'timestamp': datetime.now().isoformat(),
        'author': 'Alton Lee Wei Bin',
        'cultural_context': 'Malaysian',
        'layers': {
            'surface': 'Building attribution infrastructure',
            'emotional': 'Determined and focused',
            'contextual': 'Teluk Intan innovation hub',
            'wisdom': 'Legal protection enables market execution',
            'cultural': 'Malaysian values in global AI ethics'
        },
        'quality_score': 0.95,
        'revenue_potential': 71.4,  # €50 × 0.95 × 1.5 cultural
        'consent_verified': True,
        'attribution_hash': 'hash_xyz',
        'z_protocol_version': 'v2.0',
        'usage_rights': {'academic': True, 'commercial': False}
    }
    
    # Save and verify
    db.save_wisdom_drop(wisdom_drop)
    print(db.get_revenue_summary())
    
    # Export for academic partners
    db.export_to_json('ysense_academic_export.json')