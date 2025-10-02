# src/tos_component.py
"""
YSense™ Platform v4.1 - Terms of Service UI Component
Z Protocol v2.0 Compliant Registration Flow
"""

import streamlit as st
from typing import Dict, Optional
from datetime import datetime
import hashlib

def display_tos_modal() -> bool:
    """Display Terms of Service modal and get user acceptance"""

    st.markdown("""
    <style>
    .tos-container {
        background-color: #f8f9fa;
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .tos-header {
        color: #007bff;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .tos-section {
        margin: 15px 0;
        padding: 10px;
        background: white;
        border-radius: 5px;
    }
    .z-protocol-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin: 10px 0;
    }
    .privacy-badge {
        background: #28a745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="tos-container">', unsafe_allow_html=True)

        st.markdown('<div class="tos-header">📋 Terms of Service & Privacy Policy</div>', unsafe_allow_html=True)

        st.markdown('<div class="z-protocol-badge">🛡️ Z Protocol v2.0 Compliant</div>', unsafe_allow_html=True)

        # Quick summary
        st.markdown("""
        ### 🎯 Quick Summary

        **Privacy-First Platform** - Your data, your control:

        - ✅ **No passwords** - Cryptographic key authentication only
        - ✅ **Explicit consent** - Every use requires your permission
        - ✅ **Revenue sharing** - 15-30% based on content tier
        - ✅ **72-hour deletion** - GDPR compliant data removal
        - ✅ **100% attribution** - Full recognition for your wisdom
        - ✅ **Cultural sovereignty** - Community control over knowledge
        """)

        # Core principles
        with st.expander("🛡️ Core Principles (Z Protocol v2.0)", expanded=False):
            st.markdown("""
            1. **Human Dignity Primacy**: You are a wisdom carrier, not a data point
            2. **Cultural Sovereignty**: Complete control over your knowledge and stories
            3. **Transparent Attribution**: Full tracking and recognition
            4. **Equitable Value Sharing**: Fair compensation (15-30% revenue share)
            """)

        # Five-tier system
        with st.expander("🎯 Five-Tier Content Classification", expanded=False):
            st.markdown("""
            Choose your content tier for each wisdom submission:

            | Tier | Revenue Share | Use Case |
            |------|--------------|----------|
            | **PUBLIC** | 15% | Open educational content |
            | **PERSONAL** | 20% | Personal experiences |
            | **CULTURAL** | 25% + fund | Traditional knowledge |
            | **SACRED** | 30% + fund | Spiritual/ceremonial content |
            | **THERAPEUTIC** | 25% + fund | Mental health/healing insights |
            """)

        # Privacy guarantees
        with st.expander("🔐 Privacy Guarantees", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                **We NEVER:**
                - ❌ Sell your data
                - ❌ Use data without consent
                - ❌ Train AI without permission
                - ❌ Share without approval
                """)

            with col2:
                st.markdown("""
                **We ALWAYS:**
                - ✅ Ask explicit consent
                - ✅ Share revenue (15-30%)
                - ✅ Delete within 72 hours
                - ✅ Maintain 100% attribution
                """)

        # Your rights
        with st.expander("🔑 Your Rights & Controls", expanded=False):
            st.markdown("""
            **GDPR & PDPA Compliant Rights:**

            1. **Access** - Download all your data anytime
            2. **Rectification** - Correct any inaccurate data
            3. **Erasure** - Delete your data within 72 hours
            4. **Portability** - Export data in JSON/CSV
            5. **Restriction** - Limit how data is used
            6. **Object** - Object to specific processing
            7. **Withdraw Consent** - Stop AI training anytime
            """)

        # Revenue transparency
        with st.expander("💰 Revenue Transparency", expanded=False):
            st.markdown("""
            **Public Dashboard Access:**
            - ✅ Total platform revenue (public)
            - ✅ Your individual earnings (private)
            - ✅ Content performance metrics
            - ✅ Revenue tier breakdown
            - ✅ Payout history

            **Transparency Standard:**
            - 100% visibility into revenue calculations
            - Real-time dashboard updates
            - Monthly payout schedules
            - Community fund allocations
            """)

        st.markdown('</div>', unsafe_allow_html=True)

    # Acceptance checkboxes
    st.markdown("---")
    st.markdown("### ✍️ Required Acknowledgements")

    accept_read = st.checkbox(
        "✅ I have read and understood the Terms of Service and Privacy Policy",
        key="tos_read"
    )

    accept_z_protocol = st.checkbox(
        "✅ I understand the Z Protocol v2.0 framework and consent principles",
        key="tos_z_protocol"
    )

    accept_privacy = st.checkbox(
        "✅ I understand my data privacy rights and revenue sharing model",
        key="tos_privacy"
    )

    accept_consent = st.checkbox(
        "✅ I agree to provide explicit consent for each wisdom submission and AI training use",
        key="tos_consent"
    )

    accept_cultural = st.checkbox(
        "✅ I acknowledge the cultural sovereignty principles for Cultural/Sacred tier content",
        key="tos_cultural"
    )

    # Full acceptance
    st.markdown("---")
    accept_all = st.checkbox(
        "**📝 I ACCEPT the Terms of Service and agree to all above statements**",
        key="tos_accept_all"
    )

    # Validation
    all_checked = (
        accept_read and
        accept_z_protocol and
        accept_privacy and
        accept_consent and
        accept_cultural and
        accept_all
    )

    if all_checked:
        st.success("✅ Thank you for accepting our Terms of Service!")
        st.markdown("""
        <div class="privacy-badge">🛡️ Privacy-First</div>
        <div class="privacy-badge">🔐 Z Protocol v2.0</div>
        <div class="privacy-badge">💰 Revenue Transparent</div>
        """, unsafe_allow_html=True)

        # Show full ToS link
        st.markdown("""
        📄 **Full Terms of Service**: [View Complete Document](TERMS_OF_SERVICE.md)
        """)

        return True
    else:
        if accept_all and not all_checked:
            st.warning("⚠️ Please check all acknowledgements above to continue")
        return False


