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

# Import our modules - MINIMAL VERSION
# try:
#     from src.models import User, WisdomDrop, create_tables
#     from src.auth import AuthManager
#     from src.wisdom_library import WisdomLibrary
#     from src.attribution_engine import AttributionEngine
#     from src.revenue_models import RevenueModel, ContributorTier
#     from src.terms_consent_system import TermsConsentSystem
#     from src.whitepaper_system import WhitePaperSystem
#     from src.agent_system_v41 import AgentSystem
#     from src.metrics_collector import MetricsCollector
# except ImportError as e:
#     st.error(f"Import error: {e}")
#     st.stop()

# MINIMAL WORKING VERSION - NO IMPORTS FROM SRC

# ========== PROTOTYPE MODE IMPORTS ==========
from src.prototype_mode import prototype_mode
from src.prototype_privacy_policy import prototype_privacy
# ============================================

# Page Configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="YSense™ v4.1 | 慧觉™",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look with Mobile Responsiveness
st.markdown("""
<style>
    /* Base app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }

    /* Status card styling */
    .status-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        text-align: center;
    }

    /* Mobile responsiveness - tablets and smaller */
    @media (max-width: 768px) {
        /* Adjust main container padding */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }

        /* Adjust header sizes */
        h1 {
            font-size: 1.5rem !important;
        }

        h2 {
            font-size: 1.3rem !important;
        }

        h3 {
            font-size: 1.1rem !important;
        }

        /* Make buttons full width on mobile */
        .stButton > button {
            width: 100% !important;
        }

        /* Adjust expander styling */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
        }

        /* Adjust text input sizes */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-size: 0.9rem !important;
        }

        /* Adjust select boxes */
        .stSelectbox {
            font-size: 0.9rem !important;
        }

        /* Reduce padding on cards */
        .status-card {
            padding: 1rem !important;
        }

        /* Sidebar adjustments */
        [data-testid="stSidebar"] {
            width: 250px !important;
        }

        /* Columns stack on mobile */
        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }

    /* Mobile responsiveness - phones only */
    @media (max-width: 480px) {
        /* Further reduce font sizes */
        h1 {
            font-size: 1.2rem !important;
        }

        h2 {
            font-size: 1.1rem !important;
        }

        h3 {
            font-size: 1rem !important;
        }

        /* Tighter padding */
        .main .block-container {
            padding: 0.5rem 0.25rem !important;
        }

        /* Smaller metrics */
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }

        /* Adjust sidebar for small screens */
        [data-testid="stSidebar"] {
            width: 200px !important;
        }
    }

    /* Ensure content doesn't overflow */
    * {
        max-width: 100%;
        box-sizing: border-box;
    }

    /* Make images responsive */
    img {
        max-width: 100%;
        height: auto;
    }

    /* Adjust dataframe/table display */
    .dataframe {
        font-size: 0.8rem !important;
        overflow-x: auto !important;
    }
</style>

<!-- Viewport meta tag for proper mobile scaling -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>💧 YSense™ Platform v4.1 Fresh</h1>
    <h2>慧觉™ - AI Attribution Infrastructure</h2>
    <p>Human-AI Collaboration Platform</p>
</div>
""", unsafe_allow_html=True)

# Status Card
st.markdown("""
<div class="status-card">
    <h3>🚀 Deployment Status</h3>
    <p><strong>Status:</strong> ✅ Successfully Deployed</p>
    <p><strong>Platform:</strong> Google Cloud Run</p>
    <p><strong>Region:</strong> asia-southeast1 (Singapore)</p>
    <p><strong>Deployed:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """</p>
</div>
""", unsafe_allow_html=True)

# Coming Soon Section
st.markdown("""
<div class="status-card">
    <h2>🎯 Coming Soon</h2>
    <p>We're building something amazing! The YSense™ Platform v4.1 Fresh is currently in development.</p>
    <p>This minimal version confirms our Cloud Run deployment is working perfectly.</p>
</div>
""", unsafe_allow_html=True)

# Feature Preview
st.markdown("### 🔮 Planned Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🧠 AI Wisdom Collection**
    - Advanced AI model integration
    - Real-time wisdom processing
    - Intelligent content analysis
    """)

with col2:
    st.markdown("""
    **👥 User Management**
    - Secure authentication system
    - User profile management
    - Role-based access control
    """)

