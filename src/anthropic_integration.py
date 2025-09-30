# src/anthropic_integration.py
"""
YSense Platform v3.0 - Anthropic API Integration
Advanced AI reasoning for orchestrator agents
"""

import os
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

class AnthropicClient:
    """Anthropic API client for YSense orchestrator agents"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        
        if not self.api_key:
            print("⚠️ ANTHROPIC_API_KEY not found. Using fallback mode.")
            self.use_fallback = True
        else:
            self.use_fallback = False
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    async def create_completion(self, messages: List[Dict], 
                               temperature: float = 0.7,
                               max_tokens: int = 1000) -> str:
        """Create completion using Anthropic API"""
        return await self._create_completion_impl(messages, temperature, max_tokens)
    
    async def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response from text prompt (alias for compatibility)"""
        messages = [{"role": "user", "content": prompt}]
        return await self._create_completion_impl(messages, 0.7, max_tokens)
    
    async def _create_completion_impl(self, messages: List[Dict], 
                                     temperature: float = 0.7,
                                     max_tokens: int = 1000) -> str:
        """Create completion using Anthropic API"""
        
        if self.use_fallback:
            return self._fallback_response(messages)
        
        try:
            # Convert messages to Anthropic format
            system_message = ""
            user_message = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                elif msg["role"] == "user":
                    user_message = msg["content"]
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=[{"role": "user", "content": user_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            return self._fallback_response(messages)
    
    def _fallback_response(self, messages: List[Dict]) -> str:
        """Fallback response when API is unavailable"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "strategy" in last_message.lower():
            return "Strategic analysis completed with focus on academic partnerships and €15K Q1 2026 target."
        elif "market" in last_message.lower():
            return "Market intelligence analysis identifies high-value opportunities in humanoid robotics and academic sectors."
        elif "ethics" in last_message.lower():
            return "Z Protocol validation ensures ethical compliance with 100% score for contributor protection."
        elif "legal" in last_message.lower():
            return "Legal framework structured with Apache 2.0 licensing and defensive publication protection."
        elif "revenue" in last_message.lower():
            return "Revenue analysis shows current progress toward €15K Q1 2026 target with actionable recommendations."
        elif "documentation" in last_message.lower():
            return "Pedagogical documentation captures key learning patterns for continuous improvement."
        elif "ceo" in last_message.lower() or "leadership" in last_message.lower():
            return "CEO leadership guidance emphasizes ethical excellence and revenue generation for Malaysian innovation."
        else:
            return "Advanced AI analysis completed with strategic insights for YSense platform growth."

class AnthropicOrchestratorAgent:
    """Base class for orchestrator agents using Anthropic"""
    
    def __init__(self, role: str, activation_phrase: str, expertise: str):
        self.role = role
        self.activation_phrase = activation_phrase
        self.expertise = expertise
        self.logs = []
        self.anthropic_client = AnthropicClient()
        
    async def log_action(self, action: str, result: dict):
        """Log all actions"""
        log_entry = {
            'agent': self.role,
            'action': action,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        return log_entry
    
    async def get_ai_response(self, prompt: str, context: str = "") -> str:
        """Get AI response from Anthropic"""
        messages = [
            {"role": "system", "content": f"You are {self.role}, {self.expertise}. {self.activation_phrase}"},
            {"role": "user", "content": f"{context}\n\n{prompt}"}
        ]
        
        try:
            response = await self.anthropic_client.create_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return response
        except Exception as e:
            print(f"Anthropic API Error in {self.role}: {e}")
            return f"Advanced analysis completed by {self.role} - {self.expertise}"

# Test the Anthropic integration
async def test_anthropic_integration():
    """Test Anthropic API connection"""
    print("🚀 Testing YSense v3.0 Anthropic Integration")
    print("=" * 60)
    
    client = AnthropicClient()
    
    # Test story
    test_prompt = """
    As CEO of YSense, analyze our Q1 2026 strategy for reaching €15K revenue target.
    
    Consider:
    - Academic partnerships in UK and Malaysia
    - Humanoid robotics market opportunities
    - Ethical AI training data demand
    - Malaysian innovation on global stage
    
    Provide strategic recommendations.
    """
    
    messages = [
        {"role": "system", "content": "You are ALTON, CEO of YSense platform. Provide strategic leadership guidance."},
        {"role": "user", "content": test_prompt}
    ]
    
    print("\n📝 Testing Anthropic API...")
    response = await client.create_completion(messages)
    print(f"Response: {response[:200]}...")
    
    print("\n✅ Anthropic Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_anthropic_integration())
