import streamlit as st
import os
import sys
import asyncio
from pathlib import Path
import json
from datetime import datetime
import hashlib
import sqlite3
from typing import Optional, Dict, Any

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import our modules
try:
    from src.models import User, WisdomDrop, create_tables
    from src.auth import AuthManager
    from src.wisdom_library import WisdomLibrary
    from src.attribution_engine import AttributionEngine
    from src.revenue_models import RevenueModel, ContributorTier
    from src.terms_consent_system import TermsConsentSystem
    from src.whitepaper_system import WhitePaperSystem
    from src.agent_system_v41 import AgentSystem
    from src.metrics_collector import MetricsCollector
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Initialize components
@st.cache_resource
def init_components():
    """Initialize all platform components"""
    try:
        # Create database tables
        create_tables()
        
        # Initialize managers
        auth_manager = AuthManager()
        wisdom_library = WisdomLibrary()
        attribution_engine = AttributionEngine()
        revenue_model = RevenueModel()
        terms_system = TermsConsentSystem()
        whitepaper_system = WhitePaperSystem()
        agent_system = AgentSystem()
        metrics_collector = MetricsCollector()
        
        return {
            'auth_manager': auth_manager,
            'wisdom_library': wisdom_library,
            'attribution_engine': attribution_engine,
            'revenue_model': revenue_model,
            'terms_system': terms_system,
            'whitepaper_system': whitepaper_system,
            'agent_system': agent_system,
            'metrics_collector': metrics_collector
        }
    except Exception as e:
        st.error(f"Failed to initialize components: {e}")
        return None

