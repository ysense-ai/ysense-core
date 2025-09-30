# test_methodology_engine.py
"""
Test script for the new Methodology Core Engine
Tests the 3-stage methodology with a sample story
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.methodology_core_engine import methodology_engine

def test_methodology():
    """Test the methodology with a sample story"""
    
    print("🧪 Testing YSense™ Methodology Core Engine")
    print("=" * 50)
    
    # Sample story (similar to the one in the image)
    sample_story = """
    There were ten of us on that trip, and seven or eight were girls. 
    I got along with everyone really well. They mostly spoke in their 
    local Kelantanese dialect, which I didn't understand, but they 
    loved to joke around with me about it. It made everything even 
    more fun. Slowly, I even picked up a few words from them. After 
    the trip, I wrote a postcard to reflect on the whole experience. 
    At first, I wanted to send it individually to close friends and 
    old classmates. In the end, I decided to just post it online as 
    a memory. That postcard, that trip, and those moments still 
    mean a lot to me.
    """
    
    print(f"📝 Sample Story: {sample_story[:100]}...")
    print()
    
    try:
        # Process the story through the methodology
        print("🔄 Processing through 3-stage methodology...")
        results = methodology_engine.process_user_story(
            user_story=sample_story,
            cultural_context="Malaysian cultural exchange",
            target_audience="young adults, travelers",
            priority_focus="Connection",
            analysis_depth="Standard"
        )
        
        print("✅ Analysis completed!")
        print()
        
        # Display results
        print("📊 RESULTS SUMMARY:")
        print("-" * 30)
        
        if "session_id" in results:
            print(f"Session ID: {results['session_id']}")
        
        if "methodology_stages" in results:
            stages = results["methodology_stages"]
            
            # Stage 1: Experiential Data
            if "stage_1_experiential_extraction" in stages:
                exp_data = stages["stage_1_experiential_extraction"]
                print("\n🎯 Stage 1: Experiential Data Extraction")
                print(f"  • Emotional Journey: {exp_data.get('emotional_journey', 'N/A')}")
                print(f"  • Key Experiences: {exp_data.get('key_experiences', 'N/A')}")
                print(f"  • Learning Moments: {exp_data.get('learning_moments', 'N/A')}")
            
            # Stage 2: Vibe Analysis
            if "stage_2_vibe_resonance" in stages:
                vibe_data = stages["stage_2_vibe_resonance"]
                print("\n💫 Stage 2: Deep Dive Vibe - 3-Word Resonance")
                
                if "primary_vibe_word" in vibe_data:
                    primary = vibe_data["primary_vibe_word"]
                    print(f"  🔥 Primary Vibe: {primary.get('word', 'N/A')} - {primary.get('resonance', 'N/A')}")
                
                if "secondary_resonance_word" in vibe_data:
                    secondary = vibe_data["secondary_resonance_word"]
                    print(f"  🌟 Secondary Resonance: {secondary.get('word', 'N/A')} - {secondary.get('resonance', 'N/A')}")
                
                if "tertiary_essence_word" in vibe_data:
                    tertiary = vibe_data["tertiary_essence_word"]
                    print(f"  💎 Tertiary Essence: {tertiary.get('word', 'N/A')} - {tertiary.get('resonance', 'N/A')}")
                
                print(f"  • Authenticity Score: {vibe_data.get('authenticity_score', 'N/A')}/10")
                print(f"  • Energy Level: {vibe_data.get('energy_level', 'N/A')}/10")
            
            # Stage 3: Full Analysis
            if "stage_3_full_analysis" in stages:
                analysis_data = stages["stage_3_full_analysis"]
                print("\n🤖 Stage 3: Full AI Analysis")
                print(f"  • Executive Summary: {analysis_data.get('executive_summary', 'N/A')[:100]}...")
                print(f"  • Market Strategy: {analysis_data.get('market_strategy', 'N/A')}")
        
        # Z Protocol Score
        if "z_protocol_score" in results:
            score_data = results["z_protocol_score"]
            print(f"\n📈 Z Protocol Score: {score_data.get('overall_score', 'N/A')}/100")
            print(f"  • Grade: {score_data.get('grade', 'N/A')}")
        
        # Revenue Potential
        if "revenue_potential" in results:
            revenue_data = results["revenue_potential"]
            print(f"\n💰 Revenue Potential: {revenue_data.get('revenue_score', 'N/A')}/100")
            print(f"  • Tier: {revenue_data.get('potential_tier', 'N/A')}")
        
        print("\n🎉 Methodology test completed successfully!")
        
        # Check for fallback mode
        if "methodology_stages" in results:
            stages = results["methodology_stages"]
            fallback_detected = False
            for stage_name, stage_data in stages.items():
                if isinstance(stage_data, dict) and stage_data.get('fallback_mode', False):
                    fallback_detected = True
                    break
            
            if fallback_detected:
                print("\n⚠️  Note: Analysis completed in fallback mode (API may not be configured)")
            else:
                print("\n✅ Analysis completed with full AI integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_methodology()
    if success:
        print("\n🚀 Ready to launch the new methodology in YSense™ v4.1!")
    else:
        print("\n🔧 Please check the configuration and try again.")



