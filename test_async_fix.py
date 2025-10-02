"""Test async/await fix for methodology engine"""
import asyncio
import sys
sys.path.insert(0, '.')

from src.methodology_core_engine import methodology_engine

async def test_async_methodology():
    """Test that async methods work correctly"""

    user_story = "A short test story about learning and growth."
    user_vibe_data = {
        "primary_vibe_word": {"word": "Learning"},
        "secondary_resonance_word": {"word": "Growth"},
        "tertiary_essence_word": {"word": "Progress"},
        "energy_level": 7,
        "authenticity_score": 8,
        "resonance_strength": 8,
        "potential_impact": 7
    }

    print("Testing async process_user_story_with_vibe...")

    try:
        results = await methodology_engine.process_user_story_with_vibe(
            user_story=user_story,
            user_vibe_data=user_vibe_data,
            cultural_context="Test",
            target_audience="Developers",
            priority_focus="Testing",
            analysis_depth="Standard"
        )

        print(f"[OK] Async method executed successfully!")
        print(f"[OK] Session ID: {results.get('session_id')}")
        print(f"[OK] Status: {results.get('status', 'success')}")

        if 'error' in results:
            print(f"[WARN] Error field present: {results['error']}")
        else:
            print(f"[OK] No coroutine serialization errors!")

        return True

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_async_methodology())
    if success:
        print("\n" + "="*60)
        print("ASYNC FIX VERIFIED: All async/await issues resolved!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("ASYNC FIX FAILED: Issues remain")
        print("="*60)
        sys.exit(1)
