# src/prototype_mode.py
"""
YSense™ Platform - Prototype Mode Configuration
Safe demonstration mode with no personal data collection
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict

# Google Cloud Firestore
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False

class PrototypeMode:
    """Manages prototype/demo mode for YSense Platform"""

    def __init__(self):
        self.demo_username = "demo_user"
        self.demo_password = "ysense_prototype_2025"
        self.interest_counter_file = "prototype_interest_count.json"

        # Initialize Firestore client (uses application default credentials on GCP)
        if FIRESTORE_AVAILABLE:
            try:
                self.db = firestore.Client()
                self.use_firestore = True
            except Exception as e:
                # Fallback to JSON file if Firestore fails (local development)
                self.use_firestore = False
                st.warning(f"Firestore not available, using local file storage. Error: {e}")
        else:
            self.use_firestore = False

    def show_prototype_banner(self):
        """Display prominent prototype warning banner on every page"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFA500 0%, #FF6B35 100%);
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin-bottom: 2rem;
                    border: 3px solid #FF4500;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="color: white; margin: 0; text-align: center; font-size: 1.8rem;">
                🚧 PROTOTYPE DEMONSTRATION - NOT PRODUCTION 🚧
            </h2>
            <div style="background: rgba(255,255,255,0.95);
                        padding: 1rem;
                        border-radius: 8px;
                        margin-top: 1rem;">
                <p style="color: #333; margin: 0.5rem 0; font-size: 1.1rem;">
                    <strong>⚠️ IMPORTANT NOTICE:</strong>
                </p>
                <ul style="color: #333; margin: 0.5rem 0; font-size: 1rem; line-height: 1.6;">
                    <li><strong>This is a demonstration platform</strong> to showcase the YSense concept</li>
                    <li><strong>No personal data is collected or stored</strong> during this prototype phase</li>
                    <li><strong>All demo data resets regularly</strong> - nothing is permanent</li>
                    <li><strong>For educational and testing purposes only</strong></li>
                    <li><strong>Production version coming soon</strong> with full data protection</li>
                </ul>
                <p style="color: #666; margin: 0.5rem 0; font-size: 0.95rem; font-style: italic;">
                    This prototype demonstrates the vision for ethical AI attribution infrastructure.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def show_demo_credentials(self):
        """Display demo account credentials"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin: 1.5rem 0;
                    border: 2px solid #2E5C8A;">
            <h3 style="color: white; margin: 0 0 1rem 0; text-align: center;">
                🎯 Demo Access Credentials
            </h3>
            <div style="background: white;
                        padding: 1.5rem;
                        border-radius: 8px;
                        font-family: 'Courier New', monospace;">
                <div style="margin: 0.5rem 0;">
                    <span style="color: #666; font-weight: bold;">Username:</span>
                    <span style="color: #2E5C8A; font-size: 1.2rem; margin-left: 1rem; font-weight: bold;">
                        demo_user
                    </span>
                </div>
                <div style="margin: 0.5rem 0;">
                    <span style="color: #666; font-weight: bold;">Password:</span>
                    <span style="color: #2E5C8A; font-size: 1.2rem; margin-left: 1rem; font-weight: bold;">
                        ysense_prototype_2025
                    </span>
                </div>
            </div>
            <p style="color: white; margin: 1rem 0 0 0; text-align: center; font-size: 0.9rem;">
                ℹ️ Everyone uses the same demo account to explore platform features
            </p>
        </div>
        """, unsafe_allow_html=True)

    def show_welcome_page(self):
        """Show welcoming prototype introduction page"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #2E5C8A; font-size: 2.5rem; margin-bottom: 1rem;">
                Welcome to YSense™ Platform Prototype
            </h1>
            <p style="color: #666; font-size: 1.2rem; max-width: 800px; margin: 0 auto 2rem auto; line-height: 1.6;">
                The world's first AI Attribution Infrastructure platform - currently in prototype demonstration phase.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Three-column feature showcase
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; height: 200px;">
                <h3 style="color: #4A90E2; text-align: center;">🎯 Explore Concept</h3>
                <p style="color: #666; text-align: center;">
                    See how AI attribution and ethical wisdom sharing could work
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; height: 200px;">
                <h3 style="color: #4A90E2; text-align: center;">🧪 Test Features</h3>
                <p style="color: #666; text-align: center;">
                    Try the wisdom library, attribution system, and transparency tools
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; height: 200px;">
                <h3 style="color: #4A90E2; text-align: center;">💡 Share Feedback</h3>
                <p style="color: #666; text-align: center;">
                    Help shape the future of ethical AI development
                </p>
            </div>
            """, unsafe_allow_html=True)

    def increment_interest_counter(self):
        """Increment the interest counter (anonymous)"""
        try:
            if self.use_firestore:
                # Use Firestore
                doc_ref = self.db.collection('prototype_stats').document('interest_counter')
                doc = doc_ref.get()

                if doc.exists:
                    data = doc.to_dict()
                    data["count"] += 1
                    data["last_interest"] = datetime.now().isoformat()
                else:
                    data = {
                        "count": 1,
                        "first_interest": datetime.now().isoformat(),
                        "last_interest": datetime.now().isoformat()
                    }

                doc_ref.set(data)
                return data["count"]
            else:
                # Fallback to JSON file (local development)
                if os.path.exists(self.interest_counter_file):
                    with open(self.interest_counter_file, 'r') as f:
                        data = json.load(f)
                else:
                    data = {"count": 0, "first_interest": datetime.now().isoformat()}

                data["count"] += 1
                data["last_interest"] = datetime.now().isoformat()

                with open(self.interest_counter_file, 'w') as f:
                    json.dump(data, f, indent=2)

                return data["count"]
        except Exception as e:
            st.error(f"Error incrementing counter: {e}")
            return 0

    def get_interest_count(self) -> int:
        """Get current interest count"""
        try:
            if self.use_firestore:
                # Use Firestore
                doc_ref = self.db.collection('prototype_stats').document('interest_counter')
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict().get("count", 0)
                return 0
            else:
                # Fallback to JSON file (local development)
                if os.path.exists(self.interest_counter_file):
                    with open(self.interest_counter_file, 'r') as f:
                        data = json.load(f)
                        return data.get("count", 0)
                return 0
        except Exception as e:
            return 0

    def show_interest_button(self):
        """Display interest tracking button"""
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem;
                        border-radius: 15px;
                        text-align: center;
                        margin: 2rem 0;">
                <h3 style="color: white; margin: 0 0 1rem 0;">
                    Interested in YSense Platform?
                </h3>
                <p style="color: white; margin: 0 0 1.5rem 0;">
                    Help us gauge interest in ethical AI attribution infrastructure
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("👍 I'm Interested in This Concept", use_container_width=True, type="primary"):
                new_count = self.increment_interest_counter()
                st.success(f"✅ Thank you! Your interest has been recorded.")
                st.balloons()
                st.info(f"👥 **{new_count} people** have shown interest in YSense Platform!")

            # Always show current count
            current_count = self.get_interest_count()
            if current_count > 0:
                st.markdown(f"""
                <div style="background: #f0f7ff;
                            padding: 1rem;
                            border-radius: 8px;
                            text-align: center;
                            margin-top: 1rem;
                            border: 2px solid #4A90E2;">
                    <p style="color: #2E5C8A; font-size: 1.2rem; margin: 0; font-weight: bold;">
                        👥 {current_count} people interested so far!
                    </p>
                </div>
                """, unsafe_allow_html=True)

    def demo_login(self, username: str, password: str) -> bool:
        """Verify demo account credentials"""
        return (username == self.demo_username and password == self.demo_password)

    def get_demo_credentials(self) -> Dict[str, str]:
        """Return demo credentials"""
        return {
            "username": self.demo_username,
            "password": self.demo_password
        }

    def show_login_page(self):
        """Show prototype login page with demo credentials"""
        st.title("🔐 YSense Platform - Demo Access")

        # Show prototype warning
        self.show_prototype_banner()

        # Show demo credentials prominently
        self.show_demo_credentials()

        st.markdown("---")

        # Login form
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.subheader("Enter Demo Credentials")

            username = st.text_input("Username", value="", placeholder="demo_user")
            password = st.text_input("Password", value="", type="password", placeholder="ysense_prototype_2025")

            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("🚀 Enter Demo Platform", use_container_width=True, type="primary"):
                    if self.demo_login(username, password):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = self.demo_username
                        st.session_state['demo_mode'] = True
                        st.success("✅ Demo access granted!")
                        st.rerun()
                    else:
                        st.error("❌ Please use the demo credentials shown above")

            with col_b:
                if st.button("📋 Auto-Fill Demo Credentials", use_container_width=True):
                    st.info("Use the credentials displayed in the blue box above!")

        st.markdown("---")

        # Information section
        st.markdown("""
        ### 💡 About This Prototype

        This demonstration showcases the **vision and concept** of YSense Platform:

        - **Explore** the wisdom library and attribution system
        - **Test** the interface and user experience
        - **Understand** how ethical AI attribution could work
        - **Provide feedback** to help shape the platform

        **Remember:** This is a prototype. No real accounts, no personal data collected, no permanent storage.

        The production version will include:
        - ✅ Full user authentication with secure accounts
        - ✅ Permanent database with data protection
        - ✅ Legal compliance (GDPR, privacy laws)
        - ✅ Revenue sharing system (when operational)
        - ✅ Professional-grade security
        """)

    def is_prototype_mode(self) -> bool:
        """Check if running in prototype mode"""
        return True  # Always true for now

    def show_footer_disclaimer(self):
        """Show footer disclaimer on all pages"""
        st.markdown("---")
        st.markdown("""
        <div style="background: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 1px solid #dee2e6;
                    margin-top: 2rem;">
            <p style="color: #666; margin: 0; font-size: 0.9rem;">
                🚧 <strong>Prototype Demonstration</strong> | No Personal Data Collected |
                All Data Resets Regularly | Educational Purpose Only
            </p>
            <p style="color: #888; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
                YSense™ Platform v4.1 - Concept Demonstration | © 2025 YSense AI
            </p>
        </div>
        """, unsafe_allow_html=True)


# Global instance
prototype_mode = PrototypeMode()