with col3:
    st.markdown("""
    **📊 Analytics Dashboard**
    - Real-time metrics
    - Performance insights
    - Revenue tracking
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>YSense™ Platform v4.1 Fresh | Built with ❤️ for Human-AI Collaboration</p>
    <p>Powered by Google Cloud Run | Streamlit Framework</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Platform Status")
    st.success("✅ Cloud Run Deployed")
    st.info("🔄 Development Active")
    st.warning("⚠️ Features Coming Soon")
    
    st.markdown("### 📈 Quick Stats")
    st.metric("Deployment Status", "Success", "100%")
    st.metric("Uptime", "Active", "0 downtime")
    st.metric("Version", "v4.1-minimal", "Initial")
    
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub Repository](https://github.com/ysense-ai/ysense-core)")
    st.markdown("[Documentation](https://docs.ysense.ai)")
    st.markdown("[Support](mailto:support@ysense.ai)")

# Placeholder for future initialization
# When full frontend is enabled, components will be initialized here

def init_components():
    """Initialize components - stub function for minimal mode"""
    # Returns None in minimal mode
    # When full frontend is enabled, this will initialize actual components
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
    """Add the professional header with logo and Human-AI collaboration banner"""
    try:
        import streamlit.components.v1 as components

        # Load images
        logo_base64 = load_image_as_base64("assets/Logo Ysense.png")
        collaboration_base64 = load_image_as_base64("assets/Human-AI collaboration.jpg")

        # Debug: Check if images loaded
        if not logo_base64:
            st.warning("Logo image not found")
        if not collaboration_base64:
            st.warning("Collaboration image not found")

        # Build background image HTML only if image loaded
        background_html = ""
        if collaboration_base64:
            background_html = f"""
            <!-- Human-AI Collaboration Background -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; opacity: 0.45; display: flex; justify-content: center; align-items: center;">
                <img src="data:image/jpeg;base64,{collaboration_base64}"
                     style="width: 100%; height: 100%; object-fit: cover; filter: brightness(1.1) contrast(1.1);"
                     alt="Human-AI Collaboration"
                     onerror="console.error('Failed to load collaboration image')"/>
            </div>"""

        header_html = f"""
        <div style="position: relative;
                    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e3a8a 100%);
                    padding: 1.5rem 2rem; margin: -1rem -1rem 2rem -1rem;
                    text-align: center; color: white;
                    border-radius: 0 0 20px 20px;
                    overflow: hidden;
                    min-height: 180px;
                    width: 100vw;
                    margin-left: calc(-50vw + 50%);
                    margin-right: calc(-50vw + 50%);
                    box-shadow: 0 8px 24px rgba(0,0,0,0.3);">

            <!-- Animated Background Pattern -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; opacity: 0.05;">
                <div style="background-image: repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,255,255,.1) 35px, rgba(255,255,255,.1) 70px); width: 100%; height: 100%;"></div>
            </div>

            {background_html}

            <!-- Overlay gradient for depth -->
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                        background: linear-gradient(135deg, rgba(30, 27, 75, 0.65) 0%, rgba(30, 58, 138, 0.65) 100%);
                        z-index: 3;"></div>

            <!-- Logo Area (only show if logo loaded) -->
            {'<div style="position: absolute; left: 2rem; top: 50%; transform: translateY(-50%); z-index: 10;"><img src="data:image/png;base64,' + logo_base64 + '" width="70" height="70" style="border-radius: 50%; box-shadow: 0 6px 20px rgba(0,0,0,0.4); border: 2px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);" alt="YSense Logo"/></div>' if logo_base64 else ''}

            <!-- Main Content -->
            <div style="position: relative; z-index: 15; padding: 0 110px;">
                <!-- Main Title -->
                <div style="margin-bottom: 0.8rem;">
                    <h1 style="margin: 0;
                               font-size: 2.2em;
                               font-weight: 700;
                               letter-spacing: -0.5px;
                               background: linear-gradient(90deg, #ffffff 0%, #e0e7ff 100%);
                               -webkit-background-clip: text;
                               -webkit-text-fill-color: transparent;
                               background-clip: text;
                               text-shadow: 0 2px 8px rgba(0,0,0,0.3);
                               line-height: 1.2;">
                        YSense™ v4.1 | 慧觉™
                    </h1>
                </div>

                <!-- Subtitle -->
                <p style="margin: 0 auto 1rem auto;
                          font-size: 1.05em;
                          opacity: 0.92;
                          font-weight: 500;
                          max-width: 700px;
                          line-height: 1.4;
                          text-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                    AI Attribution Infrastructure: The Genesis of Human-AI Wisdom Collaboration
                </p>

                <!-- Feature Pills -->
                <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
                    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(99, 102, 241, 0.3) 100%);
                                padding: 0.5rem 1rem;
                                border-radius: 20px;
                                backdrop-filter: blur(10px);
                                border: 1.5px solid rgba(255,255,255,0.25);
                                box-shadow: 0 3px 12px rgba(0,0,0,0.2);">
                        <span style="font-size: 0.85em; font-weight: 600;">🤖 AI Analysis</span>
                    </div>
                    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(168, 85, 247, 0.3) 100%);
                                padding: 0.5rem 1rem;
                                border-radius: 20px;
                                backdrop-filter: blur(10px);
                                border: 1.5px solid rgba(255,255,255,0.25);
                                box-shadow: 0 3px 12px rgba(0,0,0,0.2);">
                        <span style="font-size: 0.85em; font-weight: 600;">📚 Attribution</span>
                    </div>
                    <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(239, 68, 68, 0.3) 100%);
                                padding: 0.5rem 1rem;
                                border-radius: 20px;
                                backdrop-filter: blur(10px);
                                border: 1.5px solid rgba(255,255,255,0.25);
                                box-shadow: 0 3px 12px rgba(0,0,0,0.2);">
                        <span style="font-size: 0.85em; font-weight: 600;">⚖️ Z Protocol v2.0</span>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(header_html, height=180)

    except Exception as e:
        st.error(f"Error loading header: {e}")

