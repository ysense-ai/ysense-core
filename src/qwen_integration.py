# qwen_integration.py
"""
YSense Platform v3.0 - QWEN API Integration
Replaces OpenAI with Alibaba Cloud QWEN for cost efficiency
"""

import os
import json
import httpx
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
from dotenv import load_dotenv

load_dotenv()

class QWENClient:
    """QWEN API client for YSense intelligent agents"""
    
    def __init__(self):
        self.api_key = os.getenv("QWEN_API_KEY", "")
        self.model = os.getenv("QWEN_MODEL", "qwen-turbo")  # qwen-turbo, qwen-plus, qwen-max
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        if not self.api_key:
            print("⚠️ QWEN_API_KEY not found. Using fallback mode.")
            self.use_fallback = True
        else:
            self.use_fallback = False
    
    async def create_completion(self, messages: List[Dict], 
                               temperature: float = 0.7,
                               max_tokens: int = 500) -> str:
        """Create completion using QWEN API"""
        
        if self.use_fallback:
            return self._fallback_response(messages)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert OpenAI format to QWEN format
        qwen_messages = []
        for msg in messages:
            qwen_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        payload = {
            "model": self.model,
            "input": {
                "messages": qwen_messages
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.8,
                "repetition_penalty": 1.1,
                "result_format": "message"
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Extract text from QWEN response format
                    if "output" in result and "choices" in result["output"]:
                        return result["output"]["choices"][0]["message"]["content"]
                    return result.get("output", {}).get("text", "Processing...")
                else:
                    print(f"QWEN API Error: {response.status_code}")
                    return self._fallback_response(messages)
                    
        except Exception as e:
            print(f"QWEN API Exception: {e}")
            return self._fallback_response(messages)
    
    def _fallback_response(self, messages: List[Dict]) -> str:
        """Fallback response when API is unavailable"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "extract" in last_message.lower():
            return "Extracting wisdom layers from your story..."
        elif "feedback" in last_message.lower():
            return "Your wisdom captures profound human experience."
        else:
            return "Processing your wisdom with Malaysian innovation..."

class QWENWisdomExtractor:
    """Specialized QWEN client for wisdom extraction"""
    
    def __init__(self):
        self.client = QWENClient()
    
    async def extract_five_layers(self, story: str, culture: str) -> Dict:
        """Extract Five-Layer Perception using QWEN"""
        
        prompt = f"""
        Extract five layers of wisdom from this {culture} story.
        
        Story: {story}
        
        Return as JSON with these exact keys:
        - surface: What literally happened (facts and events)
        - emotional: The emotions and feelings captured
        - contextual: Cultural and situational context
        - wisdom: Universal lesson or insight learned
        - cultural: Unique {culture} cultural perspective
        
        Be concise but profound. Find the human moment that matters for AI training.
        Format: Valid JSON only, no markdown.
        """
        
        messages = [
            {"role": "system", "content": "You extract deep wisdom from human stories for ethical AI training."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.client.create_completion(
            messages=messages,
            temperature=0.6,
            max_tokens=400
        )
        
        try:
            # Clean response and parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            
            return json.loads(cleaned)
        except:
            # Fallback structure
            return {
                "surface": "Processing your story...",
                "emotional": "Feeling the moment...",
                "contextual": f"Understanding {culture} context...",
                "wisdom": "Extracting wisdom...",
                "cultural": f"Preserving {culture} perspective..."
            }
    
    async def generate_agent_feedback(self, wisdom_drop: Dict, agent_role: str) -> str:
        """Generate feedback from specific agent perspective"""
        
        agent_prompts = {
            "Y-Strategy": "As Chief Strategy Officer, what market value does this wisdom have?",
            "X-Intelligence": "As Market Intelligence, what insights can AI companies gain?",
            "Z-Ethics": "As Ethics Officer, how does this preserve human dignity?",
            "P-Legal": "As Legal Framework, how is attribution protected?",
            "XV-Reality": "As Reality Enforcement, what's the revenue potential?",
            "PED-Learning": "As Documentation Officer, what timeless lesson is captured?",
            "ALTON-Vision": "As CEO, how does this bridge human wisdom to AI?"
        }
        
        prompt = agent_prompts.get(agent_role, "What value does this wisdom provide?")
        
        messages = [
            {"role": "system", "content": f"You are {agent_role} of YSense, evaluating human wisdom."},
            {"role": "user", "content": f"{prompt}\n\nWisdom: {json.dumps(wisdom_drop)}"}
        ]
        
        return await self.client.create_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )

# Test the QWEN integration
async def test_qwen_integration():
    """Test QWEN API connection and wisdom extraction"""
    
    print("🚀 Testing YSense v3.0 QWEN Integration")
    print("=" * 60)
    
    extractor = QWENWisdomExtractor()
    
    # Test story
    test_story = """
    In my kampung, grandmother teaches patience through making rendang.
    Six hours of slow cooking, she says, cannot be rushed by modern flames.
    Each stir carries generations of wisdom - the paste darkens like memories
    deepening with time. Now I teach robots this patience, that not everything
    needs optimization. Some processes honor the journey, not just the destination.
    """
    
    # Test extraction
    print("\n📝 Testing Five-Layer Extraction...")
    layers = await extractor.extract_five_layers(test_story, "Malaysian")
    print(json.dumps(layers, indent=2))
    
    # Test agent feedback
    print("\n🤖 Testing Agent Feedback...")
    feedback = await extractor.generate_agent_feedback(layers, "Y-Strategy")
    print(f"Y-Strategy: {feedback}")
    
    print("\n✅ QWEN Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_qwen_integration())