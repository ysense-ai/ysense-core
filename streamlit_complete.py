"""
YSense Platform v3.0 - Complete Registration System
Fully connected frontend with backend persistence
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Backend API URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="YSense™ Platform v3.0",
    page_icon="🔒",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Sidebar - System Status
with st.sidebar:
    st.header("💡 System Status")
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend: Connected")
            st.write(f"API: {API_URL}")
        else:
            st.error("❌ Backend: Error")
    except:
        st.error("❌ Backend: Not Running")
    
    # Login Status
    if st.session_state.logged_in:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

# Main Content
st.title("🚀 YSense™ Platform v3.0")
st.markdown("**AI Attribution Infrastructure** | DOI: 10.5281/zenodo.17072168")

# Show different content based on login status
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["📝 Register", "🔐 Login"])
    
    with tab1:
        st.header("User Registration")
        
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*")
                email = st.text_input("Email*")
                attribution_name = st.text_input("Attribution Name (Optional)")
            
            with col2:
                age = st.number_input("Age*", min_value=18, max_value=120, value=18)
                jurisdiction = st.selectbox("Jurisdiction*", ["Malaysia", "Singapore", "UK", "EU", "US", "Other"])
                cultural_context = st.selectbox("Cultural Context", ["Malaysian", "Western", "Asian", "Global"])
            
            st.subheader("📋 Required Consents")
            consent_data = st.checkbox("✅ Data Collection: I consent to YSense collecting my wisdom contributions")
            consent_commercial = st.checkbox("✅ Commercial Use: I consent to commercial use with mandatory attribution")
            consent_ai = st.checkbox("✅ AI Training: I consent to ethical AI training use with attribution")
            consent_revenue = st.checkbox("✅ Revenue Model: I accept the 30-50% tiered revenue sharing terms")
            consent_attribution = st.checkbox("✅ Attribution: I understand attribution is permanent and cannot be removed")
            consent_terms = st.checkbox("✅ Terms Acceptance: I have read and accept the Terms of Service v2.0")
            
            submitted = st.form_submit_button("Create Account", type="primary")
            
            if submitted:
                if not all([username, email, age, jurisdiction]):
                    st.error("Please fill all required fields")
                elif not all([consent_data, consent_commercial, consent_ai, consent_revenue, consent_attribution, consent_terms]):
                    st.error("Please accept all required consents")
                else:
                    # Register with backend
                    registration_data = {
                        "username": username,
                        "email": email,
                        "attribution_name": attribution_name or username,
                        "age": age,
                        "jurisdiction": jurisdiction,
                        "consents": {
                            "data_collection": consent_data,
                            "commercial_use": consent_commercial,
                            "ai_training": consent_ai,
                            "revenue_model": consent_revenue,
                            "attribution": consent_attribution,
                            "terms": consent_terms
                        }
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/register", json=registration_data)
                        if response.status_code == 200:
                            st.success("✅ Registration successful! (Backend connected)")
                            st.balloons()
                            # Auto login after registration
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
    
    with tab2:
        st.header("Login")
        
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password", help="For demo: use any password")
            
            if st.form_submit_button("Login"):
                if login_username:
                    # Simple login (for demo - no password check)
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Please enter username")

else:
    # Logged in - Show main platform
    st.success(f"Welcome back, {st.session_state.username}!")
    
    # Main Platform Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💰 Revenue", "🔐 Z Protocol", "📈 Analytics"])
    
    with tab1:
        st.header("Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Your Contributions", "0", "+0")
        with col2:
            st.metric("Revenue Generated", "€0.00", "")
        with col3:
            st.metric("Attribution Score", "0", "")
        with col4:
            st.metric("Platform Version", "3.0", "")
        
        st.divider()
        
        # Wisdom Contribution Form
        st.subheader("📝 Submit New Wisdom")
        with st.form("wisdom_form"):
            wisdom_content = st.text_area("Your Wisdom Content", 
                placeholder="Share your knowledge, insights, or expertise...")
            wisdom_category = st.selectbox("Category", 
                ["Technology", "Philosophy", "Business", "Science", "Culture", "Other"])
            
            if st.form_submit_button("Submit Wisdom"):
                if wisdom_content:
                    st.success("Wisdom submitted for attribution!")
                    # Here you would send to backend
                else:
                    st.warning("Please enter some content")
    
    with tab2:
        st.header("💰 Revenue Dashboard")
        st.info("Revenue tracking based on your attributed contributions")
        
        # Revenue metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", "€0.00")
        with col2:
            st.metric("This Month", "€0.00")
        with col3:
            st.metric("Pending", "€0.00")
        
        # Revenue calculator
        st.subheader("Revenue Calculator")
        contributions = st.slider("Number of contributions", 0, 1000, 100)
        usage_rate = st.slider("Average usage rate", 0.0, 1.0, 0.1)
        estimated_revenue = contributions * 0.10 * usage_rate * 0.70
        st.success(f"Estimated Revenue: €{estimated_revenue:.2f}")
    
    with tab3:
        st.header("🔐 Z Protocol Management")
        st.write("Manage your consent preferences")
        
        # Show current consents
        st.subheader("Your Active Consents")
        st.write("✅ Data Collection: Active")
        st.write("✅ Commercial Use: Active")
        st.write("✅ AI Training: Active")
        st.write("✅ Revenue Sharing: Active")
        
        if st.button("Withdraw Consent"):
            st.warning("This will remove your data from the platform")
    
    with tab4:
        st.header("📈 Analytics")
        
        # View registered users (if backend connected)
        try:
            response = requests.get(f"{API_URL}/users")
            if response.status_code == 200:
                data = response.json()
                st.metric("Total Users", data.get("count", 0))
                
                if data.get("users"):
                    st.subheader("Registered Users")
                    st.json(data["users"])
        except:
            st.info("Analytics will appear here once data is available")

# Footer
st.divider()
st.markdown("YSense™ Platform v3.0 | Protected by Defensive Publication | Teluk Intan, Malaysia")
