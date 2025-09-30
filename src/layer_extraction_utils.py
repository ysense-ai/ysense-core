# layer_extraction_utils.py
"""
Layer extraction utilities for YSense
Separated to avoid circular imports
"""

import re

def extract_layers_from_story(story_text: str) -> dict:
    """
    Intelligently extract 5-layer responses from natural storytelling
    This works behind the scenes
    """
    layers = {
        'narrative': '',
        'somatic': '',
        'attention': '',
        'synesthetic': '',
        'temporal_auditory': ''
    }
    
    # Split into paragraphs
    paragraphs = story_text.split('\n\n')
    
    # Smart extraction patterns
    patterns = {
        'narrative': [
            r'(story|happened|occurred|began|started|unfolded)',
            r'(people think|known as|famous for|reputation)',
            r'(truth is|actually|really|but)'
        ],
        'somatic': [
            r'(felt|feeling|emotion|body|physical)',
            r'(heart|stomach|chest|hands|breath)',
            r'(excited|nervous|calm|tense|relaxed)'
        ],
        'attention': [
            r'(noticed|saw|observed|detail|small)',
            r'(missed|overlooked|didn\'t see|ignore)',
            r'(tiny|subtle|hidden|quiet)'
        ],
        'synesthetic': [
            r'(vibe|atmosphere|feeling|sense|mood)',
            r'(texture|weight|temperature|thickness)',
            r'(warm|cool|heavy|light|smooth|rough)'
        ],
        'temporal_auditory': [
            r'(sound|hear|listen|noise|quiet)',
            r'(rhythm|beat|melody|hum|buzz)',
            r'(if.*sound|sounded like|reminds me of)'
        ]
    }
    
    # Extract content for each layer
    for para in paragraphs:
        para_lower = para.lower()
        
        # Check each layer's patterns
        for layer, layer_patterns in patterns.items():
            if not layers[layer]:  # If layer not yet filled
                for pattern_group in layer_patterns:
                    if re.search(pattern_group, para_lower):
                        # Extract relevant sentences
                        sentences = para.split('.')
                        for sentence in sentences:
                            if re.search(pattern_group, sentence.lower()):
                                if layers[layer]:
                                    layers[layer] += ' ' + sentence.strip()
                                else:
                                    layers[layer] = sentence.strip()
                        break
    
    # Fill any empty layers with contextual extraction
    full_text_lower = story_text.lower()
    
    if not layers['narrative']:
        # Extract opening or context-setting content
        layers['narrative'] = paragraphs[0][:200] if paragraphs else story_text[:200]
    
    if not layers['somatic']:
        # Look for any emotional or physical description
        for para in paragraphs:
            if any(word in para.lower() for word in ['i', 'my', 'me']):
                layers['somatic'] = para[:150]
                break
    
    if not layers['attention']:
        # Find specific details mentioned
        detail_sentences = [s for s in story_text.split('.') 
                          if any(word in s.lower() for word in ['see', 'saw', 'notice', 'look'])]
        if detail_sentences:
            layers['attention'] = detail_sentences[0].strip()
    
    if not layers['synesthetic']:
        # Extract descriptive language
        desc_words = re.findall(r'\b(warm|cold|soft|hard|smooth|rough|heavy|light|thick|thin)\b', 
                               full_text_lower)
        if desc_words:
            layers['synesthetic'] = f"The experience felt {', '.join(desc_words[:3])}"
    
    if not layers['temporal_auditory']:
        # Create from rhythm of narrative
        if 'quiet' in full_text_lower:
            layers['temporal_auditory'] = "A gentle quietness"
        elif 'loud' in full_text_lower or 'noise' in full_text_lower:
            layers['temporal_auditory'] = "A crescendo of activity"
        else:
            layers['temporal_auditory'] = "The steady rhythm of unfolding moments"
    
    return layers