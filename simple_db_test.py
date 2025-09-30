#!/usr/bin/env python3
"""
Simple Database Test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.wisdom_library import WisdomLibrary

def test_simple_save():
    """Test simple database save"""
    print("🔍 Testing Simple Database Save...")
    
    try:
        # Create WisdomLibrary instance
        wisdom_lib = WisdomLibrary()
        print("✅ WisdomLibrary created")
        
        # Test save
        wisdom_id = wisdom_lib.create_wisdom_drop(
            title="Test Story",
            content="This is a test story to verify database save functionality.",
            category="Test",
            tags=["test"],
            user_id=1,
            tier="Standard"
        )
        
        if wisdom_id:
            print(f"✅ Save successful! Wisdom ID: {wisdom_id}")
            return True
        else:
            print("❌ Save failed - no ID returned")
            return False
            
    except Exception as e:
        print(f"❌ Save failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_save()
    if success:
        print("🎉 Database save test PASSED!")
    else:
        print("❌ Database save test FAILED!")



