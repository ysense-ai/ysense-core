# src/demo_mode_config.py
"""
YSense™ Live Demo Mode Configuration
Enables real AI analysis while maintaining clear demo status with no data persistence
"""

class LiveDemoMode:
    """Configuration for Live Demo Mode with real AI but no data persistence"""

    # Core settings
    ENABLED = True
    NAME = "Live AI Demo Mode"

    # AI API settings
    USE_REAL_AI_APIS = True  # Set to True to activate real API calls
    ANTHROPIC_ENABLED = True
    QWEN_ENABLED = True

    # Data persistence settings
    SAVE_TO_DATABASE = False  # Never save demo data to database
    SESSION_ONLY_STORAGE = True  # Only store in session state
    AUTO_CLEAR_ON_REFRESH = True  # Clear all data on page refresh
    AUTO_CLEAR_ON_LOGOUT = True  # Clear all data on logout

    # User data collection
    COLLECT_USER_INFO = False  # No personal information collected
    ANONYMOUS_MODE = True  # All users are anonymous
    TRACK_ANALYTICS = False  # No analytics tracking in demo

    # Content retention
    CONTENT_RETENTION_MINUTES = 0  # 0 = session only, cleared on refresh
    STORE_ANALYSIS_RESULTS = False  # Don't store analysis results permanently

    # Demo disclaimers
    SHOW_DEMO_BANNER = True
    SHOW_DATA_WARNING = True
    SHOW_API_COST_WARNING = True

    # Demo limitations
    MAX_ANALYSES_PER_SESSION = 10  # Limit to prevent API abuse
    MAX_STORY_LENGTH = 2000  # Character limit for demo
    RATE_LIMIT_SECONDS = 30  # Minimum seconds between analyses

    @classmethod
    def get_demo_disclaimer(cls) -> str:
        """Get the demo mode disclaimer text"""
        return """
        ⚠️ **LIVE DEMO MODE - IMPORTANT NOTICE**

        **This is a demonstration platform with real AI analysis:**

        ✅ **What Works:**
        - Real AI analysis powered by Anthropic Claude & QWEN
        - Full 3-stage methodology demonstration
        - Complete workflow experience

        ⚠️ **What You Should Know:**
        - **NO data is permanently stored** - all content is lost on refresh/logout
        - **NO user information is collected** - completely anonymous
        - **Session-only storage** - results exist only in your current session
        - **Demo purposes only** - not for production use

        🔒 **Privacy Guarantee:**
        - Your input is sent to AI APIs for analysis only
        - No database storage of your content
        - No tracking or analytics
        - Content cleared immediately on page refresh

        **By using this demo, you acknowledge that all content is temporary and will be lost.**
        """

    @classmethod
    def get_data_warning(cls) -> str:
        """Get warning before refresh/logout"""
        return """
        ⚠️ **WARNING: All Your Data Will Be Lost!**

        This is a **DEMO PLATFORM** with **NO DATA PERSISTENCE**.

        **If you refresh this page or logout:**
        - All analysis results will be deleted
        - All input content will be lost
        - No data is saved to any database

        **To keep your results:**
        1. Copy/paste analysis results to a local file
        2. Take screenshots of important findings
        3. Save content to your own storage

        **This is by design for privacy and demo purposes.**
        """

    @classmethod
    def get_api_cost_notice(cls) -> str:
        """Get API cost notice for platform owner"""
        return """
        💰 **API COST NOTICE (Platform Owner)**

        **Live Demo Mode is ACTIVE with real API calls:**
        - Each analysis consumes API credits
        - Anthropic Claude: ~$0.03 per analysis
        - QWEN: ~$0.01 per analysis
        - Total: ~$0.04 per demo session

        **Current Limits:**
        - Max 10 analyses per session
        - 30-second cooldown between analyses
        - 2000 character story limit

        **Monitor your API usage to control costs!**
        """

    @classmethod
    def should_use_real_api(cls) -> bool:
        """Check if real API should be used"""
        return cls.ENABLED and cls.USE_REAL_AI_APIS

    @classmethod
    def should_save_to_database(cls) -> bool:
        """Check if data should be saved to database"""
        return not cls.ENABLED or cls.SAVE_TO_DATABASE

    @classmethod
    def get_session_storage_key(cls) -> str:
        """Get session storage key prefix"""
        return "demo_session_"

    @classmethod
    def validate_demo_limits(cls, session_state) -> dict:
        """Validate demo usage limits"""
        analyses_count = session_state.get('demo_analyses_count', 0)
        last_analysis_time = session_state.get('demo_last_analysis_time', 0)

        import time
        current_time = time.time()

        # Check max analyses limit
        if analyses_count >= cls.MAX_ANALYSES_PER_SESSION:
            return {
                'allowed': False,
                'reason': f'Demo limit reached: {cls.MAX_ANALYSES_PER_SESSION} analyses per session',
                'message': 'Please refresh to start a new demo session'
            }

        # Check rate limit
        time_since_last = current_time - last_analysis_time
        if last_analysis_time > 0 and time_since_last < cls.RATE_LIMIT_SECONDS:
            remaining = int(cls.RATE_LIMIT_SECONDS - time_since_last)
            return {
                'allowed': False,
                'reason': f'Rate limit: Please wait {remaining} seconds',
                'message': f'You can run another analysis in {remaining} seconds'
            }

        return {'allowed': True}

    @classmethod
    def increment_usage(cls, session_state):
        """Increment demo usage counters"""
        import time
        session_state['demo_analyses_count'] = session_state.get('demo_analyses_count', 0) + 1
        session_state['demo_last_analysis_time'] = time.time()

    @classmethod
    def clear_session_data(cls, session_state):
        """Clear all demo session data"""
        keys_to_clear = [key for key in session_state.keys() if key.startswith('demo_')]
        for key in keys_to_clear:
            del session_state[key]

        # Clear analysis results
        if 'methodology_results' in session_state:
            del session_state['methodology_results']
        if 'wisdom_results' in session_state:
            del session_state['wisdom_results']

# Global instance
live_demo_mode = LiveDemoMode()
