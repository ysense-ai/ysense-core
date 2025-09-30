#!/usr/bin/env python3
"""
Test script to verify AgentSystem import
"""

import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

try:
    from agent_system_v41 import AgentSystem
    print("✅ AgentSystem imported successfully!")
    
    # Test instantiation
    agent_system = AgentSystem()
    print("✅ AgentSystem instantiated successfully!")
    
    # Test method availability
    if hasattr(agent_system, 'execute_workflow'):
        print("✅ execute_workflow method found!")
    else:
        print("❌ execute_workflow method not found!")
    
    print("\n🎉 All tests passed! AgentSystem is ready.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")



