# layer_analyzer.py
"""
YSense™ Five-Layer Deep Analysis Engine
Extracts maximum value from each wisdom drop with QWEN AI integration
"""

import os
import json
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from src.qwen_integration import QWENClient

class LayerAnalyzer:
    """Deep analysis for Five-Layer Perception™"""
    
    def __init__(self, QWEN_client=None):
        self.QWEN_client = QWEN_client or QWENClient()
        self.use_fallback = not hasattr(self.QWEN_client, 'create_completion')
        
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
        
        # Calculate quality and revenue with enhanced analysis
        wisdom_drop['quality_score'] = self._calculate_quality(wisdom_drop['layers'])
        wisdom_drop['revenue_potential'] = self._calculate_revenue(
            wisdom_drop['quality_score'], 
            cultural_context,
            wisdom_drop['layers']  # Pass layers for dynamic revenue calculation
        )
        
        # Generate attribution hash
        wisdom_drop['attribution_hash'] = self._generate_attribution_hash(wisdom_drop)
        
        return wisdom_drop
    
    async def _deep_analysis(self, content: str) -> Dict[str, str]:
        """Use QWEN AI for deep layer extraction with enhanced prompts"""
        layers = {}
        
        # Enhanced prompts for better analysis
        enhanced_prompts = {
            'surface': """
            Extract the factual events and observations from this wisdom story.
            Focus on: What specifically happened? What actions were taken? What was achieved?
            Be specific and detailed about the concrete events.
            """,
            'emotional': """
            Identify the emotions, feelings, and inner experiences captured in this story.
            Focus on: How did this experience feel? What emotions were present? 
            What was the emotional journey? Include both positive and challenging emotions.
            """,
            'contextual': """
            Analyze the context, circumstances, and background of this experience.
            Focus on: When and where did this occur? What circumstances led to this?
            What was the situation or environment? What external factors influenced this?
            """,
            'wisdom': """
            Extract the universal lesson, insight, or wisdom from this experience.
            Focus on: What truth or principle emerged? What can others learn from this?
            What timeless insight was gained? What universal value does this hold?
            """,
            'cultural': """
            Identify the cultural perspective, values, and worldview present in this story.
            Focus on: What cultural values are expressed? What traditions or beliefs are shown?
            How does this reflect the contributor's cultural background? What cultural wisdom is shared?
            """
        }
        
        for layer_name, prompt in enhanced_prompts.items():
            try:
                response = await self.QWEN_client.create_completion(
                    messages=[
                        {
                            "role": "system", 
                            "content": f"You are an expert analyst for the YSense Five-Layer Perception Framework. You extract deep insights from human wisdom stories for ethical AI training. Focus on the {layer_name} layer with precision and cultural sensitivity."
                        },
                        {
                            "role": "user", 
                            "content": f"{prompt}\n\nWisdom Story: {content}\n\nProvide a detailed analysis for the {layer_name} layer:"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=200
                )
                
                layers[layer_name] = response.strip()
                
            except Exception as e:
                print(f"QWEN API call failed for {layer_name}: {e}")
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
        """Calculate intelligent quality score based on content depth and value"""
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
                content = layers[layer]
                
                # Enhanced quality scoring
                layer_score = self._analyze_layer_quality(content, layer)
                quality += weight * layer_score
        
        return min(quality, 1.0)  # Cap at 1.0
    
    def _analyze_layer_quality(self, content: str, layer_type: str) -> float:
        """Analyze the quality of a specific layer's content"""
        if not content or len(content.strip()) < 10:
            return 0.0
        
        # Base score from content length
        length_score = min(len(content) / 100, 1.0)  # Normalize to 0-1
        
        # Quality indicators for each layer type
        quality_indicators = {
            'surface': ['specifically', 'concretely', 'achieved', 'accomplished', 'created', 'built'],
            'emotional': ['felt', 'experienced', 'emotions', 'feeling', 'joy', 'challenge', 'growth'],
            'contextual': ['when', 'where', 'because', 'circumstances', 'environment', 'situation'],
            'wisdom': ['learned', 'realized', 'insight', 'principle', 'truth', 'lesson', 'understanding'],
            'cultural': ['values', 'tradition', 'culture', 'community', 'heritage', 'beliefs', 'customs']
        }
        
        # Count quality indicators
        content_lower = content.lower()
        indicator_count = sum(1 for indicator in quality_indicators.get(layer_type, []) 
                            if indicator in content_lower)
        indicator_score = min(indicator_count / 3, 1.0)  # Normalize to 0-1
        
        # Depth analysis - look for complex sentences and detailed descriptions
        sentence_count = len([s for s in content.split('.') if s.strip()])
        depth_score = min(sentence_count / 3, 1.0)  # Normalize to 0-1
        
        # Combine scores: 40% length, 30% indicators, 30% depth
        final_score = (length_score * 0.4 + indicator_score * 0.3 + depth_score * 0.3)
        
        return min(final_score, 1.0)
    
    def _calculate_revenue(self, quality_score: float, cultural_context: str, layers: Dict[str, str] = None) -> float:
        """Calculate dynamic revenue potential based on content value and market demand"""
        base_rate = 50.0  # €50 base rate
        
        # Get cultural multiplier
        multiplier = self.cultural_multipliers.get(
            cultural_context, 
            self.cultural_multipliers['Default']
        )
        
        # Base revenue calculation
        revenue = base_rate * quality_score * multiplier
        
        # Enhanced revenue factors if layers are available
        if layers:
            # Wisdom layer value multiplier
            wisdom_content = layers.get('wisdom', '')
            if wisdom_content:
                wisdom_value = self._assess_wisdom_value(wisdom_content)
                revenue *= wisdom_value
            
            # Cultural rarity bonus
            cultural_content = layers.get('cultural', '')
            if cultural_content:
                cultural_rarity = self._assess_cultural_rarity(cultural_content)
                revenue *= cultural_rarity
            
            # Commercial applicability
            commercial_value = self._assess_commercial_value(layers)
            revenue *= commercial_value
        
        # Quality-based bonuses
        if quality_score >= 0.9:
            revenue *= 1.2  # 20% excellence bonus
        elif quality_score >= 0.8:
            revenue *= 1.1  # 10% high quality bonus
        elif quality_score >= 0.7:
            revenue *= 1.05  # 5% good quality bonus
        
        return round(revenue, 2)
    
    def _assess_wisdom_value(self, wisdom_content: str) -> float:
        """Assess the commercial value of wisdom content"""
        high_value_indicators = [
            'universal', 'timeless', 'principle', 'fundamental', 'essential',
            'breakthrough', 'innovation', 'discovery', 'insight', 'truth'
        ]
        
        content_lower = wisdom_content.lower()
        value_count = sum(1 for indicator in high_value_indicators 
                         if indicator in content_lower)
        
        # Return multiplier based on wisdom value (1.0 to 1.5)
        return 1.0 + (value_count * 0.1)
    
    def _assess_cultural_rarity(self, cultural_content: str) -> float:
        """Assess the rarity and preservation value of cultural content"""
        rare_cultural_indicators = [
            'traditional', 'ancestral', 'indigenous', 'heritage', 'ancient',
            'ritual', 'ceremony', 'custom', 'folklore', 'oral tradition'
        ]
        
        content_lower = cultural_content.lower()
        rarity_count = sum(1 for indicator in rare_cultural_indicators 
                          if indicator in content_lower)
        
        # Return multiplier based on cultural rarity (1.0 to 1.4)
        return 1.0 + (rarity_count * 0.08)
    
    def _assess_commercial_value(self, layers: Dict[str, str]) -> float:
        """Assess overall commercial applicability for AI training"""
        commercial_indicators = [
            'training', 'learning', 'teaching', 'education', 'development',
            'problem-solving', 'decision-making', 'leadership', 'innovation'
        ]
        
        all_content = ' '.join(layers.values()).lower()
        commercial_count = sum(1 for indicator in commercial_indicators 
                              if indicator in all_content)
        
        # Return multiplier based on commercial value (1.0 to 1.3)
        return 1.0 + (commercial_count * 0.05)
    
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
            # Use QWEN embeddings
            response = self.QWEN_client.embeddings.create(
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
    
    # Initialize without QWEN (fallback mode)
    analyzer = LayerAnalyzer(QWEN_client=None)
    
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