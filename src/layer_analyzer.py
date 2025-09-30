# layer_analyzer.py
"""
YSense™ Five-Layer Deep Analysis Engine
Extracts maximum value from each wisdom drop
"""

import os
import json
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np

class LayerAnalyzer:
    """Deep analysis for Five-Layer Perception™"""
    
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        self.use_fallback = openai_client is None
        
        # Layer-specific prompts for deep analysis
        self.layer_prompts = {
            'surface': "Extract the factual events and observations: What specifically happened?",
            'emotional': "Identify the emotions and feelings: How did this experience feel?",
            'contextual': "Analyze the context: When, where, and why did this occur? What circumstances led to this?",
            'wisdom': "Extract the lesson or insight: What universal truth or learning emerged?",
            'cultural': "Identify cultural perspective: What cultural values, traditions, or viewpoints are present?"
        }
        
        # Cultural context multipliers for revenue
        self.cultural_multipliers = {
            'Malaysian': 1.5,
            'Southeast Asian': 1.3,
            'Asian': 1.2,
            'Global South': 1.15,
            'Indigenous': 1.4,
            'Default': 1.0
        }
    
    async def analyze_wisdom(self, raw_content: str, author: str, cultural_context: str = None) -> Dict:
        """
        Perform deep Five-Layer analysis on raw wisdom content
        """
        wisdom_drop = {
            'id': self._generate_id(raw_content, author),
            'timestamp': datetime.now().isoformat(),
            'author': author,
            'cultural_context': cultural_context or 'Global',
            'raw_content': raw_content,
            'layers': {},
            'quality_score': 0.0,
            'revenue_potential': 0.0,
            'consent_verified': False,
            'attribution_hash': '',
            'z_protocol_version': 'v2.0'
        }
        
        # Analyze each layer
        if self.use_fallback:
            wisdom_drop['layers'] = self._fallback_analysis(raw_content)
        else:
            wisdom_drop['layers'] = await self._deep_analysis(raw_content)
        
        # Calculate quality and revenue
        wisdom_drop['quality_score'] = self._calculate_quality(wisdom_drop['layers'])
        wisdom_drop['revenue_potential'] = self._calculate_revenue(
            wisdom_drop['quality_score'], 
            cultural_context
        )
        
        # Generate attribution hash
        wisdom_drop['attribution_hash'] = self._generate_attribution_hash(wisdom_drop)
        
        return wisdom_drop
    
    async def _deep_analysis(self, content: str) -> Dict[str, str]:
        """Use LLM for deep layer extraction"""
        layers = {}
        
        for layer_name, prompt in self.layer_prompts.items():
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are analyzing content for the {layer_name} layer of the Five-Layer Perception Framework."},
                        {"role": "user", "content": f"{prompt}\n\nContent: {content}"}
                    ],
                    max_tokens=150,
                    temperature=0.3
                )
                
                layers[layer_name] = response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"API call failed for {layer_name}: {e}")
                # Fallback to rule-based extraction
                layers[layer_name] = self._extract_layer_fallback(layer_name, content)
        
        return layers
    
    def _fallback_analysis(self, content: str) -> Dict[str, str]:
        """Rule-based analysis when API is unavailable"""
        return {
            'surface': self._extract_surface(content),
            'emotional': self._extract_emotional(content),
            'contextual': self._extract_contextual(content),
            'wisdom': self._extract_wisdom(content),
            'cultural': self._extract_cultural(content)
        }
    
    def _extract_surface(self, content: str) -> str:
        """Extract factual observations"""
        # Look for action words and facts
        keywords = ['did', 'made', 'created', 'built', 'achieved', 'completed', 'started']
        sentences = content.split('.')
        
        surface_facts = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                surface_facts.append(sentence.strip())
        
        return '. '.join(surface_facts[:3]) if surface_facts else content[:200]
    
    def _extract_emotional(self, content: str) -> str:
        """Extract emotional content"""
        emotion_words = {
            'positive': ['happy', 'excited', 'proud', 'grateful', 'inspired', 'confident'],
            'negative': ['frustrated', 'worried', 'anxious', 'disappointed', 'stressed'],
            'neutral': ['focused', 'determined', 'curious', 'thoughtful']
        }
        
        found_emotions = []
        content_lower = content.lower()
        
        for category, words in emotion_words.items():
            for word in words:
                if word in content_lower:
                    found_emotions.append(f"{category}: {word}")
        
        return ', '.join(found_emotions) if found_emotions else "Determined and focused"
    
    def _extract_contextual(self, content: str) -> str:
        """Extract context information"""
        context_markers = {
            'time': ['when', 'during', 'after', 'before', 'while'],
            'place': ['at', 'in', 'from', 'where'],
            'reason': ['because', 'since', 'due to', 'for', 'to']
        }
        
        context_info = []
        for category, markers in context_markers.items():
            for marker in markers:
                if marker in content.lower():
                    # Find sentence containing marker
                    for sentence in content.split('.'):
                        if marker in sentence.lower():
                            context_info.append(f"{category}: {sentence.strip()[:100]}")
                            break
                    break
        
        return ' | '.join(context_info) if context_info else "Professional context"
    
    def _extract_wisdom(self, content: str) -> str:
        """Extract learned lessons"""
        wisdom_indicators = ['learned', 'realized', 'discovered', 'understood', 
                           'lesson', 'insight', 'principle', 'truth']
        
        for indicator in wisdom_indicators:
            if indicator in content.lower():
                # Extract sentence with indicator
                for sentence in content.split('.'):
                    if indicator in sentence.lower():
                        return sentence.strip()
        
        # If no explicit wisdom, generate from content
        return f"Key insight from: {content[:100]}"
    
    def _extract_cultural(self, content: str) -> str:
        """Extract cultural perspective"""
        cultural_markers = {
            'Malaysian': ['Malaysia', 'Malaysian', 'Teluk Intan', 'kampung'],
            'Asian': ['Asian', 'Eastern', 'collective', 'harmony'],
            'Western': ['Western', 'individual', 'independent'],
            'Indigenous': ['indigenous', 'traditional', 'ancestral']
        }
        
        found_cultures = []
        for culture, markers in cultural_markers.items():
            if any(marker.lower() in content.lower() for marker in markers):
                found_cultures.append(culture)
        
        return ', '.join(found_cultures) if found_cultures else "Universal human perspective"
    
    def _calculate_quality(self, layers: Dict[str, str]) -> float:
        """Calculate quality score based on layer completeness"""
        scores = {
            'surface': 0.15,
            'emotional': 0.20,
            'contextual': 0.15,
            'wisdom': 0.30,  # Wisdom layer weighted higher
            'cultural': 0.20
        }
        
        quality = 0.0
        for layer, weight in scores.items():
            if layer in layers and layers[layer]:
                # Score based on content length and quality
                content = layers[layer]
                if len(content) > 20:  # Meaningful content
                    quality += weight
                elif len(content) > 10:  # Some content
                    quality += weight * 0.5
        
        return min(quality, 1.0)  # Cap at 1.0
    
    def _calculate_revenue(self, quality_score: float, cultural_context: str) -> float:
        """Calculate revenue potential in EUR"""
        base_rate = 50.0  # €50 base rate
        
        # Get cultural multiplier
        multiplier = self.cultural_multipliers.get(
            cultural_context, 
            self.cultural_multipliers['Default']
        )
        
        # Revenue = base × quality × cultural_multiplier
        revenue = base_rate * quality_score * multiplier
        
        # Apply bonus for high quality
        if quality_score >= 0.9:
            revenue *= 1.1  # 10% excellence bonus
        
        return round(revenue, 2)
    
    def _generate_id(self, content: str, author: str) -> str:
        """Generate unique ID for wisdom drop"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{author}_{content[:50]}_{timestamp}"
        return f"wisdom_{hashlib.md5(unique_string.encode()).hexdigest()[:8]}"
    
    def _generate_attribution_hash(self, wisdom_drop: Dict) -> str:
        """Generate cryptographic attribution hash"""
        attribution_data = {
            'author': wisdom_drop['author'],
            'timestamp': wisdom_drop['timestamp'],
            'content_hash': hashlib.sha256(
                wisdom_drop['raw_content'].encode()
            ).hexdigest()[:16]
        }
        
        attribution_string = json.dumps(attribution_data, sort_keys=True)
        return hashlib.sha256(attribution_string.encode()).hexdigest()
    
    def generate_embedding(self, content: str, use_mock: bool = False) -> List[float]:
        """Generate embedding vector for semantic search"""
        if use_mock:
            # Mock embedding for testing
            return [0.1] * 768
        
        try:
            # Use OpenAI embeddings
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=content
            )
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Embedding generation failed: {e}")
            # Fallback to simple hash-based pseudo-embedding
            return self._generate_pseudo_embedding(content)
    
    def _generate_pseudo_embedding(self, content: str) -> List[float]:
        """Generate deterministic pseudo-embedding from content"""
        # Create reproducible pseudo-random embedding
        np.random.seed(hash(content) % (2**32))
        embedding = np.random.randn(768) * 0.1
        return embedding.tolist()


# Example usage with fallback mode
if __name__ == "__main__":
    import asyncio
    
    # Initialize without OpenAI (fallback mode)
    analyzer = LayerAnalyzer(openai_client=None)
    
    # Test wisdom content
    test_content = """
    Today I successfully integrated the Five-Layer Perception framework into our 
    YSense platform in Teluk Intan. I felt proud and excited seeing the Malaysian 
    innovation taking shape. This happened because we needed a way to preserve 
    human wisdom ethically. I learned that defensive publication provides stronger 
    protection than patents for open-source projects. This reflects Malaysian values 
    of community sharing while protecting attribution rights.
    """
    
    # Analyze
    async def test_analysis():
        wisdom = await analyzer.analyze_wisdom(
            test_content,
            author="Alton Lee Wei Bin",
            cultural_context="Malaysian"
        )
        
        print("=== YSense Wisdom Analysis ===")
        print(f"ID: {wisdom['id']}")
        print(f"Quality Score: {wisdom['quality_score']:.2f}")
        print(f"Revenue Potential: €{wisdom['revenue_potential']:.2f}")
        print("\n--- Five Layers ---")
        for layer, content in wisdom['layers'].items():
            print(f"{layer.upper()}: {content}")
        print(f"\nAttribution Hash: {wisdom['attribution_hash']}")
    
    asyncio.run(test_analysis())