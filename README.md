# 🚀 YSense Platform v4.0 - Clean Edition

**The world's first AI attribution infrastructure for ethical AI training through human wisdom.**

---

## 🎯 **What This Is**

This is a **clean, focused version** of YSense Platform v4.0 containing only the essential files needed to run the platform. Perfect for deployment, sharing, or starting fresh.

---

## ✨ **v4.0 Features**

### **🧠 AI-Powered Intelligence**
- **Orchestrator:** 7 intelligent agents powered by Anthropic Claude
- **Layer Analyzer:** QWEN AI for deep wisdom analysis
- **Dynamic Scoring:** Unique analysis per user input
- **Revenue Calculation:** Market-aware pricing

### **⚖️ Ethical Compliance**
- **Z Protocol v2.0:** 100% compliance validation
- **Crypto Key Authentication:** Secure, simple login
- **Consent Management:** Complete GDPR/PDPA compliance
- **Attribution Protection:** Immutable wisdom attribution

### **🌍 Cultural Sensitivity**
- **Cultural Multipliers:** Enhanced valuation for cultural context
- **Malaysian Focus:** Special support for Malaysian wisdom
- **Global Reach:** Universal human wisdom preservation

---

## 🚀 **Quick Start**

### **Option 1: One-Click Launch (Recommended)**
```bash
# Double-click any of these files:
LAUNCH_YSENSE.bat              # Standard launcher
LAUNCH_YSENSE_SMART.bat        # Smart launcher (handles port conflicts)
LAUNCH_YSENSE_MANUAL.bat       # Manual launcher (uses ports 8005/8503)
```

### **Option 2: Manual Launch**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend
python -m uvicorn src.main:app --port 8003 --reload

# 3. Start frontend (in new terminal)
streamlit run streamlit_app.py --server.port 8501
```

---

## 📁 **Project Structure**

```
YSense-Platform-v4.0-Clean/
├── src/                          # Core application code
│   ├── main.py                   # FastAPI application
│   ├── models.py                 # Database models
│   ├── config.py                 # Configuration
│   ├── orchestrator.py           # AI orchestrator (Anthropic)
│   ├── layer_analyzer.py         # Wisdom analyzer (QWEN)
│   ├── anthropic_integration.py  # Anthropic API client
│   ├── qwen_integration.py       # QWEN API client
│   └── z_protocol_enhanced.py    # Z Protocol v2.0
├── api/                          # API endpoints
│   ├── auth.py                   # Authentication
│   ├── wisdom.py                 # Wisdom management
│   ├── revenue.py                # Revenue system
│   └── legal.py                  # Legal compliance
├── core/                         # Core utilities
│   └── mcp_integration.py        # MCP integration
├── scripts/                      # Utility scripts
├── tests/                        # Test files
├── docs/                         # Documentation
├── streamlit_app.py              # Frontend application
├── requirements.txt              # Python dependencies
├── LAUNCH_YSENSE.bat             # One-click launcher
├── LAUNCH_YSENSE_SMART.bat       # Smart launcher
├── LAUNCH_YSENSE_MANUAL.bat      # Manual launcher
└── README.md                     # This file
```

---

## 🌐 **Access Your Platform**

Once launched, access your platform at:

- **🌐 Frontend UI:** http://localhost:8501
- **🚀 Backend API:** http://localhost:8003
- **📚 API Documentation:** http://localhost:8003/docs

---

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:

```bash
# AI API Keys (optional - fallback mode available)
ANTHROPIC_API_KEY=your_anthropic_key_here
QWEN_API_KEY=your_qwen_key_here

# Database
DATABASE_URL=sqlite:///./ysense_local.db

# Security
SECRET_KEY=your_secret_key_here
```

### **API Keys (Optional)**
- **Without API keys:** Platform runs in fallback mode with basic functionality
- **With API keys:** Full AI-powered analysis and intelligence

---

## 🎯 **How to Use**

### **1. Register/Login**
- Register with email and username
- Save your generated crypto key securely
- Note your Z Protocol consent key

### **2. Create Wisdom**
- Tell your story naturally
- AI analyzes with 7 intelligent agents
- Get quality score and revenue potential
- Cultural context automatically detected

### **3. View Analytics**
- Track your wisdom collection
- Monitor revenue potential
- View quality scores
- Manage consent settings

---

## 🛠️ **Troubleshooting**

### **Port Already in Use**
```bash
# Use the smart launcher
LAUNCH_YSENSE_SMART.bat

# Or use manual launcher (different ports)
LAUNCH_YSENSE_MANUAL.bat
```

### **Python Not Found**
- Install Python 3.8+ from https://python.org
- Make sure to check "Add Python to PATH"

### **Package Installation Issues**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

---

## 🎉 **What's New in v4.0**

### **✅ AI Integration Complete**
- All 7 orchestrator agents use Anthropic Claude
- Layer analyzer uses QWEN AI for deep analysis
- Dynamic quality scoring based on content
- Market-aware revenue calculation

### **✅ Enhanced User Experience**
- Unique analysis for every user input
- Cultural sensitivity and multipliers
- Fair, dynamic pricing system
- One-click launch options

### **✅ Production Ready**
- Fallback modes when APIs unavailable
- Comprehensive error handling
- Complete audit trails
- Legal compliance framework

---

## 🚀 **Ready to Launch!**

**Your clean YSense Platform v4.0 is ready to revolutionize ethical AI through human wisdom attribution!**

**Just double-click `LAUNCH_YSENSE.bat` and you're ready to go!** 🌟

---

## 📞 **Support**

For issues or questions:
1. Check the troubleshooting section above
2. Review the API documentation at http://localhost:8003/docs
3. Check the terminal/command windows for error messages

---

**Built with ❤️ in Teluk Intan, Malaysia 🇲🇾**