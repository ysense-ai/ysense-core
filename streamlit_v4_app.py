# 🌟 YSense Platform v4.0 - Independent AI-Powered Interface

import streamlit as st
import requests
import json
from datetime import datetime
import time
import random

# Page Configuration
st.set_page_config(
    page_title="YSense™ v4.0 | 慧觉™ - AI-Powered Wisdom Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8004/api/v3"
API_V4_BASE_URL = "http://localhost:8004/api/v4"

# Header Image (Subtle and Comfortable)
def add_header_image():
    """Add subtle header image representing human-AI collaboration"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDgwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI4MDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjNjMzM0E2Ii8+CjxjaXJjbGUgY3g9IjQwMCIgY3k9IjEwMCIgcj0iNDAiIGZpbGw9IiNGRkZGRkYiIG9wYWNpdHk9IjAuOCIvPgo8Y2lyY2xlIGN4PSIzNjAiIGN5PSI4MCIgcj0iMjAiIGZpbGw9IiM0MEEzRkYiIG9wYWNpdHk9IjAuNiIvPgo8Y2lyY2xlIGN4PSI0NDAiIGN5PSI4MCIgcj0iMjAiIGZpbGw9IiM0MEEzRkYiIG9wYWNpdHk9IjAuNiIvPgo8bGluZSB4MT0iMzYwIiB5MT0iODAiIHgyPSI0NDAiIHkyPSI4MCIgc3Ryb2tlPSIjRkZGRkZGIiBzdHJva2Utd2lkdGg9IjIiIG9wYWNpdHk9IjAuNyIvPgo8dGV4dCB4PSI0MDAiIHk9IjE0MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSIjRkZGRkZGIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBvcGFjaXR5PSIwLjgiPkh1bWFuLUFJIENvbGxhYm9yYXRpb248L3RleHQ+Cjwvc3ZnPgo=" 
             style="width: 100%; max-width: 800px; height: auto; border-radius: 10px; opacity: 0.9;">
    </div>
    """, unsafe_allow_html=True)

# Custom CSS for Professional Look
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .ai-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'crypto_key' not in st.session_state:
        st.session_state.crypto_key = None
    if 'z_protocol_consent_key' not in st.session_state:
        st.session_state.z_protocol_consent_key = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "story_input"
    if 'ai_analysis' not in st.session_state:
        st.session_state.ai_analysis = {}
    if 'layer_review' not in st.session_state:
        st.session_state.layer_review = {}

