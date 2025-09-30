import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd

class MetricsCollector:
    """Collect and calculate platform metrics for transparency"""
    
    def __init__(self, db_path="database/ysense_local.db"):
        self.db_path = db_path
        # Ensure database folder exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._ensure_metrics_tables()
    
    def _ensure_metrics_tables(self):
        """Create metrics tracking tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS wisdom_drops (
                    drop_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author TEXT NOT NULL,
                    content_type TEXT,
                    quality_score REAL,
                    revenue_potential REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tier2_eligible BOOLEAN DEFAULT 0,
                    tier3_eligible BOOLEAN DEFAULT 0,
                    tier4_eligible BOOLEAN DEFAULT 0
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS platform_metrics (
                    metric_date DATE PRIMARY KEY,
                    total_users INTEGER,
                    active_contributors INTEGER,
                    total_drops INTEGER,
                    avg_quality_score REAL,
                    total_revenue REAL,
                    ai_training_revenue REAL,
                    cultural_revenue REAL,
                    research_revenue REAL
                )
            ''')
    
    def get_live_metrics(self):
        """Get real-time platform metrics"""
        with sqlite3.connect(self.db_path) as conn:
            # Get user counts from wisdom_drops table
            total_users = conn.execute(
                "SELECT COUNT(DISTINCT author_id) FROM wisdom_drops"
            ).fetchone()[0] or 0
            
            active_contributors = conn.execute(
                "SELECT COUNT(DISTINCT author_id) FROM wisdom_drops WHERE created_at > date('now', '-30 days')"
            ).fetchone()[0] or 0
            
            # Get wisdom drops stats
            drops_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_drops,
                    SUM(views) as total_views,
                    SUM(downloads) as total_downloads
                FROM wisdom_drops
            """).fetchone()
            
            total_drops = drops_stats[0] or 0
            total_views = drops_stats[1] or 0
            total_downloads = drops_stats[2] or 0
            
            return {
                'total_users': total_users,
                'active_contributors': active_contributors,
                'total_drops': total_drops,
                'total_views': total_views,
                'total_downloads': total_downloads,
                'revenue_earned': 0.0,  # Will be calculated by revenue system
                'last_updated': datetime.now().isoformat()
            }
    
    def get_pricing_breakdown(self):
        """Get detailed pricing breakdown by category"""
        with sqlite3.connect(self.db_path) as conn:
            breakdown = conn.execute("""
                SELECT 
                    content_type,
                    COUNT(*) as count,
                    AVG(quality_score) as avg_quality,
                    SUM(revenue_potential) as total_revenue
                FROM wisdom_drops
                GROUP BY content_type
            """).fetchall()
            
            return pd.DataFrame(breakdown, columns=[
                'Content Type', 'Drops Count', 'Avg Quality', 'Revenue Generated'
            ])