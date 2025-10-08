# YSense™ Live Demo Mode Setup Guide

## 🎬 Overview

Your platform now has **Live Demo Mode** - real AI analysis with no data persistence!

---

## ✅ What's Been Implemented

### 1. **Live Demo Mode Configuration** (`src/demo_mode_config.py`)
- ✅ Real AI API activation setting
- ✅ Session-only storage (no database)
- ✅ Usage limits (10 analyses per session, 30-sec cooldown)
- ✅ Character limit (2000 chars per story)
- ✅ Clear disclaimers and warnings

### 2. **AI Workflow Integration** (`streamlit_app.py`)
- ✅ Demo banner on AI Workflow page
- ✅ Usage counter display
- ✅ Story length validation
- ✅ Rate limiting
- ✅ Session-only result storage
- ✅ Database save blocking

### 3. **Privacy & Warnings**
- ✅ Updated privacy policy with AI API disclosure
- ✅ Logout confirmation when data exists
- ✅ Sidebar data loss warnings
- ✅ Clear "no persistence" messaging

### 4. **Mobile Responsiveness**
- ✅ Responsive CSS for tablets (≤768px)
- ✅ Responsive CSS for phones (≤480px)
- ✅ Full-width buttons on mobile
- ✅ Stacked columns on small screens
- ✅ Proper viewport meta tag

---

## 🚀 How to Activate Live Demo Mode

### Step 1: Verify Your API Keys

Check your `.env` file:

```bash
# QWEN API (Alibaba Cloud)
QWEN_API_KEY=sk-9f933e251786491bba21a0ddb3c417d1
QWEN_MODEL=qwen-plus

# Anthropic API (Claude)
ANTHROPIC_API_KEY=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
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**⚠️ Important:**
- These keys may be expired or invalid
- You need to verify they have API credits
- Replace with fresh keys if needed

### Step 2: Test API Keys

```bash
# Test QWEN API
python src/qwen_integration.py

# Test Anthropic API
python src/anthropic_integration.py
```

If APIs work, you'll see real responses. If not, update your keys.

### Step 3: Configure Demo Mode

Edit `src/demo_mode_config.py`:

```python
class LiveDemoMode:
    # Core settings
    ENABLED = True  # ✅ Already set to True
    NAME = "Live AI Demo Mode"

    # AI API settings
    USE_REAL_AI_APIS = True  # ✅ Set this to True for real AI
    ANTHROPIC_ENABLED = True
    QWEN_ENABLED = True

    # Data persistence settings
    SAVE_TO_DATABASE = False  # ✅ No database saves
    SESSION_ONLY_STORAGE = True  # ✅ Session only
    AUTO_CLEAR_ON_REFRESH = True  # ✅ Clear on refresh
    AUTO_CLEAR_ON_LOGOUT = True  # ✅ Clear on logout

    # Demo limitations
    MAX_ANALYSES_PER_SESSION = 10  # Adjust if needed
    MAX_STORY_LENGTH = 2000  # Character limit
    RATE_LIMIT_SECONDS = 30  # Cooldown between analyses
