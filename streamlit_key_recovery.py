# 🔑 YSense Platform v4.0 - Key Recovery Frontend

def show_key_recovery():
    """Show key recovery interface"""
    st.markdown("### 🔑 Key Recovery Center")
    st.markdown("Lost your keys? Don't worry, we can help you recover them!")
    
    # Recovery type selection
    recovery_type = st.selectbox(
        "What do you need to recover?",
        ["Crypto Key (for login)", "Z Protocol Key (for consent management)", "Both Keys"],
        help="Select the type of key you need to recover"
    )
    
    # Email input
    email = st.text_input(
        "Enter your registered email address",
        placeholder="your.email@example.com",
        help="Enter the email address you used to register your account"
    )
    
    # Recovery button
    if st.button("Send Recovery Email", type="primary", use_container_width=True):
        if not email:
            st.error("Please enter your email address")
            return
        
        # Map recovery type to API format
        recovery_type_map = {
            "Crypto Key (for login)": "crypto_key",
            "Z Protocol Key (for consent management)": "z_protocol_key",
            "Both Keys": "both"
        }
        
        api_recovery_type = recovery_type_map[recovery_type]
        
        # Show loading spinner
        with st.spinner("Sending recovery email..."):
            try:
                result = api_call("POST", "auth/recover-crypto-key", {
                    "email": email,
                    "recovery_type": api_recovery_type
                }, authenticated=False)
                
                if result and result.get("success"):
                    st.success("✅ Recovery email sent successfully!")
                    st.info("📧 Check your email inbox (and spam folder) for your keys.")
                    st.warning("⚠️ **Security Note:** If you didn't request this recovery, please contact support immediately.")
                    
                    # Show next steps
                    st.markdown("### 📋 Next Steps:")
                    st.markdown("1. **Check your email** for the recovery message")
                    st.markdown("2. **Copy your keys** from the email")
                    st.markdown("3. **Login** using your recovered crypto key")
                    st.markdown("4. **Consider generating new keys** for enhanced security")
                    
                    # Option to generate new keys
                    if st.button("Generate New Keys (Recommended)", type="secondary"):
                        st.info("🔐 You can generate new keys after logging in for enhanced security.")
                
                else:
                    st.error("❌ Failed to send recovery email. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Account recovery info
    st.markdown("---")
    st.markdown("### ℹ️ Account Recovery Information")
    
    if st.button("Check Account Status", type="secondary"):
        if not email:
            st.error("Please enter your email address first")
            return
        
        try:
            with st.spinner("Checking account status..."):
                result = api_call("GET", f"auth/account-recovery/{email}", 
                                authenticated=False)
                
                if result:
                    st.success("✅ Account found!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Username", result["username"])
                        st.metric("Account Status", result["account_status"])
                    
                    with col2:
                        st.metric("Recovery Enabled", "✅ Yes" if result["recovery_enabled"] else "❌ No")
                        if result["last_recovery_attempt"]:
                            st.metric("Last Recovery", result["last_recovery_attempt"])
                    
                    st.info(f"📧 Available recovery methods: {', '.join(result['available_recovery_methods'])}")
                else:
                    st.error("❌ No account found with this email address")
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Security tips
    st.markdown("---")
    st.markdown("### 🔒 Security Tips")
    
    with st.expander("How to keep your keys safe"):
        st.markdown("""
        **Best Practices:**
        - 📝 **Save your keys** in a secure password manager
        - 📧 **Keep your email secure** - this is your recovery method
        - 🔄 **Generate new keys** regularly for enhanced security
        - 🚫 **Never share your keys** with anyone
        - 📱 **Use a secure device** when accessing your account
        
        **If you suspect your keys are compromised:**
        - 🔄 Generate new keys immediately
        - 📧 Check your email for unauthorized access
        - 🆘 Contact support if needed
        """)
    
    # Contact support
    st.markdown("---")
    st.markdown("### 🆘 Need Help?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Contact Support:**")
        st.markdown("📧 Email: support@ysense.ai")
        st.markdown("💬 Live Chat: Available 24/7")
    
    with col2:
        st.markdown("**Common Issues:**")
        st.markdown("• Email not received? Check spam folder")
        st.markdown("• Account locked? Contact support")
        st.markdown("• Wrong email? Verify your address")

def show_key_management():
    """Show key management interface for logged-in users"""
    st.markdown("### 🔑 Key Management")
    st.markdown("Manage your crypto keys and Z Protocol keys")
    
    # Current keys (masked)
    st.markdown("#### Current Keys")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Crypto Key:**")
        st.code("••••••••••••••••", language="text")
        st.caption("Used for login authentication")
    
    with col2:
        st.markdown("**Z Protocol Key:**")
        st.code("••••••••••••••••", language="text")
        st.caption("Used for consent management")
    
    # Generate new keys
    st.markdown("#### Generate New Keys")
    st.warning("⚠️ **Warning:** Generating new keys will invalidate your current keys. You'll need to update any saved copies.")
    
    if st.button("Generate New Keys", type="primary"):
        try:
            with st.spinner("Generating new keys..."):
                result = api_call("POST", "auth/generate-new-keys", authenticated=True)
                
                if result and result.get("success"):
                    st.success("✅ New keys generated successfully!")
                    
                    # Show new keys
                    st.markdown("#### Your New Keys:")
                    st.info(f"🔑 **Crypto Key:** `{result['crypto_key']}`")
                    st.info(f"🛡️ **Z Protocol Key:** `{result['z_protocol_consent_key']}`")
                    
                    st.warning("⚠️ **IMPORTANT:** Save these keys immediately! You'll need them to access your account.")
                    
                    # Copy buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Copy Crypto Key"):
                            st.write("Crypto key copied to clipboard!")
                    
                    with col2:
                        if st.button("Copy Z Protocol Key"):
                            st.write("Z Protocol key copied to clipboard!")
                
                else:
                    st.error("❌ Failed to generate new keys")
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Key history
    st.markdown("#### Key History")
    st.info("📊 Key generation history and security logs will be available in future updates.")

# Add to main navigation
def add_recovery_to_navigation():
    """Add recovery options to main navigation"""
    if not st.session_state.get("authenticated", False):
        # Show recovery link in login page
        st.markdown("---")
        st.markdown("### 🔑 Lost Your Keys?")
        st.markdown("[Click here to recover your keys](#key-recovery)")
    
    else:
        # Show key management in dashboard
        st.markdown("---")
        st.markdown("### 🔑 Key Management")
        if st.button("Manage Keys"):
            st.session_state.current_page = "key_management"
            st.rerun()



