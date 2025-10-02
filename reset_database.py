#!/usr/bin/env python3
"""
Database Reset Script - Fix Missing Columns
"""

import os
import sqlite3
from datetime import datetime

def reset_database():
    """Reset database with proper schema"""
    db_path = "ysense_local.db"
    
    print("🔄 Resetting database with proper schema...")
    
    # Backup existing database
    if os.path.exists(db_path):
        backup_path = f"ysense_local_backup_{int(datetime.now().timestamp())}.db"
        os.rename(db_path, backup_path)
        print(f"✅ Existing database backed up to: {backup_path}")
    
    # Create new database with proper schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create wisdom_drops table with all required columns
    cursor.execute('''
        CREATE TABLE wisdom_drops (
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
    
    # Create other required tables
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
            paid_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_fingerprints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_hash TEXT NOT NULL,
            semantic_hash TEXT NOT NULL,
            wisdom_id INTEGER NOT NULL,
            contributor_id INTEGER NOT NULL,
            similarity_score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database reset complete with proper schema!")
    
    # Test the database
    test_database()

def test_database():
    """Test database functionality"""
    print("\n🔍 Testing database functionality...")
    
    try:
        from src.wisdom_library import WisdomLibrary
        
        # Create WisdomLibrary instance
        wisdom_lib = WisdomLibrary()
        print("✅ WisdomLibrary created successfully")
        
        # Test save
        wisdom_id = wisdom_lib.create_wisdom_drop(
            title="Test Story",
            content="This is a test story to verify database functionality.",
            category="Test",
            tags=["test"],
            user_id=1,
            tier="Standard"
        )
        
        if wisdom_id:
            print(f"✅ Test save successful! Wisdom ID: {wisdom_id}")
            
            # Test retrieval
            wisdom = wisdom_lib.get_wisdom_by_id(wisdom_id)
            if wisdom:
                print(f"✅ Test retrieval successful! Title: {wisdom.title}")
            else:
                print("❌ Test retrieval failed")
                
        else:
            print("❌ Test save failed")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Database Reset...")
    reset_database()
    print("\n🎉 Database reset complete!")





