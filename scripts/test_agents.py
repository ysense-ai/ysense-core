"""Test multi-agent system"""
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator import YSenseOrchestrator

async def test_agents():
    print("Testing YSense Multi-Agent System...")
    orchestrator = YSenseOrchestrator()
    result = await orchestrator.execute_daily_workflow()
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_agents())