# API Helper Functions
def api_call(method, endpoint, data=None, headers=None):
    """Make API call to backend"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server. Please ensure the backend is running.")
        return None

def api_v4_call(method, endpoint, data=None, headers=None):
    """Make API call to v4.0 backend"""
    try:
        url = f"{API_V4_BASE_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            st.error(f"v4.0 API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to v4.0 API server. Please ensure the backend is running.")
        return None

# AI Recommendation Functions
def generate_ai_vibe_recommendations(story: str, layers: dict) -> list:
    """Generate AI vibe word recommendations based on story analysis"""
    
    # Based on SAMPLE SHOWCASE patterns, create intelligent recommendations
    vibe_patterns = {
        "joy": ["Joy", "Wonder", "Awe", "Happiness", "Delight"],
        "love": ["Love", "Eternity", "Presence", "Connection", "Belonging"],
        "growth": ["Possibility", "Awakening", "Energy", "Transformation", "Discovery"],
        "peace": ["Stillness", "Enlightenment", "Connection", "Calm", "Serenity"],
        "struggle": ["Struggle", "Resilience", "Enjoyment", "Perseverance", "Strength"],
        "heritage": ["Roots", "Reverence", "Belonging", "Tradition", "Wisdom"],
        "music": ["Melodic", "Rhythmic", "Harmonic", "Sonic", "Musical"],
        "family": ["Warmth", "Togetherness", "Nurturing", "Bonding", "Care"],
        "nature": ["Natural", "Organic", "Pure", "Fresh", "Vital"],
        "creative": ["Creative", "Inspiring", "Imaginative", "Artistic", "Expressive"]
    }
    
    # Analyze story content for themes
    story_lower = story.lower()
    themes = []
    
    if any(word in story_lower for word in ["happy", "joy", "smile", "laugh", "delight"]):
        themes.append("joy")
    if any(word in story_lower for word in ["love", "heart", "care", "affection", "family"]):
        themes.append("love")
    if any(word in story_lower for word in ["grow", "learn", "discover", "new", "change"]):
        themes.append("growth")
    if any(word in story_lower for word in ["calm", "peace", "quiet", "still", "zen"]):
        themes.append("peace")
    if any(word in story_lower for word in ["sing", "music", "song", "melody", "sound"]):
        themes.append("music")
    if any(word in story_lower for word in ["daughter", "child", "family", "parent"]):
        themes.append("family")
    if any(word in story_lower for word in ["create", "art", "imagine", "design", "make"]):
        themes.append("creative")
    
    # Default themes if none detected
    if not themes:
        themes = ["joy", "love", "growth"]
    
    # Generate recommendations
    recommendations = []
    for theme in themes[:3]:  # Take first 3 themes
        if theme in vibe_patterns:
            recommendations.append(random.choice(vibe_patterns[theme]))
    
    # Fill remaining slots if needed
    while len(recommendations) < 3:
        remaining_themes = [t for t in vibe_patterns.keys() if t not in themes]
        if remaining_themes:
            theme = random.choice(remaining_themes)
            recommendations.append(random.choice(vibe_patterns[theme]))
        else:
            recommendations.append("Meaningful")
    
    return recommendations[:3]

# Authentication Functions
def show_login():
    """Show login interface"""
    st.markdown("## 🔐 Login to YSense v4.0")
    
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        crypto_key = st.text_input("Crypto Key", type="password", help="Enter your crypto key")
        
        submit_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
        
        if submit_button:
            if not username_or_email or not crypto_key:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Logging in..."):
                    result = api_call("POST", "auth/login", {
                        "username_or_email": username_or_email,
                        "crypto_key": crypto_key
                    })
                    
                    if result:
                        st.session_state.authenticated = True
                        st.session_state.username = result.get("username")
                        st.session_state.crypto_key = crypto_key
                        st.session_state.z_protocol_consent_key = result.get("z_protocol_consent_key")
                        st.session_state.access_token = result.get("access_token")
                        st.success("✅ Login successful!")
                        st.rerun()

def show_registration():
    """Show registration interface with complete consent and terms"""
    st.markdown("## 📝 Register for YSense v4.0")
    st.info("✨ **Complete registration with consent and terms of service**")
    
    with st.form("registration_form"):
        st.markdown("### 👤 Personal Information")
        username = st.text_input("Username", help="Choose a unique username")
        email = st.text_input("Email", help="Your email address")
        age = st.number_input("Age", min_value=13, max_value=120, value=25, help="Must be 13 or older")
        
        st.markdown("### 📋 Consent Agreement")
        st.markdown("**Please read and accept the following agreements:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Data & Privacy:**")
            consent_data = st.checkbox("✅ Data Collection Consent", value=True, 
                                     help="I consent to the collection and processing of my personal data")
            consent_commercial = st.checkbox("✅ Commercial Use Consent", value=True,
                                           help="I consent to my wisdom being used for commercial purposes")
            consent_ai = st.checkbox("✅ AI Training Consent", value=True,
                                   help="I consent to my wisdom being used for AI training")
        
        with col2:
            st.markdown("**Revenue & Attribution:**")
            consent_revenue = st.checkbox("✅ Revenue Sharing Consent", value=True,
                                        help="I consent to revenue sharing from my wisdom")
            consent_attribution = st.checkbox("✅ Attribution Consent", value=True,
                                            help="I consent to permanent attribution of my wisdom")
            consent_terms = st.checkbox("✅ Terms of Service", value=True,
                                      help="I agree to the Terms of Service")
        
        st.markdown("### 🔐 Z Protocol v2.0 Compliance")
        st.info("**Z Protocol v2.0:** Our advanced compliance framework ensures ethical AI training and proper attribution.")
        
        z_protocol_consent = st.checkbox("✅ Z Protocol v2.0 Compliance", value=True,
                                       help="I agree to comply with Z Protocol v2.0 standards")
        
        st.markdown("### 📄 Important Information")
        st.markdown("""
        **🔑 Crypto Key Authentication:** You will receive a unique crypto key for secure login (no passwords!)
        
        **🔐 Z Protocol Consent Key:** You will receive a consent key for verification and management
        
        **💰 Revenue Sharing:** 30-50% revenue share based on your tier and wisdom quality
        
        **🛡️ Your Rights:** Right to deletion (except published wisdom), GDPR/PDPA compliant
        """)
        
        submit_button = st.form_submit_button("🌟 Register for YSense v4.0", type="primary", use_container_width=True)
        
        if submit_button:
            if not all([username, email, age]):
                st.error("⚠️ Please fill in all personal information fields")
            elif not all([consent_data, consent_commercial, consent_ai, consent_revenue, consent_attribution, consent_terms, z_protocol_consent]):
                st.error("⚠️ Please accept all consent agreements and terms")
            else:
                with st.spinner("🌟 Creating your YSense v4.0 account..."):
                    result = api_call("POST", "auth/register", {
                        "username": username,
                        "email": email,
                        "age": age,
                        "consent_data_collection": consent_data,
                        "consent_commercial_use": consent_commercial,
                        "consent_ai_training": consent_ai,
                        "consent_revenue_sharing": consent_revenue,
                        "consent_attribution": consent_attribution,
                        "consent_terms": consent_terms
                    })
                    
                    if result:
                        st.success("🎉 **Registration successful!**")
                        st.markdown("### 🔑 Your Authentication Keys")
                        st.info(f"**Crypto Key:** `{result.get('crypto_key')}`")
                        st.info(f"**Z Protocol Consent Key:** `{result.get('z_protocol_consent_key')}`")
                        st.warning("⚠️ **IMPORTANT:** Please save these keys securely! You'll need them to access your account.")
                        
                        st.markdown("### 🚀 Next Steps")
                        st.markdown("1. **Save your keys** in a secure location")
                        st.markdown("2. **Login** using your crypto key")
                        st.markdown("3. **Start creating** AI-powered wisdom drops!")
                        
                        st.balloons()

# v4.0 AI-Powered Workflow Functions
def show_story_input():
    """Show story input interface"""
    st.markdown("## 📖 Tell Your Story")
    st.info("✨ **Simply tell your story naturally - our AI will analyze it with 7 intelligent agents!**")
    
    with st.form("story_form"):
        story = st.text_area(
            "Your Story",
            placeholder="Tell us about your experience, memory, or moment you'd like to share...",
            height=200,
            help="Share your story in your own words. The AI will analyze it to extract the Five-Layer Perception."
        )
        
        cultural_context = st.selectbox(
            "Cultural Context",
            ["Malaysian", "Southeast Asian", "Global", "Other"],
            help="This helps our AI understand cultural nuances"
        )
        
        language = st.selectbox(
            "Language",
            ["en", "ms", "zh", "ta", "hi"],
            help="Primary language of your story"
        )
        
        submit_button = st.form_submit_button("🤖 Analyze with AI", type="primary", use_container_width=True)
        
        if submit_button:
            if len(story.strip()) < 50:
                st.error("⚠️ Please provide a more detailed story (at least 50 characters)")
            else:
                with st.spinner("🤖 AI is analyzing your story..."):
                    headers = {"Authorization": f"Bearer {st.session_state.get('access_token', '')}"}
                    result = api_v4_call("POST", "wisdom/analyze-story", {
                        "story": story,
                        "cultural_context": cultural_context,
                        "language": language
                    }, headers)
                    
                    if result:
                        st.session_state.ai_analysis = result
                        st.session_state.current_step = "layer_review"
                        st.success("✅ AI analysis complete!")
                        st.rerun()

def show_layer_review():
    """Show layer review interface"""
    st.markdown("## 📋 Review AI-Extracted Layers")
    st.info("✨ **Review and edit the layers extracted by our AI. Your input makes them perfect!**")
    
    analysis = st.session_state.get("ai_analysis", {})
    layers = analysis.get("layers", {})
    
    if not layers:
        st.error("No layers found. Please go back and analyze your story.")
        return
    
    with st.form("review_form"):
        st.markdown("### 🤖 AI-Extracted Layers (Review & Edit)")
        
        # Display each layer for review
        layer_narrative = st.text_area(
            "1️⃣ **Narrative Layer**",
            value=layers.get("narrative", ""),
            height=100,
            help="The story and narrative elements"
        )
        
        layer_somatic = st.text_area(
            "2️⃣ **Somatic Layer**",
            value=layers.get("somatic", ""),
            height=100,
            help="Physical and emotional sensations"
        )
        
        layer_attention = st.text_area(
            "3️⃣ **Attention Layer**",
            value=layers.get("attention", ""),
            height=100,
            help="Key details and observations"
        )
        
        layer_synesthetic = st.text_area(
            "4️⃣ **Synesthetic Layer**",
            value=layers.get("synesthetic", ""),
            height=100,
            help="Sensory experiences and cross-modal perceptions"
        )
        
        layer_temporal_auditory = st.text_area(
            "5️⃣ **Temporal-Auditory Layer**",
            value=layers.get("temporal_auditory", ""),
            height=100,
            help="Rhythmic and temporal qualities"
        )
        
        # User edits
        user_edits = {}
        if layer_narrative != layers.get("narrative", ""):
            user_edits["narrative"] = layer_narrative
        if layer_somatic != layers.get("somatic", ""):
            user_edits["somatic"] = layer_somatic
        if layer_attention != layers.get("attention", ""):
            user_edits["attention"] = layer_attention
        if layer_synesthetic != layers.get("synesthetic", ""):
            user_edits["synesthetic"] = layer_synesthetic
        if layer_temporal_auditory != layers.get("temporal_auditory", ""):
            user_edits["temporal_auditory"] = layer_temporal_auditory
        
        notes = st.text_area(
            "Notes (Optional)",
            placeholder="Any additional thoughts or changes you made...",
            height=80
        )
        
        col1, col2 = st.columns(2)
        with col1:
            approve_button = st.form_submit_button("✅ Approve & Continue", type="primary", use_container_width=True)
        with col2:
            back_button = st.form_submit_button("⬅️ Back to Story", use_container_width=True)
        
        if approve_button:
            # Save review data
            st.session_state.layer_review = {
                "layers": {
                    "narrative": layer_narrative,
                    "somatic": layer_somatic,
                    "attention": layer_attention,
                    "synesthetic": layer_synesthetic,
                    "temporal_auditory": layer_temporal_auditory
                },
                "user_edits": user_edits,
                "approved": True,
                "notes": notes
            }
            st.session_state.current_step = "deep_vibe"
            st.success("✅ Layers approved!")
            st.rerun()
        
        if back_button:
            st.session_state.current_step = "story_input"
            st.rerun()

def show_deep_vibe_distillation():
    """Show Deep Vibe Distillation interface - AI recommends, Human decides"""
    st.markdown("## 🌊 Deep Vibe Distillation")
    st.info("✨ **Human Experience is Most Valuable** - AI recommends, you decide!")
    
    analysis = st.session_state.get("ai_analysis", {})
    review = st.session_state.get("layer_review", {})
    
    # Get final layers
    final_layers = review.get("layers", {}).copy()
    final_layers.update(review.get("user_edits", {}))
    
    # AI Vibe Word Recommendations (based on SAMPLE SHOWCASE patterns)
    st.markdown("### 🤖 AI Vibe Word Recommendations")
    st.info("💡 **AI suggests these vibe words based on your story analysis. You can use them or choose your own!**")
    
    # Generate AI recommendations based on story content
    story = analysis.get("story", "")
    ai_recommendations = generate_ai_vibe_recommendations(story, final_layers)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**AI Suggestion 1:**")
        st.info(f"💡 **{ai_recommendations[0]}**")
    with col2:
        st.markdown("**AI Suggestion 2:**")
        st.info(f"💡 **{ai_recommendations[1]}**")
    with col3:
        st.markdown("**AI Suggestion 3:**")
        st.info(f"💡 **{ai_recommendations[2]}**")
    
    st.markdown("---")
    
    with st.form("deep_vibe_form"):
        st.markdown("### 🎵 Your Vibe Words (Your Choice)")
        st.info("✨ **Choose YOUR 3 words that capture the essence of YOUR experience**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            vibe_word_1 = st.text_input(
                "Vibe Word 1", 
                placeholder="Your first word...",
                help="Choose a word that captures the essence of your experience"
            )
        with col2:
            vibe_word_2 = st.text_input(
                "Vibe Word 2", 
                placeholder="Your second word...",
                help="Choose a word that captures the essence of your experience"
            )
        with col3:
            vibe_word_3 = st.text_input(
                "Vibe Word 3", 
                placeholder="Your third word...",
                help="Choose a word that captures the essence of your experience"
            )
        
        st.markdown("### 💭 Why These Three Words?")
        st.info("🌟 **Share why you chose these specific words and what they mean to you**")
        
        vibe_words_explanation = st.text_area(
            "Your Vibe Words Explanation",
            placeholder="Explain why you chose these three words. What do they mean to you? How do they capture your experience? What feelings do they represent?",
            height=120,
            help="This is your personal interpretation - the most valuable part of your wisdom!"
        )
        
        st.markdown("### 💝 Personal Connection")
        personal_connection = st.text_area(
            "Personal Connection",
            placeholder="What does this experience mean to you personally? How does it connect to your life, values, or memories?",
            height=150,
            help="Share your personal connection to this experience"
        )
        
        st.markdown("### ✨ Essence Description (Optional)")
        essence = st.text_area(
            "Essence Description",
            placeholder="Describe the core essence or meaning of this experience...",
            height=100,
            help="Optional: Add a final essence description"
        )
        
        submit_button = st.form_submit_button("🌟 Complete Wisdom Drop", type="primary", use_container_width=True)
        
        if submit_button:
            vibe_words = [vibe_word_1, vibe_word_2, vibe_word_3]
            
            if not all(vibe_words):
                st.error("⚠️ Please provide all 3 vibe words")
            elif len(personal_connection.strip()) < 20:
                st.error("⚠️ Personal connection must contain at least 20 characters")
            elif len(vibe_words_explanation.strip()) < 20:
                st.error("⚠️ Please explain why you chose these three words (at least 20 characters)")
            else:
                # Create complete wisdom drop
                with st.spinner("🌟 Creating your wisdom drop..."):
                    try:
                        # Prepare data
                        story_data = {
                            "story": analysis.get("story", ""),
                            "cultural_context": analysis.get("cultural_context", "Global"),
                            "language": analysis.get("language", "en")
                        }
                        
                        review_data = {
                            "analysis_id": analysis.get("analysis_id"),
                            "layers": final_layers,
                            "user_edits": review.get("user_edits", {}),
                            "approved": True
                        }
                        
                        vibe_data = {
                            "vibe_words": vibe_words,
                            "vibe_words_explanation": vibe_words_explanation,
                            "personal_connection": personal_connection,
                            "essence_description": essence
                        }
                        
                        # Create wisdom drop
                        headers = {"Authorization": f"Bearer {st.session_state.get('access_token', '')}"}
                        result = api_v4_call("POST", "wisdom/create-wisdom-drop", {
                            "story_input": story_data,
                            "review": review_data,
                            "vibe_input": vibe_data
                        }, headers)
                        
                        if result:
                            st.success("🎉 **Wisdom Drop Created Successfully!**")
                            
                            # Display results
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.info(f"📊 **Quality Score:** {result.get('quality_score', 'N/A')}")
                            with col2:
                                st.info(f"💰 **Revenue Potential:** €{result.get('revenue_potential', 'N/A')}")
                            with col3:
                                st.info(f"🔐 **Z Protocol Score:** {result.get('z_protocol_score', 'N/A')}")
                            
                            # Z Protocol v2.0 Compliance Status
                            z_compliant = result.get('z_protocol_compliant', False)
                            if z_compliant:
                                st.success("✅ **Z Protocol v2.0 Compliant** - Your wisdom drop meets all compliance standards!")
                            else:
                                st.warning("⚠️ **Z Protocol v2.0 Issues** - Please review the recommendations below.")
                            
                            # Display violations and recommendations
                            violations = result.get('z_protocol_violations', [])
                            recommendations = result.get('z_protocol_recommendations', [])
                            
                            if violations:
                                st.error("**Z Protocol v2.0 Violations:**")
                                for violation in violations:
                                    st.error(f"• {violation}")
                            
                            if recommendations:
                                st.info("**Z Protocol v2.0 Recommendations:**")
                                for recommendation in recommendations:
                                    st.info(f"• {recommendation}")
                            
                            st.info(f"🆔 **Wisdom ID:** {result.get('wisdom_id', 'N/A')}")
                            st.info(f"🔐 **Attribution Hash:** {result.get('attribution_hash', 'N/A')[:20]}...")
                            
                            # Reset for new story
                            st.session_state.current_step = "story_input"
                            st.session_state.ai_analysis = {}
                            st.session_state.layer_review = {}
                            
                            st.balloons()
                        else:
                            st.error("❌ Failed to create wisdom drop. Please try again.")
                    
                    except Exception as e:
                        st.error(f"❌ Error creating wisdom drop: {str(e)}")

# Main Application
def main():
    """Main v4.0 application"""
    init_session_state()
    add_header_image()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 YSense™ v4.0 | 慧觉™</h1>
        <p style='font-size: 1.2em; margin: 0;'>
        AI-Powered Wisdom Platform<br>
        <em>Human Experience is Most Valuable - AI Recommends, Human Decides!</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 YSense v4.0 Features")
        st.markdown("""
        ✨ **AI-Powered Story Analysis**  
        🌊 **Enhanced Deep Vibe Distillation**  
        🔑 **Crypto Key Recovery**  
        💭 **Human Experience Respected**  
        📚 **SAMPLE SHOWCASE Integration**  
        """)
        
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.markdown(f"### Welcome, {st.session_state.username}!")
            
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.crypto_key = None
                st.session_state.z_protocol_consent_key = None
                st.session_state.current_step = "story_input"
                st.session_state.ai_analysis = {}
                st.session_state.layer_review = {}
                st.rerun()
        else:
            st.markdown("### Get Started")
            st.markdown("Register or login to start creating AI-powered wisdom drops!")
    
    # Main content
    if not st.session_state.authenticated:
        # Authentication required
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_registration()
    
    else:
        # Authenticated user - show v4.0 workflow
        st.markdown("""
        <div class="ai-highlight">
            <h3>🚀 AI-Powered Wisdom Creation Workflow</h3>
            <p>Simply tell your story, and our 7 intelligent agents will analyze it for you!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get access token for API calls
        if not st.session_state.get('access_token'):
            st.warning("⚠️ Please login to access the AI-powered workflow.")
            show_login()
        else:
            # Workflow steps
            if st.session_state.current_step == "story_input":
                show_story_input()
            elif st.session_state.current_step == "layer_review":
                show_layer_review()
            elif st.session_state.current_step == "deep_vibe":
                show_deep_vibe_distillation()
            else:
                show_story_input()

if __name__ == "__main__":
    main()
