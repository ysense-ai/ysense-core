#!/usr/bin/env python3
"""
Test script for YSense Orchestrator with QWEN API integration
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.orchestrator import YSenseOrchestrator

async def test_orchestrator():
    """Test the orchestrator with AI integration"""
    print("🚀 Testing YSense Orchestrator with QWEN API")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = YSenseOrchestrator()
    
    # Test individual agents
    print("\n📊 Testing Individual Agents:")
    
    # Test Strategy Agent
    print("\n1. Strategy Agent (Y):")
    strategy_result = await orchestrator.agents["Y"].execute("Convert Tesla Optimus opportunity")
    print(f"   Strategy: {strategy_result['strategy'][:100]}...")
    
    # Test Market Intelligence Agent
    print("\n2. Market Intelligence Agent (X):")
    opportunities = await orchestrator.agents["X"].scan_opportunities()
    print(f"   Found {len(opportunities)} opportunities")
    print(f"   AI Analysis: {opportunities[0]['ai_analysis'][:100]}...")
    
    # Test Ethics Agent
    print("\n3. Ethics Compliance Agent (Z):")
    ethics_result = await orchestrator.agents["Z"].validate_dataset("test_dataset")
    print(f"   Z Protocol Score: {ethics_result['z_protocol_score']}%")
    print(f"   AI Analysis: {ethics_result['ai_analysis'][:100]}...")
    
    # Test Legal Agent
    print("\n4. Legal Framework Agent (P):")
    legal_result = await orchestrator.agents["P"].structure_agreement("humanoid_robotics")
    print(f"   Template: {legal_result['template']}")
    print(f"   AI Analysis: {legal_result['ai_legal_analysis'][:100]}...")
    
    # Test Reality Enforcement Agent
    print("\n5. Reality Enforcement Agent (XV):")
    metrics = await orchestrator.agents["XV"].validate_metrics()
    print(f"   Revenue Progress: {metrics['progress_percentage']:.1f}%")
    print(f"   AI Analysis: {metrics['ai_analysis'][:100]}...")
    
    # Test Documentation Agent
    print("\n6. Pedagogical Documentation Agent (PED):")
    doc_result = await orchestrator.agents["PED"].log_and_learn("test_event", {"test": "data"})
    print(f"   Logged: {doc_result['logged']}")
    print(f"   AI Analysis: {doc_result['ai_analysis'][:100]}...")
    
    # Test CEO Agent
    print("\n7. CEO Persona Agent (ALTON):")
    ceo_result = await orchestrator.agents["ALTON"].execute("team_rally")
    print(f"   Vision: {ceo_result['vision']}")
    print(f"   AI Guidance: {ceo_result['ai_leadership_guidance'][:100]}...")
    
    # Test full workflow
    print("\n🔄 Testing Full Daily Workflow:")
    workflow_result = await orchestrator.execute_daily_workflow()
    print(f"   Status: {workflow_result['status']}")
    print(f"   Date: {workflow_result['date']}")
    
    print("\n✅ Orchestrator Test Complete!")
    print("\n🎯 All agents are now using QWEN API for AI-powered analysis!")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())



