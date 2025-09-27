# five_prompt_toolkit.py
"""
5-Prompt Perception Toolkit™ v2.0
Proper implementation with Deep Vibe Distillation
Created by: Alton Lee | YSense AI | 慧觉
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

class FivePromptToolkit:
    """
    Implementation of the 5-Prompt Perception Toolkit™ 
    with proper Deep Vibe Distillation process
    """
    
    def __init__(self):
        # The 5 Core Prompts - EXACTLY as documented
        self.prompts = {
            'narrative': {
                'prompt': "What is the unspoken story of this place or thing? As well as, what is the well-known story of it too from my perspective?",
                'layer_name': 'Narrative Layer',
                'purpose': 'Capture both hidden/personal narrative and broader context',
                'ai_value': 'Contextual understanding, cultural background'
            },
            'somatic': {
                'prompt': "What does being here make my emotion and body feel? What in my mind as present here?",
                'layer_name': 'Somatic Layer', 
                'purpose': 'Ground experience in physical and emotional reality',
                'ai_value': 'Emotional grounding, human sensation modeling'
            },
            'attention': {
                'prompt': "What is one tiny detail here that most people would miss? What do I miss out in this places and things?",
                'layer_name': 'Attention Layer',
                'purpose': 'Capture unique perceptual details and acknowledge limitations',
                'ai_value': 'Detail recognition, perspective diversity'
            },
            'synesthetic': {
                'prompt': "What are three non-visual words to describe the 'vibe' here? Let it flow through me and feels.",
                'layer_name': 'Synesthetic Layer',
                'purpose': 'Access cross-sensory perception beyond visual dominance',
                'ai_value': 'Synesthetic understanding, qualitative assessment'
            },
            'temporal_auditory': {
                'prompt': "If this moment had a sound, what would it be?",
                'layer_name': 'Temporal-Auditory Layer',
                'purpose': 'Capture temporal and auditory essence of the experience',
                'ai_value': 'Temporal context, auditory association patterns'
            }
        }
        
        # The Sacred Distillation Prompt - Y's Role
        self.distillation_prompt = "If you had to describe the single, core 'echo' that this entire experience leaves in your heart, what is that feeling?"
        
        # Cultural multipliers for Malaysian context
        self.cultural_multipliers = {
            'Malaysian': 1.5,
            'Malaysian Chinese': 1.6,
            'Hokkien': 1.7,
            'Southeast Asian': 1.3,
            'Kampung': 1.4,
            'Indigenous': 1.4,
            'Global South': 1.15,
            'Default': 1.0
        }
        
        # Archive of Alton's wisdom drops (from documentation)
        self.wisdom_archive = self._load_archive()
    
    def _load_archive(self) -> List[Dict]:
        """Load the documented wisdom drops from Alton's archive"""
        return [
            {
                'id': 'DROP_001',
                'title': 'KELANTAN BEACH TRIP (2013)',
                'vibe_words': ['Joy', 'Wonder', 'Awe'],
                'personal_connection': 'Beautiful shock of seeing a new world underwater',
                'cultural_context': 'First snorkeling experience, Kelantanese friendship, cross-cultural immersion',
                'essence': 'Discovery of hidden worlds through cultural bridge-building'
            },
            {
                'id': 'DROP_002',
                'title': 'BECOMING A CREATOR',
                'vibe_words': ['Possibility', 'Awakening', 'Energy'],
                'personal_connection': 'This vision begins to take practical, tangible shape',
                'cultural_context': 'Creator35LWB timeline realization, age 33 awakening',
                'essence': 'Creative identity emergence and timeline consciousness'
            },
            {
                'id': 'DROP_003',
                'title': 'THE ECHO IN THE SILENCE',
                'vibe_words': ['Stillness', 'Enlighten', 'Connection'],
                'personal_connection': 'Sound so clear and pure, carries deep sense of Zen',
                'cultural_context': 'YSense logo water droplet, mission contemplation, inner peace',
                'essence': 'Zen awareness connecting inner stillness to outer mission'
            },
            {
                'id': 'DROP_004',
                'title': 'LOVE IN A SMALL VILLAGE',
                'vibe_words': ['Eternity', 'Presence', 'Love'],
                'personal_connection': 'True meaning of love reflected in them - growing old together',
                'cultural_context': 'Elderly couple in Negeri Sembilan, love evolution understanding',
                'essence': 'Witnessing eternal love teaching present love'
            },
            {
                'id': 'DROP_005',
                'title': 'A DRAGON IN THE DISTRICT',
                'vibe_words': ['Struggle', 'Resilience', 'Enjoyment'],
                'personal_connection': 'Embrace what I love without overthinking - just enjoy the game',
                'cultural_context': 'Basketball journey, mentor rejection, leadership through adversity',
                'essence': 'Finding joy beyond struggle through resilient love'
            },
            {
                'id': 'DROP_006',
                'title': 'THE YSENSE MANIFESTO',
                'vibe_words': ['A drop 💧'],  # Special case
                'personal_connection': 'Every story shared builds bridges between cultures',
                'cultural_context': 'Community invitation, mission launch, co-creation beginning',
                'essence': 'Single drop creating infinite ripples of cultural bridge-building'
            },
            {
                'id': 'DROP_007',
                'title': 'REMEMBERING THE SOURCE (Merdeka Day)',
                'vibe_words': ['Roots', 'Reverence', 'Belonging'],
                'personal_connection': 'Cultural inheritance lives on through us - and now through our children',
                'cultural_context': 'Hokkien traditions, 弟子规 teaching, generational wisdom transmission',
                'essence': 'Cultural heritage as living bridge between past and future'
            }
        ]
    
    def create_wisdom_drop(self, 
                          author: str,
                          experience_title: str,
                          layer_responses: Dict[str, str],
                          cultural_context: str = None) -> Dict:
        """
        Create a wisdom drop from the 5 layer responses
        NOTE: This does NOT include vibe words - those come later!
        """
        
        # Validate all 5 layers are present
        required_layers = ['narrative', 'somatic', 'attention', 'synesthetic', 'temporal_auditory']
        for layer in required_layers:
            if layer not in layer_responses or not layer_responses[layer]:
                raise ValueError(f"Missing required layer: {layer}")
        
        # Generate unique ID
        wisdom_id = self._generate_id(author, experience_title)
        
        # Create the wisdom drop structure
        wisdom_drop = {
            'id': wisdom_id,
            'timestamp': datetime.now().isoformat(),
            'author': author,
            'title': experience_title,
            'cultural_context': cultural_context or 'Global',
            'status': 'awaiting_distillation',  # Key status!
            
            # The 5 Layers
            'layers': {
                'narrative': layer_responses['narrative'],
                'somatic': layer_responses['somatic'],
                'attention': layer_responses['attention'],
                'synesthetic': layer_responses['synesthetic'],
                'temporal_auditory': layer_responses['temporal_auditory']
            },
            
            # Metadata
            'quality_score': self._calculate_initial_quality(layer_responses),
            'completeness': self._check_completeness(layer_responses),
            'attribution_hash': self._generate_attribution_hash(author, experience_title, layer_responses),
            'z_protocol_version': 'v2.0',
            
            # Distillation fields (empty until completed)
            'vibe_words': None,
            'personal_connection': None,
            'essence': None,
            'distillation_completed': False
        }
        
        return wisdom_drop
    
    def add_deep_vibe_distillation(self,
                                  wisdom_drop: Dict,
                                  vibe_words: List[str],
                                  personal_connection: str,
                                  essence_description: str = None) -> Dict:
        """
        Complete the Deep Vibe Distillation process
        This is Y's role - extracting the three sacred words
        """
        
        if len(vibe_words) != 3 and vibe_words != ['A drop 💧']:  # Special case
            raise ValueError("Deep Vibe Distillation requires exactly 3 words (or the special 'A drop' case)")
        
        # Update the wisdom drop with distillation
        wisdom_drop['vibe_words'] = vibe_words
        wisdom_drop['personal_connection'] = personal_connection
        wisdom_drop['essence'] = essence_description or self._synthesize_essence(vibe_words, personal_connection)
        wisdom_drop['distillation_completed'] = True
        wisdom_drop['distillation_timestamp'] = datetime.now().isoformat()
        wisdom_drop['status'] = 'complete'
        
        # Recalculate quality and revenue with distillation bonus
        wisdom_drop['quality_score'] = self._calculate_final_quality(wisdom_drop)
        wisdom_drop['revenue_potential'] = self._calculate_revenue(
            wisdom_drop['quality_score'],
            wisdom_drop['cultural_context']
        )
        
        return wisdom_drop
    
    def _calculate_initial_quality(self, layers: Dict[str, str]) -> float:
        """Calculate quality score for layers only (pre-distillation)"""
        score = 0.0
        weights = {
            'narrative': 0.15,
            'somatic': 0.20,
            'attention': 0.15,
            'synesthetic': 0.20,
            'temporal_auditory': 0.10
        }
        
        for layer, weight in weights.items():
            if layer in layers and layers[layer]:
                content = layers[layer]
                # Score based on richness
                if len(content) > 100:
                    score += weight
                elif len(content) > 50:
                    score += weight * 0.7
                elif len(content) > 20:
                    score += weight * 0.5
        
        return min(score, 0.80)  # Cap at 0.80 without distillation
    
    def _calculate_final_quality(self, wisdom_drop: Dict) -> float:
        """Calculate final quality with distillation bonus"""
        base_quality = self._calculate_initial_quality(wisdom_drop['layers'])
        
        if wisdom_drop.get('distillation_completed'):
            # Distillation adds 0.2 to quality (huge bonus!)
            distillation_bonus = 0.2
            
            # Check vibe word quality
            if wisdom_drop.get('vibe_words'):
                if len(wisdom_drop['vibe_words']) == 3:
                    distillation_bonus += 0.05
                if wisdom_drop.get('personal_connection'):
                    distillation_bonus += 0.05
                if wisdom_drop.get('essence'):
                    distillation_bonus += 0.05
            
            return min(base_quality + distillation_bonus, 1.0)
        
        return base_quality
    
    def _calculate_revenue(self, quality_score: float, cultural_context: str) -> float:
        """Calculate revenue with cultural multipliers"""
        base_rate = 50.0  # €50 base
        
        # Get cultural multiplier
        multiplier = self.cultural_multipliers.get(
            cultural_context,
            self.cultural_multipliers['Default']
        )
        
        # Special bonus for complete distillation
        if quality_score >= 0.95:
            multiplier *= 1.2  # Excellence bonus
        
        revenue = base_rate * quality_score * multiplier
        
        return round(revenue, 2)
    
    def _check_completeness(self, layers: Dict[str, str]) -> Dict:
        """Check which layers are complete"""
        completeness = {}
        for layer in ['narrative', 'somatic', 'attention', 'synesthetic', 'temporal_auditory']:
            if layer in layers and layers[layer] and len(layers[layer]) > 20:
                completeness[layer] = True
            else:
                completeness[layer] = False
        return completeness
    
    def _generate_id(self, author: str, title: str) -> str:
        """Generate unique wisdom drop ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_string = f"{author}_{title}_{timestamp}"
        hash_suffix = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        return f"DROP_{hash_suffix.upper()}"
    
    def _generate_attribution_hash(self, author: str, title: str, layers: Dict) -> str:
        """Generate cryptographic attribution hash"""
        attribution_data = {
            'author': author,
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'layers_hash': hashlib.sha256(
                json.dumps(layers, sort_keys=True).encode()
            ).hexdigest()[:16]
        }
        
        attribution_string = json.dumps(attribution_data, sort_keys=True)
        return hashlib.sha256(attribution_string.encode()).hexdigest()
    
    def _synthesize_essence(self, vibe_words: List[str], personal_connection: str) -> str:
        """Auto-generate essence from vibe words and connection"""
        return f"{' + '.join(vibe_words)} through {personal_connection[:50]}"
    
    def extract_layers_from_text(self, text: str) -> Dict[str, str]:
        """
        Helper to extract layer responses from free-form text
        Uses pattern matching to identify which prompt is being answered
        """
        layers = {}
        
        # Pattern matching for each layer
        patterns = {
            'narrative': r'(story|narrative|known|unspoken)',
            'somatic': r'(feel|body|emotion|present)',
            'attention': r'(detail|miss|tiny|notice)',
            'synesthetic': r'(vibe|non-visual|describe)',
            'temporal_auditory': r'(sound|hear|audio)'
        }
        
        # Split text into sentences
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for layer, pattern in patterns.items():
                if re.search(pattern, sentence_lower) and layer not in layers:
                    layers[layer] = sentence.strip()
        
        return layers
    
    def validate_vibe_words(self, words: List[str]) -> Tuple[bool, str]:
        """
        Validate that vibe words follow the methodology
        Returns (is_valid, message)
        """
        # Special case for "A drop"
        if words == ['A drop 💧'] or words == ['A drop']:
            return True, "Special singular vibe accepted"
        
        # Must be exactly 3 words
        if len(words) != 3:
            return False, "Deep Vibe Distillation requires exactly 3 words"
        
        # Each word should be meaningful (not empty, not too long)
        for word in words:
            if not word or len(word) < 2:
                return False, "Each vibe word must be meaningful"
            if len(word) > 20:
                return False, "Vibe words should be concise (under 20 characters)"
        
        return True, "Valid vibe words"
    
    def get_example_drops(self) -> List[Dict]:
        """Return Alton's documented example drops for reference"""
        return self.wisdom_archive
    
    def generate_prompt_guide(self) -> str:
        """Generate a guide for users on how to respond to prompts"""
        guide = "🎯 5-PROMPT PERCEPTION TOOLKIT™ GUIDE\n"
        guide += "="*50 + "\n\n"
        
        for key, prompt_data in self.prompts.items():
            guide += f"📌 {prompt_data['layer_name'].upper()}\n"
            guide += f"Prompt: {prompt_data['prompt']}\n"
            guide += f"Purpose: {prompt_data['purpose']}\n"
            guide += f"AI Value: {prompt_data['ai_value']}\n"
            guide += "-"*40 + "\n\n"
        
        guide += "✨ DEEP VIBE DISTILLATION (After all 5 layers)\n"
        guide += f"Final Question: {self.distillation_prompt}\n"
        guide += "Then extract 3 words that capture the essence\n"
        
        return guide


