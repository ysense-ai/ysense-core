# streamlit_app.py
"""
YSense™ Platform v2.0 - Complete Integrated Streamlit UI
Combines all components: Registration, Wisdom Collection, Distillation, Revenue Dashboard
"""

import streamlit as st
import pandas as pd
import asyncio
from datetime import datetime, timedelta
import json
import hashlib
import secrets
import requests
from typing import Dict, List, Optional

# Page Configuration
st.set_page_config(
    page_title="YSense™ | 慧觉™ - AI Attribution Infrastructure",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Revenue box */
    .revenue-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    /* Quality indicators */
    .quality-high { 
        color: #10b981; 
        font-weight: bold;
        font-size: 1.2em;
    }
    .quality-medium { 
        color: #f59e0b; 
        font-weight: bold;
        font-size: 1.2em;
    }
    .quality-low { 
        color: #ef4444; 
        font-weight: bold;
        font-size: 1.2em;
    }
    
    /* Wisdom cards */
    .wisdom-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #667eea;
    }
    
    /* Vibe words */
    .vibe-word {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 5px;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
    }
    .status-published {
        background: #10b981;
        color: white;
    }
    .status-pending {
        background: #f59e0b;
        color: white;
    }
    .status-draft {
        background: #6b7280;
        color: white;
    }
    
    /* Consent checkboxes */
    .consent-box {
        background: #f3f4f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Five Layers */
    .layer-card {
        background: #fafafa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid #667eea;
    }
    
    /* Header */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0;
    }
    
    /* Tier badges */
    .tier-bronze { background: #cd7f32; color: white; }
    .tier-silver { background: #c0c0c0; color: black; }
    .tier-gold { background: #ffd700; color: black; }
    .tier-platinum { background: #e5e4e2; color: black; }
    .tier-diamond { background: linear-gradient(135deg, #b9f2ff 0%, #ffffff 100%); color: black; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'z_protocol_tier' not in st.session_state:
        st.session_state.z_protocol_tier = "Bronze"
    if 'pending_wisdom' not in st.session_state:
        st.session_state.pending_wisdom = []
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = "http://localhost:8003/api/v3"

# API Helper Functions
def api_call(method: str, endpoint: str, data: Dict = None, authenticated: bool = True):
    """Make API call to backend"""
    url = f"{st.session_state.api_base_url}/{endpoint}"
    headers = {}
    
    if authenticated and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return None
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server. Please ensure the backend is running.")
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def get_tier_badge(tier: str) -> str:
    """Get HTML for tier badge"""
    tier_class = f"tier-{tier.lower()}"
    emoji = {"Bronze": "🥉", "Silver": "🥈", "Gold": "🥇", "Platinum": "💎", "Diamond": "💠"}.get(tier, "🏆")
    return f'<span class="status-badge {tier_class}">{emoji} {tier}</span>'

# Authentication Functions
def show_login():
    """Show login form"""
    st.markdown("### 🔐 Login to YSense")
    
    with st.form("login_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            username_or_email = st.text_input("Username or Email")
            crypto_key = st.text_input("Crypto Key", type="password", help="Your unique crypto key from registration")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted and username_or_email and crypto_key:
            result = api_call("POST", "auth/login", {
                "username_or_email": username_or_email,
                "crypto_key": crypto_key
            }, authenticated=False)
            
            if result:
                st.session_state.authenticated = True
                st.session_state.token = result["access_token"]
                st.session_state.user_id = result["user_id"]
                st.session_state.username = result["username"]
                st.session_state.z_protocol_tier = result["z_protocol_tier"]
                st.success("Login successful!")
                st.rerun()

def show_registration():
    """Show registration form with comprehensive consent"""
    st.markdown("### 📝 Join YSense - Your Wisdom, Your Attribution, Your Revenue")
    
    with st.form("registration_form"):
        st.markdown("#### Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", help="Choose a unique username")
            email = st.text_input("Email*", help="Your email for account access")
            st.info("🔑 **No Password Required!** You'll receive a unique crypto key for login after registration.")
        
        with col2:
            age = st.number_input("Age*", min_value=18, max_value=120, help="Must be 18 or older")
            jurisdiction = st.selectbox("Jurisdiction*", 
                ["Malaysia", "Singapore", "EU", "Global"],
                help="Determines applicable data protection laws")
            cultural_context = st.selectbox("Cultural Context", 
                ["Malaysian", "Malaysian Chinese", "Hokkien", "Southeast Asian", 
                 "Indigenous", "Global South", "Global"],
                help="Helps calculate cultural multipliers for revenue")
        
        attribution_name = st.text_input("Attribution Name (Optional)", 
            help="How you want to be credited (defaults to username)")
        
        st.markdown("---")
        st.markdown("#### 📜 Terms of Service & Required Consents")
        
        # Display key terms
        with st.expander("View Terms of Service (v2.0)"):
            st.markdown("""
            **YSense Platform Terms - Key Points:**
            
            1. **Your Rights:**
               - You retain copyright to your wisdom
               - Permanent attribution guaranteed
               - 30-50% revenue share based on tier
               - Right to deletion (except published wisdom)
            
            2. **Your Responsibilities:**
               - Content must be original (no copyright infringement)
               - You accept liability for fraudulent submissions
               - Minimum age: 18 years
            
            3. **Platform Usage:**
               - Wisdom may be licensed for AI training
               - Attribution always required
               - Revenue distributed monthly (€50 minimum)
               - Z Protocol compliance required (80%+ score)
            
            4. **Data Protection:**
               - GDPR/PDPA compliant
               - Data portability supported
               - 7-year audit trail retention
               - Encryption at rest and in transit
            """)
        
        st.markdown("#### Required Consents (All must be accepted)")
        
        consent_data_collection = st.checkbox(
            "✅ **Data Collection**: I consent to YSense collecting my wisdom contributions",
            help="Required for platform functionality"
        )
        
        consent_commercial_use = st.checkbox(
            "✅ **Commercial Use**: I consent to commercial use with mandatory attribution",
            help="Enables revenue generation from your wisdom"
        )
        
        consent_ai_training = st.checkbox(
            "✅ **AI Training**: I consent to ethical AI training use with attribution",
            help="Your wisdom helps train more ethical AI systems"
        )
        
        consent_revenue_sharing = st.checkbox(
            "✅ **Revenue Model**: I accept the 30-50% tiered revenue sharing terms",
            help="Higher tiers earn more (up to 50% for Diamond tier)"
        )
        
        consent_attribution = st.checkbox(
            "✅ **Attribution**: I understand attribution is permanent and cannot be removed",
            help="Your contribution will always be credited to you"
        )
        
        consent_terms = st.checkbox(
            "✅ **Terms Acceptance**: I have read and accept the Terms of Service v2.0",
            help="Complete terms available above"
        )
        
        st.markdown("#### Optional Consents")
        
        marketing_consent = st.checkbox(
            "📧 Marketing communications about platform updates",
            help="Optional - can be changed anytime"
        )
        
        research_consent = st.checkbox(
            "🔬 Participation in academic research studies",
            help="Optional - additional revenue opportunities"
        )
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            # Validate required consents
            if not all([consent_data_collection, consent_commercial_use, 
                       consent_ai_training, consent_revenue_sharing, 
                       consent_attribution, consent_terms]):
                st.error("All required consents must be accepted")
            elif not username or not email:
                st.error("Please fill in all required fields")
            else:
                # Register user
                result = api_call("POST", "auth/register", {
                    "username": username,
                    "email": email,
                    "age": age,
                    "jurisdiction": jurisdiction,
                    "cultural_context": cultural_context,
                    "attribution_name": attribution_name,
                    "consent_data_collection": consent_data_collection,
                    "consent_commercial_use": consent_commercial_use,
                    "consent_ai_training": consent_ai_training,
                    "consent_revenue_sharing": consent_revenue_sharing,
                    "consent_attribution": consent_attribution,
                    "consent_terms": consent_terms,
                    "marketing_consent": marketing_consent,
                    "research_consent": research_consent
                }, authenticated=False)
                
                if result:
                    st.success("✅ Registration successful!")
                    st.info(f"🔑 **Your Crypto Key:** `{result['crypto_key']}`")
                    st.info(f"🛡️ **Your Z Protocol Consent Key:** `{result['z_protocol_consent_key']}`")
                    st.warning("⚠️ **IMPORTANT:** Save both keys! You'll need the crypto key to log in, and the Z Protocol key for consent management.")
                    st.session_state.authenticated = True
                    st.session_state.token = result["access_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.username = result["username"]
                    st.session_state.z_protocol_tier = result["z_protocol_tier"]
                    st.rerun()

# Main Application Pages
def show_dashboard():
    """Show main dashboard"""
    st.markdown("## 📊 Dashboard")
    
    # Get user info
    user_info = api_call("GET", "auth/me")
    
    if user_info:
        # User metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Z Protocol Tier", user_info["z_protocol_tier"], 
                     help=f"Score: {user_info['z_protocol_score']:.1f}/100")
        
        with col2:
            st.metric("Revenue Share", f"{user_info['revenue_share_percentage']:.0f}%",
                     help="Your current revenue percentage")
        
        with col3:
            st.metric("Total Earnings", f"€{user_info['total_earnings']:.2f}",
                     delta=f"€{user_info['pending_earnings']:.2f} pending")
        
        with col4:
            st.metric("Attribution ID", user_info["attribution_id"][:8] + "...",
                     help="Your unique attribution identifier")
        
        # Revenue Analytics
        st.markdown("### 💰 Revenue Analytics")
        
        revenue_data = api_call("GET", "revenue/analytics")
        if revenue_data:
            # Revenue chart
            if revenue_data.get("revenue_trend"):
                df = pd.DataFrame(revenue_data["revenue_trend"])
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                    st.line_chart(df.set_index('date')['revenue'])
            
            # Top performing wisdom
            if revenue_data.get("top_performing_drops"):
                st.markdown("#### 🏆 Top Performing Wisdom")
                for drop in revenue_data["top_performing_drops"][:3]:
                    st.info(f"**{drop['title']}** - Revenue: €{drop['revenue']:.2f}")

def show_wisdom_creation():
    """Show wisdom creation interface with Five Layers"""
    st.markdown("## 🌟 Create Wisdom Drop")
    st.info("Complete the 5-Layer Perception Toolkit, then add Deep Vibe Distillation for maximum quality")
    
    with st.form("wisdom_creation"):
        # Basic Info
        title = st.text_input("Title*", placeholder="Give your wisdom a meaningful title")
        experience_title = st.text_input("Experience Title", 
            placeholder="What experience does this wisdom come from?")
        
        # Five Layers
        st.markdown("### 📝 Five-Layer Perception Toolkit")
        
        layer_narrative = st.text_area(
            "1️⃣ **Narrative Layer**",
            placeholder="What is the unspoken story of this place or thing? As well as, what is the well-known story of it too from my perspective?",
            height=100,
            help="Tell the story from your perspective. What is the unspoken narrative? What is the well-known story?"
        )
        
        # Character count for narrative layer
        if layer_narrative:
            char_count = len(layer_narrative.strip())
            if char_count < 20:
                st.warning(f"⚠️ Narrative Layer needs at least 20 characters. Current: {char_count} characters. Please add more detail about the story.")
            else:
                st.success(f"✅ Narrative Layer: {char_count} characters")
        
        layer_somatic = st.text_area(
            "2️⃣ **Somatic Layer**",
            placeholder="What does being here make my emotion and body feel? What in my mind as present here?",
            height=100,
            help="Describe your physical and emotional sensations. What does your body feel? What emotions arise?"
        )
        
        # Character count for somatic layer
        if layer_somatic:
            char_count = len(layer_somatic.strip())
            if char_count < 20:
                st.warning(f"⚠️ Somatic Layer needs at least 20 characters. Current: {char_count} characters. Please add more detail about your physical and emotional sensations.")
            else:
                st.success(f"✅ Somatic Layer: {char_count} characters")
        
        layer_attention = st.text_area(
            "3️⃣ **Attention Layer**",
            placeholder="What is one tiny detail here that most people would miss? What do I miss out in this places and things?",
            height=100,
            help="Focus on the small details that others might miss. What do you notice that others don't?"
        )
        
        # Character count for attention layer
        if layer_attention:
            char_count = len(layer_attention.strip())
            if char_count < 20:
                st.warning(f"⚠️ Attention Layer needs at least 20 characters. Current: {char_count} characters. Please add more detail about the small details you notice.")
            else:
                st.success(f"✅ Attention Layer: {char_count} characters")
        
        layer_synesthetic = st.text_area(
            "4️⃣ **Synesthetic Layer**",
            placeholder="What are three non-visual words to describe the 'vibe' here? Let it flow through me and feels. Describe the sensory experience - what does it feel like, sound like, smell like?",
            height=100,
            help="Describe the sensory experience in detail. What does it feel like, sound like, smell like? Use vivid, descriptive language."
        )
        
        # Character count for synesthetic layer
        if layer_synesthetic:
            char_count = len(layer_synesthetic.strip())
            if char_count < 20:
                st.warning(f"⚠️ Synesthetic Layer needs at least 20 characters. Current: {char_count} characters. Please add more detail about the sensory experience.")
            else:
                st.success(f"✅ Synesthetic Layer: {char_count} characters")
        
        layer_temporal_auditory = st.text_area(
            "5️⃣ **Temporal-Auditory Layer**",
            placeholder="If this moment had a sound, what would it be?",
            height=100,
            help="Describe the sounds, rhythms, and temporal qualities of this experience. What does it sound like? What rhythm does it have?"
        )
        
        # Character count for temporal-auditory layer
        if layer_temporal_auditory:
            char_count = len(layer_temporal_auditory.strip())
            if char_count < 20:
                st.warning(f"⚠️ Temporal-Auditory Layer needs at least 20 characters. Current: {char_count} characters. Please add more detail about the sounds and rhythms.")
            else:
                st.success(f"✅ Temporal-Auditory Layer: {char_count} characters")
        
        # Cultural Context
        cultural_context = st.selectbox(
            "Cultural Context",
            ["Malaysian", "Malaysian Chinese", "Hokkien", "Southeast Asian", 
             "Indigenous", "Global South", "Global"],
            help="Higher multipliers for Malaysian content (1.6x)"
        )
        
        submitted = st.form_submit_button("Create Wisdom Drop", use_container_width=True)
        
        if submitted:
            if not all([title, layer_narrative, layer_somatic, layer_attention, 
                       layer_synesthetic, layer_temporal_auditory]):
                st.error("Please complete all five layers")
            else:
                # Create wisdom drop
                result = api_call("POST", "wisdom/create", {
                    "title": title,
                    "experience_title": experience_title or title,
                    "layer_narrative": layer_narrative,
                    "layer_somatic": layer_somatic,
                    "layer_attention": layer_attention,
                    "layer_synesthetic": layer_synesthetic,
                    "layer_temporal_auditory": layer_temporal_auditory,
                    "cultural_context": cultural_context
                })
                
                if result:
                    st.success(f"✅ Wisdom Drop Created! Quality Score: {result['quality_score']:.1f}/100")
                    st.info(f"Next Step: Complete Deep Vibe Distillation to maximize quality and revenue")
                    st.session_state.pending_wisdom.append(result['id'])

def show_distillation():
    """Show Deep Vibe Distillation for pending wisdom"""
    st.markdown("## ✨ Deep Vibe Distillation")
    
    # Get pending wisdom drops
    my_drops = api_call("GET", "wisdom/my-drops?status=awaiting_distillation")
    
    if my_drops and my_drops.get("wisdom_drops"):
        for drop in my_drops["wisdom_drops"]:
            with st.expander(f"🔮 {drop['title']} (Score: {drop['quality_score']:.1f})"):
                st.markdown("### Extract the Three Sacred Words")
                st.info("If you had to describe the single, core 'echo' that this entire experience leaves in your heart, what is that feeling?")
                
                with st.form(f"distill_{drop['id']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        word1 = st.text_input("First Vibe Word", key=f"w1_{drop['id']}")
                    with col2:
                        word2 = st.text_input("Second Vibe Word", key=f"w2_{drop['id']}")
                    with col3:
                        word3 = st.text_input("Third Vibe Word", key=f"w3_{drop['id']}")
                    
                    personal_connection = st.text_area(
                        "Personal Connection",
                        placeholder="What personal meaning does this wisdom hold for you?",
                        key=f"pc_{drop['id']}"
                    )
                    
                    essence = st.text_input(
                        "Essence (Optional)",
                        placeholder="Capture the core essence in one sentence",
                        key=f"es_{drop['id']}"
                    )
                    
                    submitted = st.form_submit_button("Complete Distillation")
                    
                    if submitted:
                        if not all([word1, word2, word3, personal_connection]):
                            st.error("Please provide all three vibe words and personal connection")
                        else:
                            result = api_call("POST", f"wisdom/{drop['id']}/distill", {
                                "vibe_words": [word1, word2, word3],
                                "personal_connection": personal_connection,
                                "essence": essence
                            })
                            
                            if result:
                                st.success(f"✨ Distillation Complete! New Quality: {result['quality_score']:.1f}/100")
                                st.balloons()
                                st.info(f"Revenue Potential: €{result['revenue_potential']:.2f}")
    else:
        st.info("No wisdom drops awaiting distillation. Create a new wisdom drop first!")

def show_my_wisdom():
    """Show user's wisdom collection"""
    st.markdown("## 📚 My Wisdom Collection")
    
    # Get wisdom drops
    my_drops = api_call("GET", "wisdom/my-drops")
    
    if my_drops and my_drops.get("wisdom_drops"):
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        total = len(my_drops["wisdom_drops"])
        published = sum(1 for d in my_drops["wisdom_drops"] if d["published"])
        total_revenue = sum(d.get("revenue_generated", 0) for d in my_drops["wisdom_drops"])
        
        with col1:
            st.metric("Total Drops", total)
        with col2:
            st.metric("Published", published)
        with col3:
            st.metric("Revenue Generated", f"€{total_revenue:.2f}")
        
        # Wisdom list
        for drop in my_drops["wisdom_drops"]:
            status_class = "status-published" if drop["published"] else "status-pending"
            status_text = "Published" if drop["published"] else drop["status"].replace("_", " ").title()
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {drop['title']}")
                    if drop.get("vibe_words"):
                        st.markdown("**Vibe Words:** " + " • ".join(drop["vibe_words"]))
                
                with col2:
                    st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', 
                               unsafe_allow_html=True)
                
                with col3:
                    if not drop["published"] and drop["distillation_completed"]:
                        if st.button(f"Publish", key=f"pub_{drop['id']}"):
                            # Show publication confirmation
                            st.warning("Publishing requires Z Protocol validation (80%+ score)")
    else:
        st.info("You haven't created any wisdom drops yet. Start sharing your wisdom!")

# Main App Logic
def main():
    """Main application entry point"""
    init_session_state()
    
    # Header
    st.markdown("""
    <h1>💧 YSense™ | 慧觉™</h1>
    <p style='text-align: center; font-size: 1.2em;'>
    World's First AI Attribution Infrastructure<br>
    <em>Defensive Publication Protected (DOI: 10.5281/zenodo.17072168)</em>
    </p>
    """, unsafe_allow_html=True)
    
    # Version Selection
    version = st.sidebar.selectbox(
        "Choose Platform Version",
        ["v3.0 - Complete Platform", "v4.0 - AI-Powered Workflow"],
        help="v3.0: Full manual control | v4.0: AI-assisted workflow"
    )
    
    # Authentication check
    if not st.session_state.authenticated:
        tab1, tab2, tab3 = st.tabs(["🏠 Home", "🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("""
            ### Welcome to YSense - Your Wisdom Matters
            
            YSense is building the world's first attribution infrastructure for ethical AI training.
            Every piece of wisdom you share is permanently attributed to you and generates revenue
            when used for AI training.
            
            **🎯 Our Mission:**
            - Ensure human wisdom is never used without attribution
            - Create sustainable revenue for wisdom contributors
            - Build more ethical and culturally aware AI systems
            - Protect traditional and cultural knowledge
            
            **💰 Revenue Model:**
            - 30-50% revenue share based on your tier
            - Higher quality wisdom earns more
            - Cultural content gets multiplier bonuses
            - Monthly payments (€50 minimum)
            
            **🛡️ Your Protection:**
            - Defensive publication prevents patent theft
            - Permanent cryptographic attribution
            - GDPR/PDPA compliant
            - Right to deletion (except published wisdom)
            
            **Get Started:** Register to start contributing your wisdom!
            """)
        
        with tab2:
            show_login()
        
        with tab3:
            show_registration()
    
    else:
        # Authenticated user interface
        if version == "v4.0 - AI-Powered Workflow":
            show_v4_interface()
        else:
            # v3.0 interface
            with st.sidebar:
                st.markdown(f"### Welcome, {st.session_state.username}!")
                st.markdown(get_tier_badge(st.session_state.z_protocol_tier), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            page = st.selectbox(
                "Navigation",
                ["📊 Dashboard", "🌟 Create Wisdom", "✨ Distillation", 
                 "📚 My Collection", "💰 Revenue", "⚙️ Settings"]
            )
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                api_call("POST", "auth/logout")
                st.session_state.authenticated = False
                st.session_state.token = None
                st.session_state.user_id = None
                st.rerun()
    
    # Set page for non-authenticated users
    if not st.session_state.get('authenticated', False):
        page = "🔐 Login"
    
    # Page routing
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🌟 Create Wisdom":
        show_wisdom_creation()
    elif page == "✨ Distillation":
        show_distillation()
    elif page == "📚 My Collection":
        show_my_wisdom()
    elif page == "💰 Revenue":
        st.markdown("## 💰 Revenue Center")
        
        # Get revenue data
        revenue_data = api_call("GET", "revenue/analytics")
        if revenue_data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Earnings", f"€{revenue_data['total_earnings']:.2f}")
            with col2:
                st.metric("Pending", f"€{revenue_data['pending_earnings']:.2f}")
            with col3:
                st.metric("Paid Out", f"€{revenue_data['paid_earnings']:.2f}")
            
            # Request payment button
            if revenue_data['payment_threshold_reached']:
                if st.button("💳 Request Payment", use_container_width=True):
                    st.info("Payment request feature coming soon!")
    
    elif page == "⚙️ Settings":
        st.markdown("## ⚙️ Settings")
        
        # Consent management
        st.markdown("### 📋 Consent Management")
        user_consents = api_call("GET", "legal/my-consents")
        if user_consents:
            st.json(user_consents["current_consents"])
        
        # Data export
        st.markdown("### 📥 Data Export (GDPR)")
        if st.button("Export My Data"):
            st.info("Data export will download all your information in JSON format")
    
    elif page == "🔐 Login":
        show_login_register()

    # Footer
    st.markdown("---")
    st.markdown("""
    <p style='text-align: center; color: #666;'>
    YSense™ Platform v2.0 | Protected by Defensive Publication<br>
    Building Ethical AI Through Human Wisdom | Teluk Intan, Malaysia 🇲🇾
    </p>
    """, unsafe_allow_html=True)

def show_v4_interface():
    """Show v4.0 AI-Powered Workflow Interface"""
    st.markdown("## 🚀 YSense Platform v4.0 - AI-Powered Workflow")
    st.info("✨ **Revolutionary Feature:** Simply tell your story, and our AI will analyze it with 7 intelligent agents!")
    
    # Import and use the v4.0 interface
    try:
        from streamlit_ai_interface import show_ai_story_interface
        show_ai_story_interface()
    except ImportError:
        st.error("v4.0 AI interface not available. Please ensure streamlit_ai_interface.py is in the project directory.")
        st.info("Falling back to v3.0 interface...")
        show_v3_interface()

def show_v3_interface():
    """Show v3.0 Complete Platform Interface"""
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.username}!")
        st.markdown(get_tier_badge(st.session_state.z_protocol_tier), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "Navigation",
            ["📊 Dashboard", "🌟 Create Wisdom", "✨ Distillation", 
             "📚 My Collection", "💰 Revenue", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.crypto_key = None
            st.session_state.z_protocol_consent_key = None
            st.rerun()
    

if __name__ == "__main__":
    main()
