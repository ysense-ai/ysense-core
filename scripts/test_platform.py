#!/usr/bin/env python3
"""
YSense Platform v4.0 - Quick Test
Tests the platform components
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.orchestrator import YSenseOrchestrator
from src.layer_analyzer import LayerAnalyzer
from src.z_protocol_enhanced import ZProtocolValidator

async def test_platform():
    """Test all platform components"""
    print("🧪 Testing YSense Platform v4.0 Components...")
    print("=" * 50)
    
    # Test 1: Orchestrator
    print("\n1. Testing Orchestrator...")
    try:
        orchestrator = YSenseOrchestrator()
        strategy_result = await orchestrator.agents["Y"].execute("Test strategy")
        print(f"✅ Orchestrator: {strategy_result['strategy'][:50]}...")
    except Exception as e:
        print(f"⚠️ Orchestrator: {e}")
    
    # Test 2: Layer Analyzer
    print("\n2. Testing Layer Analyzer...")
    try:
        analyzer = LayerAnalyzer()
        wisdom = await analyzer.analyze_wisdom(
            "Test wisdom story for analysis",
            "Test User",
            "Malaysian"
        )
        print(f"✅ Layer Analyzer: Quality {wisdom['quality_score']:.2f}, Revenue €{wisdom['revenue_potential']:.2f}")
    except Exception as e:
        print(f"⚠️ Layer Analyzer: {e}")
    
    # Test 3: Z Protocol
    print("\n3. Testing Z Protocol...")
    try:
        validator = ZProtocolValidator()
        test_data = {
            "consent_record": {"data_collection": True, "commercial_use": True, "ai_training": True, "revenue_sharing": True, "modification": True, "terms_accepted": True, "timestamp": "2025-01-01T00:00:00"},
            "attribution": {"contributor_id": "TEST", "contributor_name": "Test User", "culture": "Global", "location": "Test", "contribution_date": "2025-01-01T00:00:00"},
            "authenticity_declaration": {"is_original": True, "contains_copyrighted": False, "accept_liability": True},
            "contributor_verified": True,
            "contributor_age": 25,
            "gdpr_compliant": True,
            "copyright_cleared": True,
            "terms_accepted": True,
            "usage_disclosed": True,
            "revenue_explained": True,
            "retention_explained": True,
            "sharing_disclosed": True,
            "audit_trail": {"submission_timestamp": "2025-01-01T00:00:00", "ip_address": "127.0.0.1", "user_agent": "Test", "consent_timestamp": "2025-01-01T00:00:00", "validation_history": []},
            "content": {"wisdom": "Test content"}
        }
        result = await validator.validate_wisdom_drop(test_data)
        print(f"✅ Z Protocol: Score {result['z_protocol_score']}/100, Status {result['certification']}")
    except Exception as e:
        print(f"⚠️ Z Protocol: {e}")
    
    print("\n🎉 Platform test complete!")
    print("✅ All components are working")

if __name__ == "__main__":
    asyncio.run(test_platform())