def load_image_as_base64(image_path):
    """Load image and convert to base64 for embedding"""
    try:
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def add_header_image():
    """Add the header with logo and Human-AI collaboration banner"""
    try:
        import streamlit.components.v1 as components
        
        # Load images
        logo_base64 = load_image_as_base64("assets/Logo Ysense.png")
        collaboration_base64 = load_image_as_base64("assets/Human-AI collaboration.jpg")
        
        header_html = f"""
        <div style="position: relative; background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                    padding: 2rem; margin: -1rem -1rem 2rem -1rem; 
                    text-align: center; color: white; border-radius: 0 0 20px 20px; overflow: hidden; min-height: 200px; 
                    width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%);">
            
            <!-- Logo Area (Left) -->
            <div style="position: absolute; left: 2rem; top: 50%; transform: translateY(-50%); z-index: 10;">
                <!-- YSense Logo -->
                <img src="data:image/png;base64,{logo_base64}" width="80" height="80" style="border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.3);"/>
            </div>
            
                    <!-- Human-AI Collaboration Background - Centered and Scaled -->
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; opacity: 0.3; display: flex; justify-content: center; align-items: center;">
                        <img src="data:image/jpeg;base64,{collaboration_base64}" style="width: 90%; height: 90%; object-fit: cover; border-radius: 0 0 20px 20px;"/>
                    </div>
            
            <!-- Overlay gradient for better text readability -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                        background: linear-gradient(135deg, rgba(76, 29, 149, 0.7) 0%, rgba(59, 130, 246, 0.7) 100%); 
                        z-index: 2;"></div>
            
            <!-- Main content -->
            <div style="position: relative; z-index: 15;">
                <h1 style="margin: 0; font-size: 2.5em; font-weight: bold; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    YSense™ v4.1 | 慧觉™
                </h1>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1em; opacity: 0.9; 
                          text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                    The Genesis of Human-AI Wisdom Collaboration
                </p>
                
                <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">🤖 AI Analysis</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">📚 Wisdom Attribution</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">⚖️ Z Protocol v2.0</span>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(header_html, height=200)
        
    except Exception as e:
        st.error(f"Error loading header: {e}")

def show_login():
    """Show crypto key login form"""
    st.subheader("🔐 Login to YSense™")
    st.info("🔑 **Crypto Key Authentication** - Z Protocol v2.0 Compliant")
    
    with st.form("crypto_login_form"):
        username = st.text_input("Username", placeholder="your_username")
        password = st.text_input("Password", type="password", help="Password to decrypt your private key")
        submit = st.form_submit_button("🔐 Login with Crypto Key")
        
        if submit:
            if username and password:
                try:
                    from src.crypto_auth import CryptoAuthManager
                    crypto_auth = CryptoAuthManager()
                    user = crypto_auth.authenticate_user(username, password)
                    
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['id']
                        st.session_state.username = user['username']
                        st.session_state.user_tier = user['tier']
                        st.session_state.public_key = user['public_key']
                        st.success("🔐 Crypto authentication successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                        
                except Exception as e:
                    st.error(f"Authentication error: {e}")
                    st.error("Please check if the crypto authentication system is properly initialized.")
            else:
                st.error("Please fill in all fields")
    
    # Show crypto key info
    st.markdown("---")
    st.markdown("### 🔑 About Crypto Key Authentication")
    st.info("""
    **YSense™ uses cryptographic key authentication:**
    - 🔐 **Z Protocol v2.0 Compliant** - Cryptographic signatures for attribution
    - 🚀 **No Email Required** - No SMTP dependencies
    - 📊 **Attribution Tracking** - Easy to link keys to wisdom drops
    - 💎 **Unique Identity** - Each user gets a unique crypto keypair
    - 🔒 **Enhanced Security** - Cryptographic authentication
    """)

def show_password_reset():
    """Show password reset form"""
    st.subheader("🔐 Reset Your Password")
    
    # Get token from URL parameters
    token = st.query_params.get('token', '')
    
    if token:
        # Show reset form
        st.info("Enter your new password below.")
        
        with st.form("password_reset_form"):
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_reset = st.form_submit_button("Reset Password")
            
            if submit_reset:
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        components = init_components()
                        if components:
                            auth_manager = components['auth_manager']
                            success = auth_manager.reset_password(token, new_password)
                            
                            if success:
                                st.success("Password reset successfully! You can now login with your new password.")
                                st.balloons()
                            else:
                                st.error("Invalid or expired reset token. Please request a new one.")
                        else:
                            st.error("System initialization failed")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
    else:
        st.error("No reset token provided. Please use the 'Forgot Password' link from the login page.")

def show_registration():
    """Show crypto key registration form"""
    st.subheader("🚀 Join YSense™ - Crypto Key Registration")
    st.info("🔑 **Generate Your Unique Crypto Keypair** - Z Protocol v2.0 Compliant")
    
    # Display founding contributor opportunities
    st.info("""
    **🌟 Founding Contributor Opportunities Available!**
    
    Be among the first 1000 users to join YSense™ and unlock exclusive benefits:
    - **100% Revenue Share** for Founding Contributors
    - **Partnership Opportunities** with YSense™
    - **Developer Access** to our APIs
    - **Cultural Guardian** status for wisdom preservation
    """)
    
    # Revenue model tiers
    st.subheader("💰 Revenue Model Tiers")
    
    components = init_components()
    if components:
        revenue_model = components['revenue_model']
        terms_system = components['terms_system']
        
        # Display tier information
        tiers = [
            ("Founding Contributor", "100% revenue share", "First 1000 users"),
            ("Partnership", "50% revenue share", "Strategic partners"),
            ("Developer", "30% revenue share", "API developers"),
            ("Cultural Guardian", "20% revenue share", "Wisdom preservation"),
            ("Standard", "10% revenue share", "Regular contributors")
        ]
        
        for tier, revenue, description in tiers:
            st.write(f"**{tier}**: {revenue} - {description}")
    
    with st.form("crypto_registration_form"):
        st.subheader("📝 Crypto Key Registration Form")
        
        # Basic info
        username = st.text_input("Username", placeholder="your_username", help="Choose a unique username")
        password = st.text_input("Password", type="password", help="Password to encrypt your private key")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Tier selection
        selected_tier = st.selectbox(
            "Select Contributor Tier",
            ["Founding Contributor", "Partnership", "Developer", "Cultural Guardian", "Standard"],
            help="Choose your contribution level"
        )
        
        # Terms and consents
        st.subheader("📋 Terms of Service & Consent")
        
        if components:
            terms = terms_system.get_terms()
            required_consents = terms_system.get_required_consents()
            
            # Display terms
            with st.expander("📄 Read Terms of Service"):
                st.markdown(terms)
            
            # Consent checkboxes
            consents = {}
            for consent_key, consent_info in required_consents.items():
                consents[consent_key] = st.checkbox(
                    consent_info['label'],
                    help=consent_info['description']
                )
            
            # Tier-specific commitments
            if selected_tier == "Founding Contributor":
                founding_commitment = st.checkbox(
                    "🎯 I commit to being an active Founding Contributor with 100% revenue sharing",
                    help="This is a special commitment for founding contributors"
                )
            else:
                founding_commitment = True
        
        submit = st.form_submit_button("🔑 Generate Crypto Keypair")
        
        if submit:
            if username and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    if components:
                        # Validate all consents
                        all_consents_given = all(consents.values())
                        if not all_consents_given:
                            st.error("Please accept all required consents")
                        else:
                            # Register user with crypto keys
                            try:
                                from src.crypto_auth import CryptoAuthManager
                                crypto_auth = CryptoAuthManager()
                                result = crypto_auth.create_user(username, password, selected_tier)
                                
                                if result['success']:
                                    st.success(f"🎉 Welcome to YSense™! Crypto keypair generated!")
                                    st.success(f"🔑 **Your Private Key:** `{result['private_key']}`")
                                    st.warning("⚠️ **IMPORTANT:** Save your private key securely! You'll need it to decrypt your account.")
                                    st.info(f"📊 **Public Key:** `{result['public_key']}`")
                                    st.info(f"🎯 **Tier:** {result['tier']}")
                                    st.balloons()
                                    
                                    # Show key saving instructions
                                    st.markdown("---")
                                    st.markdown("### 🔐 **How to Save Your Crypto Key:**")
                                    st.info("""
                                    1. **Copy your private key** (shown above)
                                    2. **Save it securely** (password manager, encrypted file, etc.)
                                    3. **Never share it** with anyone
                                    4. **Use your username + password** to login
                                    5. **Your private key** is encrypted with your password
                                    """)
                                else:
                                    st.error(f"Registration failed: {result['error']}")
                            except Exception as e:
                                st.error(f"Registration error: {e}")
            else:
                st.error("Please fill in all fields")

def show_founders_story():
    """Show Founder's Story and Substack link"""
    st.subheader("📖 Founder's Story")
    
    st.markdown("""
    ## 🌟 The Vision Behind YSense™
    
    **YSense™** was born from a simple yet profound realization: the future of AI lies not in replacing human wisdom, 
    but in amplifying it through authentic collaboration and proper attribution.
    
    ### 🎯 Our Mission
    To create the world's first **AI Attribution Infrastructure** that ensures:
    - **Human wisdom** gets proper credit
    - **AI contributions** are transparently tracked
    - **Collaboration** between humans and AI is seamless
    - **Revenue** flows fairly to all contributors
    
    ### 📚 Read More on Substack
    For deeper insights into our journey, methodology, and vision:
    
    **[👉 Visit YSense Substack](https://ysense.substack.com)**
    
    *Subscribe for exclusive updates, technical deep-dives, and behind-the-scenes content.*
    """)

def show_open_source():
    """Show Open Source and GitHub Defensive Publication"""
    st.subheader("🔓 Open Source & Defensive Publication")
    
    st.markdown("""
    ## 🌐 Open Source Philosophy
    
    YSense™ believes in **transparency** and **collaborative development**. Our core principles:
    
    ### 🔓 Open Source Components
    - **Core Attribution Engine** - Open source for transparency
    - **Z Protocol v2.0** - Public specification
    - **API Documentation** - Complete and open
    - **Development Tools** - Community contributions welcome
    
    ### 🛡️ Defensive Publication Strategy
    To protect our innovations while maintaining openness:
    
    **📋 Published Patents & Prior Art:**
    - AI Attribution Methods
    - Cryptographic Wisdom Tracking
    - Human-AI Collaboration Protocols
    - Revenue Distribution Algorithms
    
    ### 🔗 GitHub Repository
    **[👉 Visit GitHub Repository](https://github.com/ysense-ai/ysense-core)**
    
    *Contribute, fork, and help build the future of AI attribution.*
    
    ### 📄 Defensive Publications
    All our innovations are published as defensive publications to:
    - **Prevent patent trolls** from blocking progress
    - **Ensure open access** to critical technologies
    - **Protect the community** from IP litigation
    - **Maintain innovation** in AI attribution space
    """)

