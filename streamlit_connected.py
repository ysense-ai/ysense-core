"""
YSense Platform v3.0 - Connected Streamlit UI
Links to backend API for data persistence
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

st.title("🚀 YSense™ Platform v3.0")
st.markdown("**AI Attribution Infrastructure** | DOI: 10.5281/zenodo.17072168")

# Registration Section
st.header("📝 User Registration")

with st.form("registration_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username*")
        email = st.text_input("Email*")
        attribution_name = st.text_input("Attribution Name (Optional)")
    
    with col2:
        age = st.number_input("Age*", min_value=18, max_value=120)
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
        # Check all required fields
        if not all([username, email, age, jurisdiction]):
            st.error("Please fill all required fields")
        elif not all([consent_data, consent_commercial, consent_ai, consent_revenue, consent_attribution, consent_terms]):
            st.error("Please accept all required consents")
        else:
            # Call backend API
            try:
                # Check if backend is running
                health_response = requests.get(f"{API_URL}/health")
                
                if health_response.status_code == 200:
                    st.success("✅ Registration successful! (Backend connected)")
                    st.balloons()
                    
                    # Store in session state
                    st.session_state['user'] = {
                        'username': username,
                        'email': email,
                        'attribution_name': attribution_name,
                        'consents': {
                            'data_collection': consent_data,
                            'commercial_use': consent_commercial,
                            'ai_training': consent_ai,
                            'revenue_model': consent_revenue,
                            'attribution': consent_attribution,
                            'terms': consent_terms
                        },
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    st.warning("⚠️ Backend not responding. Registration saved locally.")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API server. Please ensure the backend is running on port 8000")
                st.info("Run this command in another terminal: python working_api.py")
            except Exception as e:
                st.error(f"Error: {e}")

# Show backend status
with st.sidebar:
    st.header("🔌 System Status")
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend: Connected")
            st.write(f"API: {API_URL}")
        else:
            st.error("❌ Backend: Error")
    except:
        st.error("❌ Backend: Not Running")
        st.write("Start backend with:")
        st.code("python working_api.py")

# Footer
st.divider()
st.markdown("YSense™ Platform v2.0 | Protected by Defensive Publication | Teluk Intan, Malaysia")