```

### Step 4: Restart the Platform

```bash
streamlit run streamlit_app.py
```

---

## 💰 Cost Considerations

### API Costs per Analysis:
- **Anthropic Claude**: ~$0.03 per analysis
- **QWEN**: ~$0.01 per analysis
- **Total**: ~$0.04 per demo session

### With Current Limits:
- Max 10 analyses per session = **$0.40 max per user**
- 30-second cooldown prevents spam
- 2000 character limit reduces token usage

### Monthly Cost Estimates:
- **100 users/month**: ~$40
- **500 users/month**: ~$200
- **1000 users/month**: ~$400

**💡 Tip:** Monitor your API usage dashboards:
- Anthropic: https://console.anthropic.com/
- Alibaba Cloud: https://dashscope.aliyun.com/

---

## 🎯 What Users Will Experience

### On AI Workflow Page:
1. **Demo Banner**: Clear warning about temporary storage
2. **Expandable Disclaimer**: Full explanation of demo mode
3. **Usage Counter**: Shows remaining analyses (e.g., "7/10 remaining")
4. **Real AI Analysis**: Actual processing by Claude & QWEN
5. **Session Results**: Results displayed but not saved to database
6. **Clear Warnings**: Reminders that data is temporary

### On Logout/Refresh:
1. **Warning**: "All analysis results will be lost!"
2. **Confirmation**: Must confirm logout if data exists
3. **Auto-Clear**: All session data deleted
4. **Fresh Start**: Next visit starts with clean session

---

## 🔒 Privacy Compliance

### What's Disclosed:
✅ AI APIs process user input
✅ Data sent to Anthropic & Alibaba Cloud
✅ Subject to their privacy policies
✅ Session-only storage (no database)
✅ Data deleted on refresh/logout

### Privacy Policy Updated:
- Section 4: AI API data processing
- Section 6: Third-party services (AI providers)
- Clear links to Anthropic & QWEN privacy policies

### User Responsibilities:
⚠️ Don't enter sensitive personal information
⚠️ Understand data is temporary
⚠️ Review AI provider privacy policies
⚠️ Use for demonstration purposes only

---

## 📱 Mobile Optimization

### What's Fixed:
✅ Responsive layout for tablets (≤768px)
✅ Responsive layout for phones (≤480px)
✅ Properly sized fonts on all devices
✅ Full-width buttons on mobile
✅ Stacked columns on small screens
✅ Viewport meta tag for proper scaling
✅ No horizontal scrolling
✅ Touch-friendly interface

### Test On:
- iPhone/Android phones
- iPad/Android tablets
- Different orientations
- Various screen sizes

---

## 🛠️ Configuration Options

### To Disable Live Demo Mode:

Edit `src/demo_mode_config.py`:
```python
ENABLED = False  # Disables all demo mode features
```

### To Use Fallback Mode (No API Costs):

Edit `src/demo_mode_config.py`:
```python
USE_REAL_AI_APIS = False  # Uses mock responses instead
```

### To Adjust Limits:

Edit `src/demo_mode_config.py`:
```python
MAX_ANALYSES_PER_SESSION = 20  # More analyses per user
MAX_STORY_LENGTH = 5000  # Longer stories allowed
RATE_LIMIT_SECONDS = 10  # Faster cooldown
```

### To Enable Database Saves:

⚠️ **Not recommended for demo!** But if needed:
```python
SAVE_TO_DATABASE = True  # Enables permanent storage
```

---

## 🎬 Demo Mode Flow

### User Journey:

1. **Visit Platform** → See prototype banner
2. **Try Demo Login** → Access with demo credentials
3. **Navigate to AI Workflow** → See live demo banner
4. **Read Disclaimer** → Understand temporary nature
5. **Enter Story** → Max 2000 characters
6. **Click Analyze** → Real AI processing
7. **View Results** → Session-only storage
8. **See Warning** → Reminded data is temporary
9. **Logout/Refresh** → All data deleted
10. **Fresh Session** → Clean start

---

## 🐛 Troubleshooting

### Issue: AI Analysis Not Working
**Solution:**
1. Check API keys are valid
2. Verify API credits available
3. Test with `python src/anthropic_integration.py`
4. Check `.env` file format

### Issue: "Fallback Mode" Messages
**Solution:**
1. API keys likely invalid/expired
2. Get new keys from provider dashboards
3. Update `.env` file
4. Restart platform

### Issue: Mobile Display Problems
**Solution:**
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Test in incognito mode
4. Check viewport is not zoomed

### Issue: Rate Limit Errors
**Solution:**
1. Wait 30 seconds between analyses
2. Don't spam the analyze button
3. Check usage counter

---

## 📊 Monitoring

### What to Monitor:

1. **API Usage**:
   - Anthropic Console: token usage, costs
   - Alibaba Cloud Dashboard: API calls, quotas

2. **User Behavior**:
   - How many analyses per session?
   - Average story length?
   - Rate limit hits?

3. **Platform Performance**:
   - Response times
   - Error rates
   - Mobile vs desktop usage

---

## 🎉 Ready to Launch!

Your platform is now configured as a **Live AI Demo** with:

✅ Real AI analysis (when API keys are valid)
✅ Clear "demo only" messaging
✅ No permanent data storage
✅ Privacy-compliant disclosures
✅ Mobile-responsive design
✅ Usage limits to control costs
✅ Session-only storage
✅ Clear data deletion warnings

**Next Steps:**

1. ✅ Verify API keys are valid and funded
2. ✅ Test on multiple devices (phone, tablet, desktop)
3. ✅ Monitor API costs in first few days
4. ✅ Gather user feedback
5. ✅ Adjust limits based on usage patterns

---

## 📞 Support

For questions about Live Demo Mode:
- Email: alton@ysenseai.org
- Check API provider documentation for API issues

---

**Last Updated:** 2025-10-08
**Version:** Live Demo Mode v1.0
**Status:** ✅ Ready for Deployment