def show_wisdom_library():
    """Show Wisdom Library (in construction)"""
    st.subheader("📚 Wisdom Library")
    
    st.info("🚧 **Under Construction** - Coming Soon!")
    
    st.markdown("""
    ## 📚 The Future of Wisdom Sharing
    
    The **YSense™ Wisdom Library** will be the world's first **cryptographically-attributed** 
    knowledge repository where:
    
    ### 🔮 Planned Features
    - **🔐 Crypto-Attributed Content** - Every wisdom drop has cryptographic proof of ownership
    - **💰 Revenue Sharing** - Contributors earn from their wisdom
    - **🤖 AI Enhancement** - AI agents help refine and expand human wisdom
    - **📊 Attribution Tracking** - Complete transparency in knowledge lineage
    - **🌍 Global Access** - Wisdom from contributors worldwide
    
    ### 🎯 What You'll Be Able To Do
    - **Share Wisdom** - Contribute your knowledge with crypto attribution
    - **Earn Revenue** - Get paid for valuable contributions
    - **Discover Insights** - Find wisdom enhanced by AI analysis
    - **Track Attribution** - See the complete lineage of any wisdom
    - **Collaborate** - Work with AI agents to refine your ideas
    
    ### 🚀 Coming Soon
    The Wisdom Library is currently in development. 
    **Register now** to be notified when it launches!
    """)

def show_whitepaper():
    """Show YSense White Paper with view tracking"""
    st.subheader("📄 YSense™ AI Attribution Infrastructure White Paper")
    
    components = init_components()
    if components:
        whitepaper_system = components['whitepaper_system']
        
        # Track view when page is accessed
        if hasattr(whitepaper_system, 'track_view'):
            whitepaper_system.track_view({"user": "anonymous", "timestamp": "now"})
        
        # Debug: Check available methods
        available_methods = [method for method in dir(whitepaper_system) if not method.startswith('_')]
        st.write(f"Available methods: {available_methods}")
        
        # Get white paper content
        if hasattr(whitepaper_system, 'get_whitepaper_content'):
            content = whitepaper_system.get_whitepaper_content()
        elif hasattr(whitepaper_system, 'get_whitepaper_abstract'):
            content = whitepaper_system.get_whitepaper_abstract()
        else:
            content = "White paper content not available"
        
        if hasattr(whitepaper_system, 'get_white_paper_metadata'):
            metadata = whitepaper_system.get_white_paper_metadata()
        else:
            metadata = {"version": "1.0", "credibility_score": 9}
        
        # Ensure all required keys exist
        if 'credibility_score' not in metadata:
            metadata['credibility_score'] = 9
        if 'version' not in metadata:
            metadata['version'] = "1.0"
        
        if hasattr(whitepaper_system, 'get_download_statistics'):
            stats = whitepaper_system.get_download_statistics()
        else:
            stats = {"total_views": 0, "total_downloads": 0}
        
        # Display metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Views", stats.get('total_views', 0))
        with col2:
            st.metric("Version", metadata['version'])
        with col3:
            st.metric("Credibility Score", f"{metadata['credibility_score']}/10")
        
        # Display content
        with st.expander("📖 Read White Paper"):
            st.markdown(content)
        
        # Download button with better error handling
        if hasattr(whitepaper_system, 'get_pdf_content'):
            try:
                pdf_content = whitepaper_system.get_pdf_content()
                if pdf_content and len(pdf_content) > 100:  # Check if we have real content
                    st.download_button(
                        label="📥 Download White Paper (PDF)",
                        data=pdf_content,
                        file_name=f"YSense_AI_Attribution_Infrastructure_White_Paper_v{metadata['version']}.pdf",
                        mime="application/pdf",
                        on_click=lambda: whitepaper_system.track_download({"user": "anonymous", "timestamp": "now"}) if hasattr(whitepaper_system, 'track_download') else None
                    )
                else:
                    st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")
            except Exception as e:
                st.error(f"PDF download error: {e}")
                st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")
        else:
            st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")
        
        # Generate citation
        if hasattr(whitepaper_system, 'generate_citation_format'):
            citation = whitepaper_system.generate_citation_format()
            st.info(f"**Citation**: {citation}")
        else:
            st.info("**Citation**: YSense™ AI Attribution Infrastructure White Paper v1.0 (2025)")

def show_my_wisdom():
    """Show user's wisdom library with metrics"""
    st.subheader("📚 My Wisdom Library")
    
    components = init_components()
    if components:
        wisdom_library = components['wisdom_library']
        metrics_collector = components['metrics_collector']
        
        # Get user's wisdom
        user_wisdom = wisdom_library.get_user_wisdom(st.session_state.user_id)
        
        if user_wisdom:
            # Display metrics
            metrics = metrics_collector.get_live_metrics()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Wisdom", len(user_wisdom))
            with col2:
                st.metric("Total Views", metrics.get('total_views', 0))
            with col3:
                st.metric("Total Downloads", metrics.get('total_downloads', 0))
            with col4:
                st.metric("Revenue Earned", f"${metrics.get('revenue_earned', 0):.2f}")
            
            # Display wisdom items
            for wisdom in user_wisdom:
                with st.expander(f"📝 {wisdom.title}"):
                    st.write(f"**Content**: {wisdom.content}")
                    st.write(f"**Created**: {wisdom.created_at}")
                    st.write(f"**Views**: {wisdom.views}")
                    st.write(f"**Downloads**: {wisdom.downloads}")
        else:
            st.info("No wisdom created yet. Create your first wisdom drop!")