# Integration helper for existing platform
class EnhancedWisdomProcessor:
    """
    Integrates 5-Prompt Toolkit with existing platform
    """
    
    def __init__(self, database):
        self.toolkit = FivePromptToolkit()
        self.db = database
    
    def process_wisdom_submission(self,
                                 author: str,
                                 title: str,
                                 responses: Dict[str, str],
                                 cultural_context: str) -> Dict:
        """
        Process initial 5-layer submission
        """
        # Create wisdom drop (without vibe words)
        wisdom_drop = self.toolkit.create_wisdom_drop(
            author=author,
            experience_title=title,
            layer_responses=responses,
            cultural_context=cultural_context
        )
        
        # Save to database
        self.db.save_wisdom_drop(wisdom_drop)
        
        return wisdom_drop
    
    def complete_distillation(self,
                             wisdom_id: str,
                             vibe_words: List[str],
                             personal_connection: str,
                             essence: str = None) -> Dict:
        """
        Complete the Deep Vibe Distillation
        """
        # Load wisdom drop
        all_drops = self.db.get_all_wisdom_drops()
        wisdom_drop = next((d for d in all_drops if d['id'] == wisdom_id), None)
        
        if not wisdom_drop:
            raise ValueError(f"Wisdom drop {wisdom_id} not found")
        
        # Validate vibe words
        is_valid, message = self.toolkit.validate_vibe_words(vibe_words)
        if not is_valid:
            raise ValueError(f"Invalid vibe words: {message}")
        
        # Complete distillation
        completed_drop = self.toolkit.add_deep_vibe_distillation(
            wisdom_drop=wisdom_drop,
            vibe_words=vibe_words,
            personal_connection=personal_connection,
            essence_description=essence
        )
        
        # Update in database
        self.db.save_wisdom_drop(completed_drop)
        
        return completed_drop
    
    def get_pending_distillations(self) -> List[Dict]:
        """Get all wisdom drops awaiting distillation"""
        all_drops = self.db.get_all_wisdom_drops()
        return [d for d in all_drops if not d.get('distillation_completed', False)]


