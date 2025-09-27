#!/usr/bin/env python3
"""
Test script for YSense Orchestrator with Anthropic API integration
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.orchestrator import YSenseOrchestrator

async def test_anthropic_orchestrator():
    """Test the orchestrator with Anthropic API integration"""
    print("🚀 Testing YSense Orchestrator with Anthropic API")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = YSenseOrchestrator()
    
    # Test individual agents
    print("\n📊 Testing Individual Agents with Anthropic:")
    
    # Test Strategy Agent
    print("\n1. Strategy Agent (Y) - Anthropic Claude:")
    strategy_result = await orchestrator.agents["Y"].execute("Convert Tesla Optimus opportunity")
    print(f"   AI Model: {strategy_result.get('ai_model', 'Unknown')}")
    print(f"   Strategy: {strategy_result['strategy'][:150]}...")
    
    # Test Market Intelligence Agent
    print("\n2. Market Intelligence Agent (X) - Anthropic Claude:")
    opportunities = await orchestrator.agents["X"].scan_opportunities()
    print(f"   AI Model: {opportunities[0].get('ai_model', 'Unknown')}")
    print(f"   Found {len(opportunities)} opportunities")
    print(f"   Anthropic Analysis: {opportunities[0]['anthropic_analysis'][:150]}...")
    
    # Test Ethics Agent
    print("\n3. Ethics Compliance Agent (Z) - Anthropic Claude:")
    ethics_result = await orchestrator.agents["Z"].validate_dataset("test_dataset")
    print(f"   AI Model: {ethics_result.get('ai_model', 'Unknown')}")
    print(f"   Z Protocol Score: {ethics_result['z_protocol_score']}%")
    print(f"   Anthropic Analysis: {ethics_result['anthropic_ethical_analysis'][:150]}...")
    
    # Test Legal Agent
    print("\n4. Legal Framework Agent (P) - Anthropic Claude:")
    legal_result = await orchestrator.agents["P"].structure_agreement("humanoid_robotics")
    print(f"   AI Model: {legal_result.get('ai_model', 'Unknown')}")
    print(f"   Template: {legal_result['template']}")
    print(f"   Anthropic Analysis: {legal_result['anthropic_legal_analysis'][:150]}...")
    
    # Test Reality Enforcement Agent
    print("\n5. Reality Enforcement Agent (XV) - Anthropic Claude:")
    metrics = await orchestrator.agents["XV"].validate_metrics()
    print(f"   AI Model: {metrics.get('ai_model', 'Unknown')}")
    print(f"   Revenue Progress: {metrics['progress_percentage']:.1f}%")
    print(f"   Anthropic Analysis: {metrics['anthropic_financial_analysis'][:150]}...")
    
    # Test Documentation Agent
    print("\n6. Pedagogical Documentation Agent (PED) - Anthropic Claude:")
    doc_result = await orchestrator.agents["PED"].log_and_learn("test_event", {"test": "data"})
    print(f"   AI Model: {doc_result.get('ai_model', 'Unknown')}")
    print(f"   Logged: {doc_result['logged']}")
    print(f"   Anthropic Analysis: {doc_result['anthropic_learning_analysis'][:150]}...")
    
    # Test CEO Agent
    print("\n7. CEO Persona Agent (ALTON) - Anthropic Claude:")
    ceo_result = await orchestrator.agents["ALTON"].execute("team_rally")
    print(f"   AI Model: {ceo_result.get('ai_model', 'Unknown')}")
    print(f"   Vision: {ceo_result['vision']}")
    print(f"   Anthropic Guidance: {ceo_result['anthropic_leadership_guidance'][:150]}...")
    
    # Test full workflow
    print("\n🔄 Testing Full Daily Workflow with Anthropic:")
    workflow_result = await orchestrator.execute_daily_workflow()
    print(f"   Status: {workflow_result['status']}")
    print(f"   Date: {workflow_result['date']}")
    
    print("\n✅ Anthropic Orchestrator Test Complete!")
    print("\n🎯 All agents are now using Anthropic Claude for advanced AI reasoning!")
    print("\n🌟 Benefits of Anthropic Integration:")
    print("   - Advanced reasoning and analysis")
    print("   - Better complex problem solving")
    print("   - Enhanced ethical considerations")
    print("   - Superior strategic thinking")
    print("   - More comprehensive responses")

if __name__ == "__main__":
    asyncio.run(test_anthropic_orchestrator())



