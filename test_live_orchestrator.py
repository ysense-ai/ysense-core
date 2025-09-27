#!/usr/bin/env python3
"""
Test YSense Orchestrator with Anthropic API - Live Test
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.orchestrator import YSenseOrchestrator

async def test_live_orchestrator():
    """Test the orchestrator with live Anthropic API calls"""
    print("🚀 Testing YSense Orchestrator with Anthropic API - LIVE TEST")
    print("=" * 70)
    
    # Initialize orchestrator
    orchestrator = YSenseOrchestrator()
    
    print("\n📊 Testing Individual Agents:")
    
    # Test Strategy Agent
    print("\n1. 🎯 Strategy Agent (Y) - Anthropic Claude:")
    try:
        strategy_result = await orchestrator.agents["Y"].execute("Convert Tesla Optimus opportunity")
        print(f"   ✅ AI Model: {strategy_result.get('ai_model', 'Unknown')}")
        print(f"   📈 Strategy: {strategy_result['strategy'][:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test Market Intelligence Agent
    print("\n2. 📊 Market Intelligence Agent (X) - Anthropic Claude:")
    try:
        opportunities = await orchestrator.agents["X"].scan_opportunities()
        print(f"   ✅ AI Model: {opportunities[0].get('ai_model', 'Unknown')}")
        print(f"   🎯 Found {len(opportunities)} opportunities")
        print(f"   💡 Analysis: {opportunities[0]['anthropic_analysis'][:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test Ethics Agent
    print("\n3. 🛡️ Ethics Compliance Agent (Z) - Anthropic Claude:")
    try:
        ethics_result = await orchestrator.agents["Z"].validate_dataset("live_test_dataset")
        print(f"   ✅ AI Model: {ethics_result.get('ai_model', 'Unknown')}")
        print(f"   📊 Z Protocol Score: {ethics_result['z_protocol_score']}%")
        print(f"   🔍 Analysis: {ethics_result['anthropic_ethical_analysis'][:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test CEO Agent
    print("\n4. 👑 CEO Persona Agent (ALTON) - Anthropic Claude:")
    try:
        ceo_result = await orchestrator.agents["ALTON"].execute("team_rally")
        print(f"   ✅ AI Model: {ceo_result.get('ai_model', 'Unknown')}")
        print(f"   🎯 Vision: {ceo_result['vision']}")
        print(f"   💪 Leadership: {ceo_result['anthropic_leadership_guidance'][:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test full workflow
    print("\n🔄 Testing Full Daily Workflow:")
    try:
        workflow_result = await orchestrator.execute_daily_workflow()
        print(f"   ✅ Status: {workflow_result['status']}")
        print(f"   📅 Date: {workflow_result['date']}")
        print(f"   📊 Metrics: {workflow_result.get('metrics', {}).get('overall_status', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 Live Test Complete!")
    print("\n🌟 Your YSense Orchestrator is now powered by Anthropic Claude!")
    print("   - Advanced AI reasoning")
    print("   - Strategic analysis")
    print("   - Ethical compliance")
    print("   - Leadership insights")

if __name__ == "__main__":
    asyncio.run(test_live_orchestrator())