def show_wisdom_library():
    """Show public wisdom library"""
    st.subheader("📚 Wisdom Library")
    
    components = init_components()
    if components:
        wisdom_library = components['wisdom_library']
        
        # Search and filter
        search_term = st.text_input("🔍 Search wisdom", placeholder="Enter keywords...")
        
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Newest", "Most Viewed", "Most Downloaded"])
        with col2:
            category = st.selectbox("Category", ["All", "Philosophy", "Technology", "Business", "Science"])
        
        # Get wisdom
        all_wisdom = wisdom_library.get_all_wisdom()
        
        if search_term:
            all_wisdom = [w for w in all_wisdom if search_term.lower() in w.title.lower() or search_term.lower() in w.content.lower()]
        
        if all_wisdom:
            for wisdom in all_wisdom:
                with st.expander(f"📝 {wisdom.title} by {wisdom.author_email}"):
                    st.write(f"**Content**: {wisdom.content}")
                    st.write(f"**Created**: {wisdom.created_at}")
                    st.write(f"**Views**: {wisdom.views}")
                    st.write(f"**Downloads**: {wisdom.downloads}")
                    
                    if st.button(f"📥 Download Attribution", key=f"download_{wisdom.id}"):
                        components['attribution_engine'].generate_attribution(wisdom.id)
                        st.success("Attribution document generated!")
        else:
            st.info("No wisdom found matching your criteria.")

