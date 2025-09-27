#!/usr/bin/env python3
"""
Test Enhanced LayerAnalyzer with QWEN Integration
Demonstrates unique quality scores and revenue potential based on user input
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.layer_analyzer import LayerAnalyzer

async def test_enhanced_analysis():
    """Test the enhanced LayerAnalyzer with different wisdom stories"""
    print("🧠 Testing Enhanced LayerAnalyzer with QWEN Integration")
    print("=" * 70)
    
    # Initialize analyzer with QWEN
    analyzer = LayerAnalyzer()
    
    # Test different wisdom stories to show unique scoring
    test_stories = [
        {
            "title": "Malaysian Innovation Story",
            "content": """
            In my kampung in Teluk Intan, I learned that innovation comes from patience and community.
            When building our YSense platform, I realized that defensive publication is more powerful 
            than patents for open-source projects. This reflects our Malaysian values of sharing 
            while protecting attribution. I felt proud creating something that honors both tradition 
            and progress. The lesson is that true innovation bridges the old and new, respecting 
            cultural heritage while building the future.
            """,
            "author": "Alton Lee Wei Bin",
            "culture": "Malaysian"
        },
        {
            "title": "Simple Daily Wisdom",
            "content": """
            Today I helped my neighbor fix their bicycle. It was a small act but it made me happy.
            I learned that helping others brings joy to both people.
            """,
            "author": "Test User",
            "culture": "Global"
        },
        {
            "title": "Deep Cultural Wisdom",
            "content": """
            My grandmother taught me the ancient art of making traditional rendang in our ancestral 
            kitchen. Through six hours of patient stirring, she revealed the fundamental principle 
            that not everything can be rushed - some processes honor the journey itself. This timeless 
            wisdom of patience and respect for tradition has guided me in building ethical AI systems 
            that preserve human dignity. The cultural heritage of our indigenous practices holds 
            universal truths about sustainable innovation and community harmony.
            """,
            "author": "Cultural Keeper",
            "culture": "Indigenous"
        }
    ]
    
    print("\n📊 Analyzing Different Wisdom Stories:")
    print("=" * 50)
    
    for i, story in enumerate(test_stories, 1):
        print(f"\n{i}. {story['title']}")
        print(f"   Author: {story['author']} | Culture: {story['culture']}")
        print(f"   Content: {story['content'][:100]}...")
        
        # Analyze the story
        wisdom = await analyzer.analyze_wisdom(
            story['content'],
            story['author'],
            story['culture']
        )
        
        print(f"\n   🎯 Analysis Results:")
        print(f"   Quality Score: {wisdom['quality_score']:.3f}")
        print(f"   Revenue Potential: €{wisdom['revenue_potential']:.2f}")
        
        print(f"\n   📝 Five Layers:")
        for layer, content in wisdom['layers'].items():
            print(f"   {layer.upper()}: {content[:80]}...")
        
        print(f"\n   🔍 Revenue Breakdown:")
        print(f"   Base Rate: €50.00")
        print(f"   Cultural Multiplier: {analyzer.cultural_multipliers.get(story['culture'], 1.0)}x")
        print(f"   Quality Factor: {wisdom['quality_score']:.3f}")
        
        # Show dynamic factors
        if wisdom['layers']:
            wisdom_value = analyzer._assess_wisdom_value(wisdom['layers'].get('wisdom', ''))
            cultural_rarity = analyzer._assess_cultural_rarity(wisdom['layers'].get('cultural', ''))
            commercial_value = analyzer._assess_commercial_value(wisdom['layers'])
            
            print(f"   Wisdom Value: {wisdom_value:.2f}x")
            print(f"   Cultural Rarity: {cultural_rarity:.2f}x")
            print(f"   Commercial Value: {commercial_value:.2f}x")
        
        print("-" * 50)
    
    print("\n🎉 Enhanced Analysis Complete!")
    print("\n🌟 Key Improvements:")
    print("   ✅ QWEN AI integration for deep analysis")
    print("   ✅ Dynamic quality scoring based on content")
    print("   ✅ Intelligent revenue calculation")
    print("   ✅ Cultural rarity assessment")
    print("   ✅ Commercial value evaluation")
    print("   ✅ Unique scoring for each user input")

if __name__ == "__main__":
    asyncio.run(test_enhanced_analysis())