# Example usage
if __name__ == "__main__":
    toolkit = FivePromptToolkit()
    
    # Show the prompts
    print(toolkit.generate_prompt_guide())
    
    # Example: Create a wisdom drop
    responses = {
        'narrative': "The unspoken story here is about Malaysian innovation finding its voice. The well-known story is that we need Silicon Valley to succeed.",
        'somatic': "My body feels energized, heart racing with possibility. My mind is present with clarity about our mission.",
        'attention': "The tiny detail others miss: the way local wisdom can outperform global solutions. What I miss: sometimes the exhaustion behind the determination.",
        'synesthetic': "Three non-visual words: warmth, determination, rising",
        'temporal_auditory': "If this moment had a sound, it would be the steady rhythm of typing keys mixed with tropical rain"
    }
    
    # Create wisdom drop (Stage 1)
    wisdom = toolkit.create_wisdom_drop(
        author="Alton Lee Wei Bin",
        experience_title="Building YSense from Teluk Intan",
        layer_responses=responses,
        cultural_context="Malaysian"
    )
    
    print(f"\n✅ Wisdom Drop Created: {wisdom['id']}")
    print(f"Quality (pre-distillation): {wisdom['quality_score']:.2f}")
    print(f"Status: {wisdom['status']}")
    
    # Later: Add Deep Vibe Distillation (Stage 2)
    wisdom = toolkit.add_deep_vibe_distillation(
        wisdom_drop=wisdom,
        vibe_words=["Determination", "Innovation", "Heritage"],
        personal_connection="Proving that Malaysian innovation doesn't need external validation",
        essence_description="Local wisdom creating global impact through authentic innovation"
    )
    
    print(f"\n✨ Distillation Complete!")
    print(f"Vibe Words: {', '.join(wisdom['vibe_words'])}")
    print(f"Final Quality: {wisdom['quality_score']:.2f}")
    print(f"Revenue Potential: €{wisdom['revenue_potential']:.2f}")