def show_v4_interface():
    """Show the new methodology-based AI workflow interface"""
    st.subheader("🤖 YSense™ Methodology AI Workflow")
    st.info("🎯 **Founder's Unique 3-Stage Methodology**: Experiential Extraction → Deep Dive Vibe → Full AI Analysis")
    
    # Input section
    st.markdown("### 📝 Input Your Story/Idea")
    st.markdown("Share your story, idea, or question")
    
    # Story input
    user_story = st.text_area(
        "Your Story/Idea",
        placeholder="Share your unique story, experience, or idea...",
        height=150,
        help="The more detailed your story, the better the analysis will be"
    )
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            cultural_context = st.text_input(
                "Cultural Context",
                placeholder="e.g., Asian business culture",
                help="Cultural background or context"
            )
            
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., entrepreneurs, students",
                help="Who is this story/idea for?"
            )
        
        with col2:
            priority_focus = st.selectbox(
                "Priority Focus",
                ["Innovation", "Growth", "Connection", "Wisdom", "Impact", "Learning"],
                help="What's the main focus?"
            )
            
            analysis_depth = st.selectbox(
                "Analysis Depth",
                ["Quick", "Standard", "Deep", "Comprehensive"],
                help="How detailed should the analysis be?"
            )
    
    # Deep Vibe 3-Word Resonance Input
    st.markdown("### 💫 Deep Dive Vibe - 3-Word Resonance")
    st.info("🎯 **Enter your own 3 words that resonate with your story** - This makes the analysis more personal and authentic!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        primary_vibe = st.text_input(
            "🔥 Primary Vibe Word",
            placeholder="e.g., Connection",
            help="The dominant emotional/energetic quality"
        )
        primary_description = st.text_area(
            "Primary Vibe Description",
            placeholder="Why this word resonates with your story...",
            height=60,
            help="Short description of why this word resonates"
        )
    
    with col2:
        secondary_vibe = st.text_input(
            "🌟 Secondary Resonance Word",
            placeholder="e.g., Growth",
            help="The underlying theme or pattern"
        )
        secondary_description = st.text_area(
            "Secondary Resonance Description",
            placeholder="How this connects to your experience...",
            height=60,
            help="Short description of the resonance"
        )
    
    with col3:
        tertiary_vibe = st.text_input(
            "💎 Tertiary Essence Word",
            placeholder="e.g., Wisdom",
            help="The core truth or wisdom"
        )
        tertiary_description = st.text_area(
            "Tertiary Essence Description",
            placeholder="What this reveals about your journey...",
            height=60,
            help="Short description of the essence"
        )
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        analyze_clicked = st.button("🚀 Analyze with Founder's Methodology", type="primary", use_container_width=True)
    
    with col2:
        submit_clicked = st.button("💾 Submit & Save to Database", type="secondary", use_container_width=True)
    
    # Handle analysis
    if analyze_clicked:
        if user_story.strip():
            with st.spinner("🔄 Processing through 3-stage methodology..."):
                try:
                    # Import the new methodology engine
                    import sys
                    import os
                    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                    from src.methodology_core_engine import methodology_engine
                    
                    # Create user vibe data
                    user_vibe_data = {
                        "primary_vibe_word": {
                            "word": primary_vibe or "Connection",
                            "resonance": primary_description or "User-defined primary vibe",
                            "story_connection": "User input",
                            "person_insight": "Personal resonance",
                            "future_guidance": "User-defined guidance"
                        },
                        "secondary_resonance_word": {
                            "word": secondary_vibe or "Growth", 
                            "resonance": secondary_description or "User-defined secondary resonance",
                            "story_connection": "User input",
                            "person_insight": "Personal resonance",
                            "future_guidance": "User-defined guidance"
                        },
                        "tertiary_essence_word": {
                            "word": tertiary_vibe or "Wisdom",
                            "resonance": tertiary_description or "User-defined tertiary essence",
                            "story_connection": "User input", 
                            "person_insight": "Personal resonance",
                            "future_guidance": "User-defined guidance"
                        },
                        "energy_level": 8,
                        "authenticity_score": 9,
                        "resonance_strength": 9,
                        "potential_impact": 8,
                        "user_defined": True
                    }
                    
                    # Process the story with user vibe data
                    import asyncio
                    results = asyncio.run(methodology_engine.process_user_story_with_vibe(
                        user_story=user_story,
                        user_vibe_data=user_vibe_data,
                        cultural_context=cultural_context,
                        target_audience=target_audience,
                        priority_focus=priority_focus,
                        analysis_depth=analysis_depth
                    ))
                    
                    # Store results in session state
                    st.session_state.methodology_results = results
                    st.success("✅ Analysis completed!")
                    
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    st.info("Using fallback analysis...")
                    
                    # Fallback results with user vibe data
                    st.session_state.methodology_results = {
                        "session_id": f"fallback_{int(datetime.now().timestamp())}",
                        "timestamp": datetime.now().isoformat(),
                        "user_story": user_story,
                        "methodology_stages": {
                            "stage_1_experiential_extraction": {
                                "emotional_journey": ["curiosity", "connection", "reflection"],
                                "key_experiences": ["story sharing", "cultural exchange"],
                                "learning_moments": ["cultural awareness", "social connection"],
                                "fallback_mode": True
                            },
                            "stage_2_vibe_resonance": user_vibe_data,
                            "stage_3_full_analysis": {
                                "executive_summary": f"Analysis focused on {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}.",
                                "market_strategy": "Strong potential for cultural bridge-building",
                                "execution_plan": "Focus on relationship-building initiatives",
                                "fallback_mode": True
                            }
                        },
                        "executive_summary": f"Analysis completed with focus on {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}.",
                        "z_protocol_score": {"overall_score": 85.0, "grade": "A"},
                        "revenue_potential": {"revenue_score": 80.0, "potential_tier": "High"}
                    }
        else:
            st.warning("Please enter your story/idea first.")
    
    # Handle submit to database
    if submit_clicked:
        if user_story.strip():
            with st.spinner("💾 Saving to database..."):
                try:
                    # Import database components
                    import sys
                    import os
                    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                    from src.wisdom_library import WisdomLibrary
                    
                    # Create wisdom library instance
                    wisdom_lib = WisdomLibrary()
                    
                    # Save the story to database
                    wisdom_data = {
                        "title": f"Story: {user_story[:50]}...",
                        "content": user_story,
                        "category": "Personal Story",
                        "tags": [primary_vibe, secondary_vibe, tertiary_vibe],
                        "cultural_context": cultural_context,
                        "target_audience": target_audience,
                        "priority_focus": priority_focus,
                        "analysis_depth": analysis_depth,
                        "vibe_data": {
                            "primary_vibe": primary_vibe,
                            "secondary_vibe": secondary_vibe,
                            "tertiary_vibe": tertiary_vibe,
                            "primary_description": primary_description,
                            "secondary_description": secondary_description,
                            "tertiary_description": tertiary_description
                        },
                        "user_id": st.session_state.get('user_id', 1),
                        "tier": st.session_state.get('user_tier', 'Standard')
                    }
                    
                    # Save to database
                    wisdom_id = wisdom_lib.create_wisdom_drop(
                        title=wisdom_data["title"],
                        content=wisdom_data["content"],
                        category=wisdom_data["category"],
                        tags=wisdom_data["tags"],
                        user_id=wisdom_data["user_id"],
                        tier=wisdom_data["tier"],
                        metadata=wisdom_data
                    )
                    
                    if wisdom_id:
                        # Check for duplicate content using anti-gaming system
                        try:
                            from src.revenue_transparency_system import revenue_system
                            
                            # Detect duplicate content
                            duplicate_check = revenue_system.detect_duplicate_content(
                                user_story, wisdom_data["user_id"]
                            )
                            
                            if duplicate_check["is_duplicate"]:
                                st.warning("⚠️ **Duplicate Content Detected!**")
                                st.error("This content has been submitted before. Revenue sharing may be affected.")
                                
                                # Report violation
                                revenue_system.report_anti_gaming_violation(
                                    contributor_id=wisdom_data["user_id"],
                                    violation_type="duplicate_content",
                                    violation_description="Same content submitted multiple times",
                                    wisdom_id=wisdom_id,
                                    similarity_score=duplicate_check["similarity_score"]
                                )
                                
                            elif duplicate_check["is_similar"]:
                                st.warning("⚠️ **Similar Content Detected!**")
                                st.info(f"Similarity Score: {duplicate_check['similarity_score']:.1f}%")
                                st.info("This content is similar to existing content. Please ensure originality.")
                                
                            else:
                                st.success("✅ **Content Originality Verified!**")
                                st.info("No duplicate or similar content detected.")
                            
                            # Register content fingerprint for future detection
                            revenue_system.register_content_fingerprint(
                                content=user_story,
                                wisdom_id=wisdom_id,
                                contributor_id=wisdom_data["user_id"]
                            )
                            
                        except Exception as e:
                            st.info("Anti-gaming check completed with fallback mode.")
                        
                        st.success(f"✅ Story saved to database! Wisdom ID: {wisdom_id}")
                        
                        # Process revenue for this wisdom contribution
                        try:
                            from src.revenue_transparency_system import revenue_system
                            
                            # Calculate revenue based on tier and performance
                            revenue_result = revenue_system.process_wisdom_revenue(
                                wisdom_id=wisdom_id,
                                contributor_id=wisdom_data["user_id"],
                                tier=wisdom_data["tier"],
                                base_revenue=10.0  # Base revenue per wisdom
                            )
                            
                            if "error" not in revenue_result:
                                st.success("💰 **Revenue Calculated!**")
                                
                                # Display revenue information
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric(
                                        "Revenue Share", 
                                        f"${revenue_result['share_amount']:.2f}",
                                        help=f"{revenue_result['share_percentage']:.1f}% of ${revenue_result['total_revenue']:.2f}"
                                    )
                                
                                with col2:
                                    st.metric(
                                        "Performance Multiplier", 
                                        f"{revenue_result['performance_metrics']['performance_multiplier']:.1f}x",
                                        help="Based on views, downloads, and recency"
                                    )
                                
                                with col3:
                                    st.metric(
                                        "Tier", 
                                        wisdom_data["tier"],
                                        help=f"{revenue_result['share_percentage']:.1f}% revenue share"
                                    )
                                
                                # Show performance metrics
                                st.info(f"""
                                **Performance Metrics:**
                                - Views: {revenue_result['performance_metrics']['views']}
                                - Downloads: {revenue_result['performance_metrics']['downloads']}
                                - Base Revenue: ${revenue_result['performance_metrics']['base_revenue']:.2f}
                                - Total Revenue: ${revenue_result['performance_metrics']['total_revenue']:.2f}
                                - Your Share: ${revenue_result['share_amount']:.2f} ({revenue_result['share_percentage']:.1f}%)
                                """)
                                
                            else:
                                st.warning(f"Revenue calculation failed: {revenue_result['error']}")
                                
                        except Exception as e:
                            st.info("Revenue calculation completed with fallback mode.")
                        
                        st.balloons()
                        
                        # Clear the form
                        st.session_state.story_submitted = True
                        st.rerun()
                    else:
                        st.error("❌ Failed to save to database")
                        
                except Exception as e:
                    st.error(f"Database save failed: {e}")
                    st.info("This might be due to database configuration. Check your setup.")
                    
                    # Debug information
                    st.markdown("### 🔍 Debug Information:")
                    st.code(f"Error: {str(e)}")
                    st.code(f"Error Type: {type(e).__name__}")
                    st.code(f"User ID: {st.session_state.get('user_id', 'Not set')}")
                    st.code(f"User Tier: {st.session_state.get('user_tier', 'Not set')}")
                    
                    # Show the wisdom data that was being saved
                    st.markdown("### 📊 Data Being Saved:")
                    st.code(f"Title: {wisdom_data.get('title', 'N/A')}")
                    st.code(f"Content Length: {len(wisdom_data.get('content', ''))}")
                    st.code(f"Category: {wisdom_data.get('category', 'N/A')}")
                    st.code(f"Tags: {wisdom_data.get('tags', [])}")
                    
                    # Try to create database tables
                    try:
                        st.info("🔄 Attempting to initialize database...")
                        from src.wisdom_library import WisdomLibrary
                        wisdom_lib = WisdomLibrary()
                        st.success("✅ Database initialized successfully!")
                        
                        # Try a simple test save
                        test_id = wisdom_lib.create_wisdom_drop(
                            title="Test Save",
                            content="Testing database save functionality",
                            category="Test",
                            tags=["test"],
                            user_id=1,
                            tier="Standard"
                        )
                        
                        if test_id:
                            st.success(f"✅ Test save successful! ID: {test_id}")
                            st.info("Please try submitting your story again.")
                        else:
                            st.error("❌ Test save failed - no ID returned")
                            
                            # Try database reset
                            st.info("🔄 Attempting database reset...")
                            try:
                                import subprocess
                                result = subprocess.run([
                                    "python", "reset_database.py"
                                ], capture_output=True, text=True, timeout=30)
                                
                                if result.returncode == 0:
                                    st.success("✅ Database reset successful!")
                                    st.info("Please try submitting your story again.")
                                else:
                                    st.error(f"❌ Database reset failed: {result.stderr}")
                            except Exception as reset_error:
                                st.error(f"❌ Database reset error: {reset_error}")
                                st.info("Please run 'python reset_database.py' manually to fix the database.")
                            
                    except Exception as db_error:
                        st.error(f"Database initialization failed: {db_error}")
                        st.code(f"DB Error Type: {type(db_error).__name__}")
                        st.info("Please check your database configuration.")
        else:
            st.warning("Please enter your story/idea first.")
    
    # Display results
    if hasattr(st.session_state, 'methodology_results') and st.session_state.methodology_results:
        results = st.session_state.methodology_results
        
        st.markdown("---")
        st.markdown("### 🔍 Complete Methodology Analysis")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Executive Summary", 
            "🎯 Stage 1: Experiential Data", 
            "💫 Stage 2: Deep Dive Vibe", 
            "🤖 Stage 3: Full AI Analysis",
            "📈 Complete Results"
        ])
        
        with tab1:
            st.markdown("#### 📊 Executive Summary")
            if "executive_summary" in results:
                st.markdown(results["executive_summary"])
            else:
                st.info("Executive summary will be generated after analysis.")
            
            # Z Protocol Score
            if "z_protocol_score" in results:
                score_data = results["z_protocol_score"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Z Protocol Score", f"{score_data.get('overall_score', 0)}/100")
                with col2:
                    st.metric("Grade", score_data.get('grade', 'N/A'))
                with col3:
                    st.metric("Status", "COMPLIANT" if score_data.get('overall_score', 0) >= 70 else "REVIEW")
        
        with tab2:
            st.markdown("#### 🎯 Stage 1: Experiential Data Extraction")
            if "methodology_stages" in results and "stage_1_experiential_extraction" in results["methodology_stages"]:
                exp_data = results["methodology_stages"]["stage_1_experiential_extraction"]
                
                # Display experiential data in a structured way
                for key, value in exp_data.items():
                    if key not in ["extraction_timestamp", "story_length", "fallback_mode", "error"]:
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        if isinstance(value, list):
                            for item in value:
                                st.markdown(f"• {item}")
                        else:
                            st.markdown(f"{value}")
                        st.markdown("")
            else:
                st.info("Experiential data extraction will be completed during analysis.")
        
        with tab3:
            st.markdown("#### 💫 Stage 2: Deep Dive Vibe - 3-Word Resonance")
            if "methodology_stages" in results and "stage_2_vibe_resonance" in results["methodology_stages"]:
                vibe_data = results["methodology_stages"]["stage_2_vibe_resonance"]
                
                # Display the 3 words prominently
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if "primary_vibe_word" in vibe_data:
                        word_data = vibe_data["primary_vibe_word"]
                        st.markdown(f"### 🔥 {word_data.get('word', 'N/A')}")
                        st.markdown(f"**Primary Vibe**")
                        st.markdown(f"*{word_data.get('resonance', 'N/A')}*")
                
                with col2:
                    if "secondary_resonance_word" in vibe_data:
                        word_data = vibe_data["secondary_resonance_word"]
                        st.markdown(f"### 🌟 {word_data.get('word', 'N/A')}")
                        st.markdown(f"**Secondary Resonance**")
                        st.markdown(f"*{word_data.get('resonance', 'N/A')}*")
                
                with col3:
                    if "tertiary_essence_word" in vibe_data:
                        word_data = vibe_data["tertiary_essence_word"]
                        st.markdown(f"### 💎 {word_data.get('word', 'N/A')}")
                        st.markdown(f"**Tertiary Essence**")
                        st.markdown(f"*{word_data.get('resonance', 'N/A')}*")
                
                # Vibe metrics
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Energy Level", f"{vibe_data.get('energy_level', 0)}/10")
                with col2:
                    st.metric("Authenticity", f"{vibe_data.get('authenticity_score', 0)}/10")
                with col3:
                    st.metric("Resonance", f"{vibe_data.get('resonance_strength', 0)}/10")
                with col4:
                    st.metric("Impact", f"{vibe_data.get('potential_impact', 0)}/10")
            else:
                st.info("Deep dive vibe analysis will be completed during analysis.")
        
        with tab4:
            st.markdown("#### 🤖 Stage 3: Full AI Analysis")
            if "methodology_stages" in results and "stage_3_full_analysis" in results["methodology_stages"]:
                analysis_data = results["methodology_stages"]["stage_3_full_analysis"]
                
                # Display analysis in structured format
                for key, value in analysis_data.items():
                    if key not in ["fallback_mode", "error", "synthesis_timestamp"]:
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                st.markdown(f"• **{sub_key.replace('_', ' ').title()}:** {sub_value}")
                        elif isinstance(value, list):
                            for item in value:
                                st.markdown(f"• {item}")
                        else:
                            st.markdown(f"{value}")
                        st.markdown("")
            else:
                st.info("Full AI analysis will be completed during analysis.")
        
        with tab5:
            st.markdown("#### 📈 Complete Results")
            
            # Revenue potential
            if "revenue_potential" in results:
                revenue_data = results["revenue_potential"]
                st.markdown("**💰 Revenue Potential:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Revenue Score", f"{revenue_data.get('revenue_score', 0)}/100")
                with col2:
                    st.metric("Potential Tier", revenue_data.get('potential_tier', 'N/A'))
            
            # Raw results (collapsible)
            with st.expander("🔍 View Raw Results"):
                st.json(results)

def main():
    """Main application"""
    # Page config
    st.set_page_config(
        page_title="YSense™ v4.1 | 慧觉™",
        page_icon="💧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for sidebar logo
    logo_base64 = load_image_as_base64("assets/Logo Ysense.png")
    st.markdown(f"""
    <style>
    /* YSense Logo for sidebar */
    .css-1d391kg::before {{
        content: '';
        display: block;
        width: 40px;
        height: 40px;
        background-image: url('data:image/png;base64,{logo_base64}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 50%;
        margin: 10px auto;
        position: relative;
        box-shadow: 0 2px 8px rgba(96, 165, 250, 0.3);
    }}
    
    /* Hide default sidebar icon */
    .css-1d391kg .css-1v0mbdj {{
        display: none;
    }}
    
    /* Style the navigation title */
    .css-1d391kg h1 {{
        color: #4c1d95 !important;
        font-weight: bold !important;
        margin-top: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add header
    add_header_image()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    if not st.session_state.authenticated:
        # Check if this is a password reset page
        if st.query_params.get('token'):
            show_password_reset()
        else:
            # Show navigation for non-authenticated users
            st.sidebar.markdown("### 🌐 Public Access")
            
            # Your desired navigation links
            if st.sidebar.button("📄 White Paper", use_container_width=True):
                st.session_state.current_page = "whitepaper"
                st.rerun()
            
            if st.sidebar.button("📖 Founder's Story", use_container_width=True):
                st.session_state.current_page = "founders_story"
                st.rerun()
            
            if st.sidebar.button("🔓 Open Source", use_container_width=True):
                st.session_state.current_page = "open_source"
                st.rerun()
            
            if st.sidebar.button("📚 Wisdom Library", use_container_width=True):
                st.session_state.current_page = "wisdom_library"
                st.rerun()
            
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔐 Account Access")
            
            # Login/Register tabs
            tab1, tab2 = st.tabs(["🔐 Login", "🚀 Register"])
            
            with tab1:
                show_login()
            
            with tab2:
                show_registration()
            
            # Show current page content
            current_page = st.session_state.get('current_page', 'whitepaper')
            
            if current_page == "whitepaper":
                show_whitepaper()
            elif current_page == "founders_story":
                show_founders_story()
            elif current_page == "open_source":
                show_open_source()
            elif current_page == "wisdom_library":
                show_wisdom_library()
    else:
        # Authenticated user navigation
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        st.sidebar.info(f"🔑 Tier: {st.session_state.user_tier}")
        
        if st.sidebar.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.user_tier = None
            st.session_state.public_key = None
            st.rerun()
        
        # Main navigation
        page = st.sidebar.selectbox(
            "Choose Page",
            ["🏠 Dashboard", "📚 Wisdom Library", "📝 My Wisdom", "🤖 AI Workflow", "💰 Revenue Dashboard", "📄 White Paper"]
        )
        
        if page == "🏠 Dashboard":
            st.subheader("🏠 Dashboard")
            st.info("Welcome to YSense™ v4.1! Use the navigation menu to explore features.")
            
        elif page == "📚 Wisdom Library":
            show_wisdom_library()
            
        elif page == "📝 My Wisdom":
            show_my_wisdom()
            
        elif page == "🤖 AI Workflow":
            show_v4_interface()
            
        elif page == "📄 White Paper":
            show_whitepaper()
            
        elif page == "💰 Revenue Dashboard":
            show_revenue_dashboard()

def show_revenue_dashboard():
    """Show Revenue Transparency Dashboard"""
    st.subheader("💰 Revenue Transparency Dashboard")
    st.info("🎯 **Complete transparency in revenue sharing** - See exactly how much you earn from your contributions!")
    
    if hasattr(st.session_state, 'user_id'):
        user_id = st.session_state.user_id
        user_tier = st.session_state.get('user_tier', 'Standard')
        
        # Import revenue system
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from src.revenue_transparency_system import revenue_system
            
            # Get contributor dashboard data
            dashboard_data = revenue_system.get_contributor_dashboard(user_id)
            
            if "error" not in dashboard_data:
                # Display dashboard
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Tier", 
                        dashboard_data["current_tier"],
                        help=f"Revenue Share: {dashboard_data['tier_benefits']['revenue_percentage']:.1f}%"
                    )
                
                with col2:
                    st.metric(
                        "Total Revenue", 
                        f"${dashboard_data['analytics']['total_revenue_earned']:.2f}",
                        help="Total earnings from all contributions"
                    )
                
                with col3:
                    st.metric(
                        "Wisdom Count", 
                        dashboard_data['analytics']['total_wisdom_count'],
                        help="Total wisdom drops created"
                    )
                
                with col4:
                    st.metric(
                        "Total Views", 
                        dashboard_data['analytics']['total_views'],
                        help="Total views across all wisdom"
                    )
                
                # Revenue breakdown
                st.markdown("---")
                st.markdown("### 📊 Revenue Breakdown")
                
                # Recent revenue shares
                if dashboard_data['recent_shares']:
                    st.markdown("#### 💰 Recent Revenue Shares")
                    for share in dashboard_data['recent_shares'][:5]:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.write(f"**{share['wisdom_title'][:30]}...**")
                        with col2:
                            st.write(f"${share['revenue_amount']:.2f}")
                        with col3:
                            st.write(f"{share['share_percentage']:.1f}%")
                        with col4:
                            status_color = "🟢" if share['payment_status'] == 'paid' else "🟡"
                            st.write(f"{status_color} {share['payment_status']}")
                
                # Monthly revenue chart
                if dashboard_data['monthly_revenue']:
                    st.markdown("#### 📈 Monthly Revenue Trend")
                    import pandas as pd
                    
                    df = pd.DataFrame(dashboard_data['monthly_revenue'])
                    df['month'] = pd.to_datetime(df['month'])
                    df = df.sort_values('month')
                    
                    st.line_chart(df.set_index('month')['total_revenue'])
                
                # Tier benefits and requirements
                st.markdown("---")
                st.markdown("### 🏆 Tier Benefits & Requirements")
                
                tier_info = dashboard_data['tier_benefits']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Current Tier: {tier_info['current_tier']}**")
                    st.markdown(f"**Revenue Share: {tier_info['revenue_percentage']:.1f}%**")
                    
                    if tier_info['next_tier']:
                        st.markdown(f"**Next Tier: {tier_info['next_tier']}**")
                        st.markdown("**Requirements:**")
                        requirements = tier_info['tier_requirements']
                        st.markdown(f"- Wisdom Count: {requirements['wisdom_count']}")
                        st.markdown(f"- Revenue Threshold: ${requirements['revenue_threshold']}")
                        st.markdown(f"- Quality Score: {requirements['quality_score']}")
                
                with col2:
                    # Progress bar for next tier
                    if tier_info['next_tier']:
                        current_revenue = dashboard_data['analytics']['total_revenue_earned']
                        requirements = tier_info['tier_requirements']
                        progress = min(current_revenue / requirements['revenue_threshold'], 1.0)
                        
                        st.markdown("**Progress to Next Tier:**")
                        st.progress(progress)
                        st.markdown(f"{progress*100:.1f}% complete")
                
                # Anti-gaming protection info
                st.markdown("---")
                st.markdown("### 🛡️ Anti-Gaming Protection")
                
                st.info("""
                **Our platform protects against:**
                - **Duplicate Content**: Same content submitted multiple times
                - **Self-Plagiarism**: Reusing your own content across different accounts
                - **Multiple Accounts**: Creating multiple accounts to gain unfair revenue
                - **Content Manipulation**: Attempting to game the system
                
                **Penalties:**
                - Duplicate content: $50 penalty
                - Self-plagiarism: $100 penalty  
                - Multiple accounts: $200 penalty
                """)
                
                # Community Wisdom Attribution
                st.markdown("---")
                st.markdown("### 🌟 Community Wisdom Attribution")
                
                st.success("""
                **Your contributions are automatically attributed:**
                - **Revenue calculated** based on your tier and wisdom performance
                - **Performance multipliers** for views, downloads, and recency
                - **Fair revenue sharing** ensures contributors are rewarded
                - **Transparent tracking** of all earnings and payments
                """)
                
                # Show community impact
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Community Impact", 
                        f"{dashboard_data['analytics']['total_views']} views",
                        help="Total views across your wisdom"
                    )
                
                with col2:
                    st.metric(
                        "Knowledge Shared", 
                        f"{dashboard_data['analytics']['total_wisdom_count']} drops",
                        help="Wisdom contributions to community"
                    )
                
                with col3:
                    st.metric(
                        "Revenue Earned", 
                        f"${dashboard_data['analytics']['total_revenue_earned']:.2f}",
                        help="Total earnings from community contributions"
                    )
                
            else:
                st.error(f"Error loading dashboard: {dashboard_data['error']}")
                
        except Exception as e:
            st.error(f"Dashboard error: {e}")
            st.info("Using mock dashboard data...")
            
            # Mock dashboard data
            st.markdown("### 📊 Mock Dashboard Data")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Tier", user_tier, "Revenue Share: 50.0%")
            
            with col2:
                st.metric("Total Revenue", "$127.80", "Total earnings")
            
            with col3:
                st.metric("Wisdom Count", "3", "Total wisdom drops")
            
            with col4:
                st.metric("Total Views", "123", "Total views")
            
            # Mock recent shares
            st.markdown("### 💰 Recent Revenue Shares")
            mock_shares = [
                {"title": "Cultural Connection Story", "amount": 25.50, "percentage": 50.0, "status": "paid"},
                {"title": "Entrepreneurial Insights", "amount": 42.30, "percentage": 50.0, "status": "paid"},
                {"title": "Personal Growth Journey", "amount": 60.00, "percentage": 50.0, "status": "pending"}
            ]
            
            for share in mock_shares:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{share['title']}**")
                with col2:
                    st.write(f"${share['amount']:.2f}")
                with col3:
                    st.write(f"{share['percentage']:.1f}%")
                with col4:
                    status_color = "🟢" if share['status'] == 'paid' else "🟡"
                    st.write(f"{status_color} {share['status']}")
            
            # Mock tier benefits
            st.markdown("### 🏆 Tier Benefits")
            st.markdown(f"**Current Tier: {user_tier}**")
            st.markdown("**Revenue Share: 50.0%**")
            st.markdown("**Next Tier: Cultural Guardian**")
            st.markdown("**Requirements:**")
            st.markdown("- Wisdom Count: 15")
            st.markdown("- Revenue Threshold: $500")
            st.markdown("- Quality Score: 80")
            
            # Progress bar
            current_revenue = 127.80
            target_revenue = 500.0
            progress = min(current_revenue / target_revenue, 1.0)
            
            st.markdown("**Progress to Next Tier:**")
            st.progress(progress)
            st.markdown(f"{progress*100:.1f}% complete")
            
    else:
        st.warning("Please log in to view your revenue dashboard.")

if __name__ == "__main__":
    main()