def show_terms_and_consent():
    """Show comprehensive Terms of Service and Consent page"""
    st.subheader("📜 Terms of Service & Consent")
    st.markdown("**Please read carefully before registration**")
    st.markdown("---")

    try:
        from src.terms_consent_system import TermsConsentSystem

        terms_system = TermsConsentSystem()

        # Display tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Terms of Service", "✅ Required Consents", "🎯 Revenue Model", "📜 Generate Certificate"])

        with tab1:
            st.markdown("### Complete Terms of Service")
            terms = terms_system.get_complete_terms_of_service()
            st.text_area("Terms of Service (Scroll to Read All)", terms, height=500, label_visibility="collapsed")

            st.download_button(
                label="📥 Download Terms of Service (TXT)",
                data=terms,
                file_name=f"YSense_Terms_of_Service_v{terms_system.version}.txt",
                mime="text/plain"
            )

        with tab2:
            st.markdown("### Required Consent Checkboxes")
            st.info("⚠️ All checkboxes must be accepted to proceed with registration")

            required_consents = terms_system.get_required_consents()

            # Store consent states
            if 'consent_states' not in st.session_state:
                st.session_state.consent_states = {}

            # Display each required consent
            for consent_id, consent_info in required_consents.items():
                if consent_info['required']:
                    st.session_state.consent_states[consent_id] = st.checkbox(
                        consent_info['label'],
                        value=st.session_state.consent_states.get(consent_id, False),
                        key=f"consent_{consent_id}",
                        help=consent_info['description']
                    )

            # Optional consents
            st.markdown("---")
            st.markdown("### Optional Consents")
            for consent_id, consent_info in required_consents.items():
                if not consent_info['required']:
                    st.session_state.consent_states[consent_id] = st.checkbox(
                        consent_info['label'],
                        value=st.session_state.consent_states.get(consent_id, False),
                        key=f"consent_opt_{consent_id}",
                        help=consent_info['description']
                    )

            # Validate consents
            st.markdown("---")
            if st.button("✅ Validate My Consents", type="primary"):
                validation = terms_system.validate_all_consents(st.session_state.consent_states)
                if validation['valid']:
                    st.success("✅ All required consents accepted! You may proceed with registration.")
                    st.session_state.consents_validated = True
                    st.session_state.consent_signature = validation['consent_signature']
                else:
                    st.error(f"❌ {validation['message']}")
                    st.warning("Please accept all required consents to continue.")

        with tab3:
            st.markdown("### Platform Vision & Values")
            st.warning("⚠️ **Important**: This platform is in early development. No revenue generation or payments are currently operational.")
            st.markdown("""
            #### 🎯 Current Stage: Early Development

            **What This Means:**
            - Platform is experimental and under active development
            - No financial compensation is offered at this time
            - Early contributors help shape the platform's future
            - Attribution systems are being tested and refined
            - No revenue promises or guarantees

            #### 🌟 Why Participate Now?

            **Be Part of Something Revolutionary:**
            - Help build the first ethical AI attribution platform
            - Shape how human wisdom is credited in AI training
            - Contribute to establishing new industry standards
            - Provide feedback that influences platform development
            - Early access to attribution and ethical AI frameworks

            #### 🛡️ Platform Core Values

            **Attribution & Ethics:**
            - Permanent attribution of your contributions
            - Respect for cultural and traditional knowledge
            - Ethical AI development principles (Z Protocol v2.0)
            - Transparency in all platform operations
            - Community-driven development

            #### 🔮 Future Possibilities (No Guarantees)

            **IF the platform succeeds:**
            - Revenue sharing models MAY be introduced
            - Early contributors MAY receive priority consideration
            - Cultural knowledge MAY receive special recognition
            - Partnership opportunities MAY become available

            **⚠️ These are aspirational goals, not commitments.**
            Do not participate expecting financial returns.
            """)

        with tab4:
            st.markdown("### Generate Your Consent Certificate")
            st.info("📜 After accepting all terms, you can generate an attributed consent certificate for your records.")

            if st.session_state.get('consents_validated', False):
                st.success("✅ Consents validated - Ready to generate certificate")

                # User details for certificate
                col1, col2 = st.columns(2)
                with col1:
                    cert_username = st.text_input("Username", placeholder="your_username")
                with col2:
                    cert_email = st.text_input("Email", placeholder="your.email@example.com")

                # Remove tier selection - not relevant for early stage
                cert_tier = "Early Stage Contributor"

                if st.button("🎓 Generate My Consent Certificate", type="primary"):
                    if cert_username and cert_email:
                        user_data = {
                            "username": cert_username,
                            "email": cert_email,
                            "tier": cert_tier
                        }
                        certificate = terms_system.generate_consent_certificate(
                            user_data,
                            st.session_state.consent_signature
                        )

                        st.success("✅ Certificate Generated Successfully!")
                        st.text_area("Your Consent Certificate", certificate, height=600)

                        st.download_button(
                            label="📥 Download Certificate (TXT)",
                            data=certificate,
                            file_name=f"YSense_Consent_Certificate_{cert_username}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )

                        st.info("💡 **Save this certificate** for your records. It serves as legal proof of your consent and agreement.")
                    else:
                        st.warning("Please provide both username and email to generate certificate.")
            else:
                st.warning("⚠️ Please validate all consents in the 'Required Consents' tab first.")

    except Exception as e:
        st.error(f"Error loading terms system: {e}")
        st.info("Terms and Consent system is initializing. Please try again.")

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
    try:
        token = st.query_params.get('token', [''])[0]
    except:
        token = ''
    
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

def show_whitepaper():
    """Show YSense White Paper with TXT and PDF downloads"""
    st.subheader("📄 YSense™ AI Attribution Infrastructure White Paper")
    st.markdown("*The Revolutionary Solution to AI Training Ethics*")
    st.markdown("---")

    try:
        from src.whitepaper_system import WhitePaperSystem
        whitepaper_system = WhitePaperSystem()

        # Get metadata
        metadata = whitepaper_system.get_white_paper_metadata()
        stats = whitepaper_system.get_download_statistics()

        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👁️ Views", stats.get('total_views', 0))
        with col2:
            st.metric("📥 Downloads", stats.get('total_downloads', 0))
        with col3:
            st.metric("📄 Version", metadata.get('version', '1.0'))

        st.markdown("")

        # Get white paper text content
        content = whitepaper_system.get_whitepaper_abstract()

        # Display content in tabs
        tab1, tab2, tab3 = st.tabs(["📖 Read Online", "📥 Download TXT", "📥 Download PDF"])

        with tab1:
            st.markdown("### White Paper Summary")
            st.markdown(content)

            st.markdown("---")
            st.markdown("### Citation")
            citation = whitepaper_system.generate_citation_format()
            st.code(citation, language=None)

        with tab2:
            st.markdown("### Download White Paper as TXT")
            st.info("💡 Download the white paper summary in text format for easy reading offline.")

            # Create TXT version with proper formatting
            txt_content = f"""
YSENSE™ AI ATTRIBUTION INFRASTRUCTURE WHITE PAPER
Version {metadata.get('version', '1.0')}

{content}

═══════════════════════════════════════════════════════════════════════

CITATION:
{citation}

═══════════════════════════════════════════════════════════════════════

© 2025 YSense™ Platform. All Rights Reserved.
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            st.download_button(
                label="📥 Download White Paper Summary (TXT)",
                data=txt_content,
                file_name=f"YSense_White_Paper_v{metadata.get('version', '1.0')}_Summary.txt",
                mime="text/plain",
                help="Download text summary of the white paper"
            )

            st.success("✅ Text version ready for download")

        with tab3:
            st.markdown("### Download Original White Paper PDF")
            st.info("📄 Download the complete white paper with full formatting and graphics.")

            # Try to get PDF
            pdf_summary = whitepaper_system.get_pdf_summary()

            if pdf_summary and pdf_summary.get('available'):
                st.success(f"✅ **PDF Available** - {pdf_summary.get('page_count')} pages, {pdf_summary.get('file_size_mb')} MB")

                try:
                    pdf_content = whitepaper_system.get_pdf_content()
                    if pdf_content and len(pdf_content) > 100:
                        st.download_button(
                            label=f"📥 Download Full White Paper (PDF) - {pdf_summary.get('file_size_mb')} MB",
                            data=pdf_content,
                            file_name=f"YSense_White_Paper_v{metadata.get('version', '1.0')}.pdf",
                            mime="application/pdf",
                            help="Download original PDF with full formatting"
                        )
                        st.success("✅ PDF ready for download")
                    else:
                        st.warning("⚠️ PDF file size issue. Please use TXT download or contact support.")
                except Exception as e:
                    st.error(f"PDF loading error: {e}")
                    st.warning("⚠️ PDF download temporarily unavailable. Please use TXT download above.")
            else:
                st.warning("⚠️ PDF version is being prepared. Please use TXT download above for now.")
                if pdf_summary:
                    st.info(f"Status: {pdf_summary.get('message', 'Processing...')}")

    except Exception as e:
        st.error(f"Error loading white paper: {e}")
        st.info("White paper system is initializing. Please try again in a moment.")

# OLD VERSION BELOW - Using init_components (doesn't work)
def show_whitepaper_OLD():
    """DEPRECATED - Old version using init_components"""
    components = init_components()
    if components:
        whitepaper_system = components['whitepaper_system']
        
        # Track view when page is accessed
        if hasattr(whitepaper_system, 'track_view'):
            whitepaper_system.track_view({"user": "anonymous", "timestamp": "now"})
        
        # Get metadata and statistics
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

        # Get PDF summary
        pdf_summary = None
        if hasattr(whitepaper_system, 'get_pdf_summary'):
            pdf_summary = whitepaper_system.get_pdf_summary()

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👁️ Views", stats.get('total_views', 0))
        with col2:
            st.metric("📥 Downloads", stats.get('total_downloads', 0))
        with col3:
            st.metric("📄 Version", metadata['version'])
        with col4:
            if pdf_summary and pdf_summary.get('available'):
                st.metric("📖 Pages", pdf_summary.get('page_count', 'N/A'))
            else:
                st.metric("⭐ Score", f"{metadata['credibility_score']}/10")

        # Display PDF summary if available
        if pdf_summary and pdf_summary.get('available'):
            st.success(f"✅ **PDF Available** - {pdf_summary.get('page_count')} pages, {pdf_summary.get('file_size_mb')} MB")

            # Show preview in expander
            if pdf_summary.get('preview'):
                with st.expander("👁️ Preview (First Page)"):
                    st.text(pdf_summary['preview'])

        # Get white paper content
        if hasattr(whitepaper_system, 'get_whitepaper_content'):
            content = whitepaper_system.get_whitepaper_content()
        elif hasattr(whitepaper_system, 'get_whitepaper_abstract'):
            content = whitepaper_system.get_whitepaper_abstract()
        else:
            content = "White paper content not available"

        # Display full content
        with st.expander("📖 Read Full White Paper", expanded=False):
            st.markdown(content)

        # Download button with counter tracking
        if hasattr(whitepaper_system, 'get_pdf_content'):
            try:
                pdf_content = whitepaper_system.get_pdf_content()
                if pdf_content and len(pdf_content) > 100:  # Check if we have real content
                    # Create a unique key for the download button
                    download_key = f"download_wp_{stats.get('total_downloads', 0)}"

                    # Track download in session state
                    if 'wp_download_clicked' not in st.session_state:
                        st.session_state.wp_download_clicked = False

                    def track_download():
                        if hasattr(whitepaper_system, 'track_download'):
                            result = whitepaper_system.track_download({
                                "user_id": st.session_state.get('username', 'anonymous'),
                                "user_type": "authenticated" if st.session_state.get('authenticated') else "public",
                                "timestamp": "now"
                            })
                            st.session_state.wp_download_clicked = True
                            return result

                    file_size = pdf_summary.get('file_size_mb', '2.8') if pdf_summary else '2.8'
                    st.download_button(
                        label=f"📥 Download White Paper (PDF) - {file_size} MB",
                        data=pdf_content,
                        file_name=f"YSense_AI_Attribution_Infrastructure_White_Paper_v{metadata['version']}.pdf",
                        mime="application/pdf",
                        key=download_key,
                        on_click=track_download
                    )

                    if st.session_state.get('wp_download_clicked'):
                        st.success("✅ Download tracked! Thank you for your interest.")
                else:
                    st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")
            except Exception as e:
                st.error(f"PDF download error: {e}")
                st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")
        else:
            st.info("📄 **View-Only Mode**: White paper is available for reading above. Views are tracked for analytics.")

        # Generate citation
        st.divider()
        st.subheader("📚 How to Cite")
        if hasattr(whitepaper_system, 'generate_citation_format'):
            citation = whitepaper_system.generate_citation_format()
            st.code(citation, language=None)
        else:
            st.code("YSense™ AI Attribution Infrastructure White Paper v1.0 (2025)", language=None)

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
    """Show public wisdom library in Substack-style format"""
    st.subheader("📚 Wisdom Library")
    st.markdown("*Stories and insights from the YSense community*")
    st.markdown("---")

    try:
        from src.wisdom_library import WisdomLibrary
        import json

        wisdom_library = WisdomLibrary()

        # User filter for authenticated users
        show_my_stories_only = False
        if st.session_state.get('authenticated', False):
            col_filter1, col_filter2 = st.columns([3, 1])
            with col_filter1:
                st.markdown("")  # Spacing
            with col_filter2:
                show_my_stories_only = st.checkbox("📝 My Stories Only", value=False)
            st.markdown("")

        # Search and filter section
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search stories", placeholder="Enter keywords...", label_visibility="collapsed")
        with col2:
            sort_by = st.selectbox("Sort", ["Newest First", "Most Viewed", "Most Downloaded"], label_visibility="collapsed")
        with col3:
            category = st.selectbox("Category", ["All Stories", "Personal Story", "Philosophy", "Technology", "Business", "Science"], label_visibility="collapsed")

        # Get all wisdom drops
        all_wisdom = wisdom_library.get_all_wisdom()

        # Filter by current user if checkbox is enabled
        if show_my_stories_only and st.session_state.get('authenticated', False):
            user_email = st.session_state.get('username', '') + '@ysenseai.org'
            all_wisdom = [w for w in all_wisdom if w.author_email == user_email]

        # Apply filters
        if category != "All Stories":
            all_wisdom = [w for w in all_wisdom if w.category == category.replace("All Stories", "")]

        if search_term:
            all_wisdom = [w for w in all_wisdom if search_term.lower() in w.title.lower() or search_term.lower() in w.content.lower()]

        # Apply sorting
        if sort_by == "Newest First":
            all_wisdom = sorted(all_wisdom, key=lambda x: x.created_at, reverse=True)
        elif sort_by == "Most Viewed":
            all_wisdom = sorted(all_wisdom, key=lambda x: x.views, reverse=True)
        elif sort_by == "Most Downloaded":
            all_wisdom = sorted(all_wisdom, key=lambda x: x.downloads, reverse=True)

        # Display count
        if show_my_stories_only:
            st.caption(f"📝 Your Stories: {len(all_wisdom)} {'story' if len(all_wisdom) == 1 else 'stories'}")
        else:
            st.caption(f"📖 {len(all_wisdom)} {'story' if len(all_wisdom) == 1 else 'stories'} found")
        st.markdown("")

        if all_wisdom:
            for wisdom in all_wisdom:
                # Parse tags
                try:
                    tags = json.loads(wisdom.tags) if isinstance(wisdom.tags, str) else wisdom.tags
                except:
                    tags = []

                # Clean title (remove "Story:" prefix if present)
                title = wisdom.title.replace("Story:", "").strip()
                # Truncate long titles
                if len(title) > 100:
                    title = title[:100] + "..."

                # Create Substack-style card
                with st.container():
                    st.markdown(f"""
                    <div style="background: white;
                                border: 1px solid #e5e7eb;
                                border-radius: 12px;
                                padding: 2rem;
                                margin-bottom: 1.5rem;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                transition: box-shadow 0.3s;">
                        <h3 style="margin: 0 0 0.5rem 0;
                                   color: #1a1a1a;
                                   font-weight: 600;
                                   font-size: 1.5rem;
                                   line-height: 1.3;">
                            {title}
                        </h3>
                        <div style="color: #6b7280;
                                    font-size: 0.875rem;
                                    margin-bottom: 1rem;
                                    display: flex;
                                    gap: 1rem;
                                    align-items: center;">
                            <span>✍️ {wisdom.author_email.split('@')[0]}</span>
                            <span>•</span>
                            <span>📅 {wisdom.created_at.strftime('%b %d, %Y')}</span>
                            <span>•</span>
                            <span>👁️ {wisdom.views} views</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Content preview (first 300 characters)
                    preview = wisdom.content[:300] + "..." if len(wisdom.content) > 300 else wisdom.content
                    st.markdown(f"<p style='color: #4b5563; line-height: 1.6; margin-bottom: 1rem;'>{preview}</p>", unsafe_allow_html=True)

                    # Tags
                    if tags and any(tags):
                        tag_html = " ".join([f"<span style='background: #f3f4f6; color: #6b7280; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem; margin-right: 0.5rem;'>#{tag}</span>" for tag in tags if tag])
                        st.markdown(tag_html, unsafe_allow_html=True)

                    # Action buttons - different for own stories vs others
                    is_own_story = False
                    if st.session_state.get('authenticated', False):
                        user_email = st.session_state.get('username', '') + '@ysenseai.org'
                        is_own_story = (wisdom.author_email == user_email)

                    if is_own_story:
                        # Show edit/delete for own stories
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                        with col1:
                            if st.button("📖 Read", key=f"read_{wisdom.id}", use_container_width=True):
                                st.session_state[f"show_full_{wisdom.id}"] = True
                        with col2:
                            if st.button("✏️ Edit", key=f"edit_{wisdom.id}", use_container_width=True):
                                st.info("✏️ Edit feature coming soon!")
                        with col3:
                            if st.button("🗑️ Delete", key=f"delete_{wisdom.id}", use_container_width=True):
                                st.warning("⚠️ Delete confirmation coming soon!")
                    else:
                        # Show read/save for other stories
                        col1, col2, col3 = st.columns([1, 1, 4])
                        with col1:
                            if st.button("📖 Read Full Story", key=f"read_{wisdom.id}", use_container_width=True):
                                st.session_state[f"show_full_{wisdom.id}"] = True
                        with col2:
                            if st.button("📥 Save", key=f"save_{wisdom.id}", use_container_width=True):
                                st.success("✅ Saved to your library!")

                    # Show full content if expanded
                    if st.session_state.get(f"show_full_{wisdom.id}", False):
                        st.markdown("---")
                        st.markdown(f"### {title}")
                        st.markdown(f"<div style='white-space: pre-wrap; line-height: 1.8; color: #1f2937;'>{wisdom.content}</div>", unsafe_allow_html=True)
                        st.markdown("---")

                        # Metadata
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("👁️ Views", wisdom.views)
                        with col2:
                            st.metric("📥 Downloads", wisdom.downloads)
                        with col3:
                            st.metric("📁 Category", wisdom.category)
                        with col4:
                            if st.button("✖️ Close", key=f"close_{wisdom.id}"):
                                st.session_state[f"show_full_{wisdom.id}"] = False
                                st.rerun()

                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("📭 No stories found. Be the first to share your wisdom!")
            st.markdown("💡 Use the **🤖 AI Workflow** page to create your first story.")

    except Exception as e:
        st.error(f"Error loading wisdom library: {e}")
        st.info("💡 The wisdom library is initializing. Please try again in a moment.")

def show_v4_interface():
    """Show the new methodology-based AI workflow interface"""
    st.subheader("🤖 YSense™ Methodology AI Workflow")

    # Import demo mode config
    try:
        from src.demo_mode_config import live_demo_mode

        # Show Live Demo Mode Banner
        if live_demo_mode.ENABLED and live_demo_mode.SHOW_DEMO_BANNER:
            st.warning("🎬 **LIVE DEMO MODE** - Real AI Analysis with No Data Persistence")

            with st.expander("⚠️ IMPORTANT: Read Before Using", expanded=False):
                st.markdown(live_demo_mode.get_demo_disclaimer())

            # Show usage limits
            if 'demo_analyses_count' in st.session_state:
                remaining = live_demo_mode.MAX_ANALYSES_PER_SESSION - st.session_state.get('demo_analyses_count', 0)
                st.info(f"📊 Demo Analyses Remaining: **{remaining}/{live_demo_mode.MAX_ANALYSES_PER_SESSION}**")
    except ImportError:
        pass

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
        # Import demo mode for validation
        try:
            from src.demo_mode_config import live_demo_mode

            # Validate demo limits
            if live_demo_mode.ENABLED:
                validation = live_demo_mode.validate_demo_limits(st.session_state)
                if not validation['allowed']:
                    st.error(f"❌ {validation['reason']}")
                    st.warning(validation['message'])
                    st.stop()

                # Check story length limit
                if len(user_story) > live_demo_mode.MAX_STORY_LENGTH:
                    st.error(f"❌ Story too long for demo: {len(user_story)}/{live_demo_mode.MAX_STORY_LENGTH} characters")
                    st.warning("Please shorten your story for the demo version.")
                    st.stop()
        except ImportError:
            pass

        if user_story.strip():
            # Create user vibe data BEFORE try block to ensure it's always available in fallback
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

            with st.spinner("🔄 Processing through 3-stage methodology..."):
                try:
                    # Import the new methodology engine
                    import sys
                    import os
                    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                    from src.methodology_core_engine import methodology_engine
                    from src.demo_mode_config import live_demo_mode

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
                    
                    # Store results in session state (session-only, not database)
                    st.session_state.methodology_results = results

                    # Increment demo usage counter
                    try:
                        from src.demo_mode_config import live_demo_mode
                        if live_demo_mode.ENABLED:
                            live_demo_mode.increment_usage(st.session_state)
                    except ImportError:
                        pass

                    st.success("✅ Analysis completed!")
                    st.info("💾 **Results stored in session only** - Will be lost on page refresh")

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
        # Check if demo mode prevents database saves
        try:
            from src.demo_mode_config import live_demo_mode
            if live_demo_mode.ENABLED and not live_demo_mode.should_save_to_database():
                st.error("❌ **Database saves disabled in Live Demo Mode**")
                st.warning("This is a demonstration platform. Data is not permanently stored.")
                st.info("💡 To save your analysis:\n1. Copy/paste results to a local file\n2. Take screenshots\n3. Save to your own storage")
                st.stop()
        except ImportError:
            pass

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
    # Initialize session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'wisdom_results' not in st.session_state:
        st.session_state.wisdom_results = None
    if 'user_tier' not in st.session_state:
        st.session_state.user_tier = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'public_key' not in st.session_state:
        st.session_state.public_key = None

    # ========== PROTOTYPE MODE: Show warning banner on ALL pages ==========
    prototype_mode.show_prototype_banner()
    # ======================================================================

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
        try:
            has_token = 'token' in st.query_params
        except:
            has_token = False

        if has_token:
            show_password_reset()
        else:
            # Show navigation for non-authenticated users
            st.sidebar.markdown("### 🌐 Public Access")

            # ========== PROTOTYPE MODE: Home button ==========
            if st.sidebar.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "home"
                st.rerun()
            # =================================================

            # Your desired navigation links
            if st.sidebar.button("📜 Terms & Consent", use_container_width=True):
                st.session_state.current_page = "terms"
                st.rerun()

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

            # ========== PROTOTYPE MODE: Privacy Policy button ==========
            if st.sidebar.button("🔒 Privacy Policy", use_container_width=True):
                st.session_state.current_page = "privacy"
                st.rerun()
            # ===========================================================

            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔐 Prototype Demo Access")

            # ========== PROTOTYPE MODE: Demo Login Button ==========
            if st.sidebar.button("🎯 Try Demo Platform", use_container_width=True, type="primary"):
                st.session_state.current_page = "demo_login"
                st.rerun()

            st.sidebar.info("🚧 Shared demo account for all users")
            # =======================================================
            
            # Show current page content
            current_page = st.session_state.get('current_page', 'home')

            # ========== PROTOTYPE MODE: Home/Welcome page ==========
            if current_page == "home":
                prototype_mode.show_welcome_page()

                st.markdown("---")
                st.markdown("## 📊 Explore the Platform Demonstration")
                st.markdown("""
                Navigate through the complete platform concept:
                - **🏠 Home**: Platform introduction and vision
                - **📜 Terms & Consent**: Our ethical framework and legal approach
                - **📚 Wisdom Library**: Browse shared knowledge and stories
                - **📄 White Paper**: Read our vision, approach, and technical details
                - **📖 Founder's Story**: Understand the mission and motivation
                - **🔓 Open Source**: View our commitment to transparency
                """)

                # Interest tracking button
                prototype_mode.show_interest_button()

            # Demo login page
            elif current_page == "demo_login":
                prototype_mode.show_login_page()

            # Privacy Policy page
            elif current_page == "privacy":
                st.title("🔒 Privacy Policy - Prototype")
                st.markdown(prototype_privacy.get_privacy_policy())
            # =======================================================

            elif current_page == "terms":
                show_terms_and_consent()
            elif current_page == "whitepaper":
                show_whitepaper()
            elif current_page == "founders_story":
                show_founders_story()
            elif current_page == "open_source":
                show_open_source()
            elif current_page == "wisdom_library":
                show_wisdom_library()
    else:
        # Authenticated user navigation
        st.sidebar.success(f"Welcome, {st.session_state.username}! (Demo)")
        st.sidebar.info(f"🔑 Tier: {st.session_state.user_tier}")
        st.sidebar.warning("🚧 Prototype - Demo Account")

        # Demo mode data warning in sidebar
        try:
            from src.demo_mode_config import live_demo_mode
            if live_demo_mode.ENABLED:
                with st.sidebar.expander("⚠️ Demo Data Warning"):
                    st.warning("All analysis results will be lost on logout/refresh!")
        except ImportError:
            pass

        if st.sidebar.button("🚪 Logout"):
            # Show logout warning
            try:
                from src.demo_mode_config import live_demo_mode
                if live_demo_mode.ENABLED:
                    # Check if user has any analysis results
                    if 'methodology_results' in st.session_state:
                        st.sidebar.error("⚠️ You have unsaved analysis results!")
                        st.sidebar.warning("Logging out will delete all your data.")
                        if not st.sidebar.button("⚠️ Confirm Logout (Data Will Be Lost)", type="primary"):
                            st.stop()

                    # Clear demo session data
                    live_demo_mode.clear_session_data(st.session_state)
            except ImportError:
                pass

            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.user_tier = None
            st.session_state.public_key = None
            st.rerun()
        
        # Main navigation
        page = st.sidebar.selectbox(
            "Choose Page",
            ["🏠 Dashboard", "📚 Wisdom Library", "🤖 AI Workflow", "💰 Revenue Dashboard", "📄 White Paper"]
        )
        
        if page == "🏠 Dashboard":
            st.subheader("🏠 Dashboard")
            st.info("Welcome to YSense™ v4.1! Use the navigation menu to explore features.")
            
        elif page == "📚 Wisdom Library":
            show_wisdom_library()

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

    # ========== PROTOTYPE MODE: Footer disclaimer on all pages ==========
    prototype_mode.show_footer_disclaimer()
    # ===================================================================

if __name__ == "__main__":
    main()

