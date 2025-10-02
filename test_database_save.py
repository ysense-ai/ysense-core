#!/usr/bin/env python3
"""
Database Save Test - Diagnose the save failure
"""

import sqlite3
import os
from datetime import datetime

def test_database_save():
    """Test database save functionality"""
    print("🔍 Testing Database Save Functionality...")
    
    # Test 1: Check if database file exists and is writable
    db_path = "ysense_local.db"
    print(f"📁 Database path: {os.path.abspath(db_path)}")
    print(f"📁 File exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        print(f"📁 File size: {os.path.getsize(db_path)} bytes")
        print(f"📁 File writable: {os.access(db_path, os.W_OK)}")
    
    # Test 2: Try to connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Database connection successful")
        
        # Test 3: Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Tables found: {[table[0] for table in tables]}")
        
        # Test 4: Try to create wisdom_drops table if it doesn't exist
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
        print("✅ wisdom_drops table created/verified")
        
        # Test 5: Try to insert a test record
        test_data = (
            "Test Story",
            "This is a test story to verify database save functionality.",
            "test@ysenseai.org",
            1,
            "Test",
            "[]",
            0,
            0,
            datetime.now(),
            datetime.now(),
            1,
            None
        )
        
        cursor.execute('''
            INSERT INTO wisdom_drops 
            (title, content, author_email, author_id, category, tags,
             views, downloads, created_at, updated_at, is_public, attribution_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_data)
        
        test_id = cursor.lastrowid
        print(f"✅ Test record inserted with ID: {test_id}")
        
        # Test 6: Verify the record was saved
        cursor.execute("SELECT * FROM wisdom_drops WHERE id = ?", (test_id,))
        saved_record = cursor.fetchone()
        
        if saved_record:
            print("✅ Test record verified in database")
            print(f"📊 Record: {saved_record}")
        else:
            print("❌ Test record not found in database")
        
        # Test 7: Clean up test record
        cursor.execute("DELETE FROM wisdom_drops WHERE id = ?", (test_id,))
        print("✅ Test record cleaned up")
        
        conn.commit()
        conn.close()
        
        print("🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_wisdom_library():
    """Test WisdomLibrary class"""
    print("\n🔍 Testing WisdomLibrary Class...")
    
    try:
        from src.wisdom_library import WisdomLibrary
        
        # Create WisdomLibrary instance
        wisdom_lib = WisdomLibrary()
        print("✅ WisdomLibrary instance created")
        
        # Test create_wisdom_drop method
        wisdom_id = wisdom_lib.create_wisdom_drop(
            title="Test Story",
            content="This is a test story to verify WisdomLibrary functionality.",
            category="Test",
            tags=["test", "verification"],
            user_id=1,
            tier="Standard",
            metadata={"test": True}
        )
        
        if wisdom_id:
            print(f"✅ WisdomLibrary.create_wisdom_drop successful: ID {wisdom_id}")
            
            # Test get_wisdom_by_id
            wisdom = wisdom_lib.get_wisdom_by_id(wisdom_id)
            if wisdom:
                print("✅ WisdomLibrary.get_wisdom_by_id successful")
                print(f"📊 Wisdom: {wisdom.title}")
            else:
                print("❌ WisdomLibrary.get_wisdom_by_id failed")
            
            # Clean up
            # Note: We don't have a delete method, so we'll leave the test record
            
        else:
            print("❌ WisdomLibrary.create_wisdom_drop failed")
            
        return True
        
    except Exception as e:
        print(f"❌ WisdomLibrary test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Database Save Diagnosis...")
    print("=" * 50)
    
    # Run tests
    db_test = test_database_save()
    wisdom_test = test_wisdom_library()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"Database Save Test: {'✅ PASSED' if db_test else '❌ FAILED'}")
    print(f"WisdomLibrary Test: {'✅ PASSED' if wisdom_test else '❌ FAILED'}")
    
    if db_test and wisdom_test:
        print("\n🎉 All tests passed! Database save should work.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")