def display_consent_checkboxes() -> Dict[str, bool]:
    """Display granular consent checkboxes for wisdom submission"""

    st.markdown("### ✅ Content Consent Options")

    st.info("**For each wisdom you submit, you control:**")

    consents = {}

    # Storage (always required)
    st.markdown("#### 📦 **Storage** (Required)")
    consents['storage'] = st.checkbox(
        "I consent to YSense™ storing this content securely",
        value=True,
        disabled=True,
        key="consent_storage"
    )

    # AI Training (optional)
    st.markdown("#### 🤖 **AI Training** (Optional)")
    consents['ai_training'] = st.checkbox(
        "I consent to this content being used for AI training (enables revenue sharing)",
        key="consent_ai_training"
    )

    if consents['ai_training']:
        st.success("✅ Revenue sharing enabled based on selected tier")

    # Public Sharing (optional)
    st.markdown("#### 🌍 **Public Sharing** (Optional)")
    consents['public_sharing'] = st.checkbox(
        "I consent to this content being publicly visible",
        key="consent_public"
    )

    # Cultural Community (for Cultural/Sacred tiers)
    st.markdown("#### 🏛️ **Cultural Community Attribution** (For Cultural/Sacred tiers)")
    consents['cultural_community'] = st.checkbox(
        "I consent to cultural community attribution (required for Cultural/Sacred tiers)",
        key="consent_cultural"
    )

    return consents


def generate_consent_signature(user_id: str, consents: Dict) -> str:
    """Generate cryptographic signature for consent record"""

    consent_string = f"{user_id}:{json.dumps(consents, sort_keys=True)}:{datetime.now().isoformat()}"
    return hashlib.sha256(consent_string.encode()).hexdigest()


def display_content_tier_selector() -> tuple:
    """Display content tier selector with revenue information"""

    st.markdown("### 🎯 Select Content Tier")

    tier_options = {
        "PUBLIC": {
            "revenue": "15%",
            "description": "Open educational and research content",
            "icon": "📚"
        },
        "PERSONAL": {
            "revenue": "20%",
            "description": "Individual experiences and personal stories",
            "icon": "👤"
        },
        "CULTURAL": {
            "revenue": "25% + community fund",
            "description": "Traditional knowledge and cultural practices",
            "icon": "🏛️"
        },
        "SACRED": {
            "revenue": "30% + community fund",
            "description": "Spiritual, ceremonial, deeply cultural content",
            "icon": "🕉️"
        },
        "THERAPEUTIC": {
            "revenue": "25% + research fund",
            "description": "Mental health, healing, wellness insights",
            "icon": "🧘"
        }
    }

    # Display tier options
    cols = st.columns(len(tier_options))

    for idx, (tier, info) in enumerate(tier_options.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin: 5px;
            ">
                <div style="font-size: 32px;">{info['icon']}</div>
                <div style="font-weight: bold; font-size: 16px;">{tier}</div>
                <div style="font-size: 14px; margin: 5px 0;">{info['revenue']}</div>
                <div style="font-size: 12px; opacity: 0.9;">{info['description']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Selector
    tier = st.selectbox(
        "Choose your tier:",
        options=list(tier_options.keys()),
        format_func=lambda x: f"{tier_options[x]['icon']} {x} - {tier_options[x]['revenue']}",
        key="tier_selector"
    )

    # Show tier details
    selected_tier = tier_options[tier]

    st.info(f"""
    **Selected: {selected_tier['icon']} {tier}**

    - **Revenue Share**: {selected_tier['revenue']}
    - **Use Case**: {selected_tier['description']}
    """)

    # Extract revenue percentage
    revenue_share = {
        "PUBLIC": 0.15,
        "PERSONAL": 0.20,
        "CULTURAL": 0.25,
        "SACRED": 0.30,
        "THERAPEUTIC": 0.25
    }

    return tier, revenue_share[tier]
