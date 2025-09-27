#!/usr/bin/env python3
"""
YSense Platform v4.0 - Database Initialization
Creates the database and initializes tables
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.models import Base, engine

def init_database():
    """Initialize the database with all tables"""
    print("🚀 Initializing YSense Platform v4.0 Database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully!")
        print("✅ All tables created")
        print("✅ Ready for YSense Platform v4.0")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database setup complete!")
        print("You can now run the platform with LAUNCH_YSENSE.bat")
    else:
        print("\n❌ Database setup failed!")
        print("Please check the error messages above")
    
    input("\nPress Enter to exit...")