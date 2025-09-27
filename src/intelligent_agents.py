# src/intelligent_agents.py
"""
Intelligent Agents that extract meaningful moments from user stories
Each agent has a specific lens for finding value in human wisdom
"""

from qwen_integration import QWENClient, QWENWisdomExtractor
from typing import Dict, List
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

class IntelligentYSenseAgent:
    """Base class for intelligent agents using QWEN"""
    
    def __init__(self, role: str, focus: str):
        self.role = role
        self.focus = focus
        self.client = QWENClient()
    
    async def extract_moment(self, story: str) -> Dict:
        """Extract meaningful moment using QWEN"""
        try:
            response = self.client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": f"You are {self.role}, focused on {self.focus}. Extract the most meaningful moment from this story."},
                    {"role": "user", "content": f"Story: {story}\n\nFind the golden moment that matters for {self.focus}. Respond with insight and empathy."}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return {
                "agent": self.role,
                "insight": response.choices[0].message.content,
                "focus": self.focus
            }
        except:
            return {"agent": self.role, "insight": "Reflecting on your wisdom...", "focus": self.focus}

class WisdomExtractionTeam:
    """All 7 agents working together to extract wisdom"""
    
    def __init__(self):
        self.extractor = QWENWisdomExtractor()
        
        # Each agent with their unique perspective
        self.agents = {
            "Y": IntelligentYSenseAgent("Y-Strategy", "finding teaching patterns that scale globally"),
            "X": IntelligentYSenseAgent("X-Intelligence", "identifying valuable market insights"),
            "Z": IntelligentYSenseAgent("Z-Ethics", "ensuring dignity and consent in every story"),
            "P": IntelligentYSenseAgent("P-Legal", "protecting attribution rights"),
            "XV": IntelligentYSenseAgent("XV-Reality", "measuring real-world impact"),
            "PED": IntelligentYSenseAgent("PED-Learning", "capturing timeless lessons"),
            "ALTON": IntelligentYSenseAgent("ALTON-Vision", "seeing the human bridge to AI")
        }
    
    async def process_user_story(self, story: str, culture: str) -> Dict:
        """Process story through all agents collaboratively"""
        
        # Step 1: Five-Layer Extraction with QWEN
        layers = await self.extractor.extract_five_layers(story, culture)
        
        # Step 2: Each agent finds their moment
        agent_insights = {}
        for name, agent in self.agents.items():
            moment = agent.extract_moment(story)
            agent_insights[name] = moment["insight"]
        
        # Step 3: Synthesize into unified response
        unified_response = await self.synthesize_response(story, layers, agent_insights)
        
        return {
            "layers": layers,
            "agent_insights": agent_insights,
            "unified_response": unified_response,
            "quality_score": self.calculate_quality(layers),
            "revenue_potential": self.calculate_revenue(layers)
            "culture": culture	
        }
    
    async def extract_five_layers(self, story: str, culture: str) -> Dict:
        """Extract Five-Layer Perception using LLM"""
        
        prompt = f"""
        Extract five layers of wisdom from this {culture} story:
        
        Story: {story}
        
        Return as JSON with these exact keys:
        - surface: What literally happened
        - emotional: The feeling captured
        - contextual: Cultural/situational context  
        - wisdom: Universal lesson learned
        - cultural: Unique {culture} perspective
        
        Be concise but profound. Find the human moment that matters.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You extract deep wisdom from human stories for AI learning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            layers = json.loads(response.choices[0].message.content)
            return layers
        except:
            return {
                "surface": "Processing your story...",
                "emotional": "Feeling the moment...",
                "contextual": f"Understanding {culture} context...",
                "wisdom": "Extracting wisdom...",
                "cultural": f"Preserving {culture} perspective..."
            }
    
    async def synthesize_response(self, story: str, layers: Dict, agent_insights: Dict) -> str:
        """Create beautiful unified response to user"""
        
        synthesis_prompt = f"""
        Create a warm, meaningful response to someone who shared their wisdom.
        
        Their story essence:
        - Wisdom found: {layers.get('wisdom', '')}
        - Cultural gift: {layers.get('cultural', '')}
        - Emotional core: {layers.get('emotional', '')}
        
        Key insights from our team:
        - Vision (ALTON): {agent_insights.get('ALTON', '')}
        - Learning (PED): {agent_insights.get('PED', '')}
        
        Write a 2-3 sentence response that:
        1. Honors their contribution
        2. Shows we deeply understood
        3. Explains how this wisdom will help AI learn
        
        Be warm, genuine, and specific to their story.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You craft meaningful responses that make people feel their wisdom matters."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content
        except:
            return "Your wisdom has been received with gratitude. Every story shared helps AI understand the beauty of human experience."
    
    def _calculate_quality(self, layers: Dict) -> float:
        """Calculate quality score"""
        filled = sum(1 for v in layers.values() if v and len(str(v)) > 20)
        return (filled / 5.0) * 100
    
    def _calculate_revenue(self, layers: Dict, culture: str) -> float:
        """Calculate revenue potential"""
        base_rate = 50.0  # EUR
        quality = self._calculate_quality(layers) / 100
        
        cultural_multipliers = {
            'Malaysian': 1.6,
            'Southeast Asian': 1.3,
            'Global': 1.0
        }
        
        multiplier = cultural_multipliers.get(culture, 1.0)
        return round(base_rate * quality * multiplier, 2)

# Interactive Response Generator for UI
class WisdomResponseGenerator:
    """Generate meaningful responses for the Streamlit UI"""
    
    def __init__(self):
        self.team = WisdomExtractionTeam()
    
    async def respond_to_user(self, story: str, culture: str, contributor_id: str) -> Dict:
        """Complete response flow for user story"""
        
        # Process through intelligent agents
        result = await self.team.process_user_story(story, culture)
        
        # Format for beautiful display
        return {
            "greeting": f"Thank you for sharing your {culture} wisdom.",
            "layers_found": result["layers"],
            "team_response": result["unified_response"],
            "special_moments": {
                "Y-Strategy": result["agent_insights"]["Y"],
                "Z-Ethics": result["agent_insights"]["Z"],
                "PED-Learning": result["agent_insights"]["PED"]
            },
            "quality_score": result["quality_score"],
            "earning": f"€{result['revenue_potential']:.2f}",
            "message": "Your wisdom is now part of humanity's gift to AI."
        }

# Test the intelligent agents
async def test_intelligent_agents():
    """Test agent collaboration"""
    
    generator = WisdomResponseGenerator()
    
    # Malaysian wisdom example
    test_story = """
    In my kampung, when teaching children to cook rendang, we never measure spices.
    Instead, grandmother says 'listen to the sizzle, it tells you when ready.'
    This patience I now teach to robots - not everything needs numbers.
    """
    
    response = await generator.respond_to_user(
        story=test_story,
        culture="Malaysian",
        contributor_id="MY_001"
    )
    
    print("YSense Intelligent Response:")
    print("=" * 60)
    print(response["greeting"])
    print(f"\n{response['team_response']}")
    print(f"\nQuality Score: {response['quality_score']:.2f}")
    print(f"Your Earning: {response['earning']}")
    print("\nSpecial Moments Found by Agents:")
    for agent, moment in response["special_moments"].items():
        print(f"\n{agent}: {moment[:100]}...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_intelligent_agents())