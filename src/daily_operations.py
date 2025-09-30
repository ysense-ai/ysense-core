# daily_operations.py (FIXED)
import asyncio
from datetime import datetime
import sys
import os

# Fix the import path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.orchestrator import YSenseOrchestrator
except ImportError:
    from orchestrator import YSenseOrchestrator

class YSenseDailyOperations:
    def __init__(self):
        self.orchestrator = YSenseOrchestrator()
        
    async def morning_routine(self):
        """Execute morning workflow"""
        print(f"\n🌅 YSense Morning Routine - {datetime.now().strftime('%Y-%m-%d')}")
        print("=" * 60)
        
        # XV: Reality Check
        print("\n📊 XV Reality Check:")
        metrics = await self.orchestrator.agents["XV"].validate_metrics()
        if metrics["overall_status"] == "CRITICAL":
            print("⚠️ CRITICAL: Immediate action needed!")
        else:
            print("✅ Metrics on track")
        
        # X: Market Intelligence
        print("\n🔍 X Market Scan:")
        opportunities = await self.orchestrator.agents["X"].scan_opportunities()
        print(f"Found {len(opportunities)} opportunities")
        
        # Y: Strategic Planning
        print("\n📋 Y Strategy Execution:")
        for opp in opportunities[:3]:
            strategy = await self.orchestrator.agents["Y"].execute(
                f"Convert {opp['segment']} opportunity"
            )
            print(f"  • {opp['segment']}: Processing...")
        
        return {
            "metrics": metrics,
            "opportunities": opportunities,
            "timestamp": datetime.now()
        }

if __name__ == "__main__":
    ops = YSenseDailyOperations()
    asyncio.run(ops.morning_routine())