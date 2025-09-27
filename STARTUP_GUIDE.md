# 🚀 YSense Platform v3.0 - Startup Guide

## 📋 Prerequisites
- Python 3.9+ ✅ (You have Python 3.13.7)
- FastAPI ✅ (You have 0.116.2)
- Streamlit ✅ (You have 1.49.1)

## 🎯 Quick Start (2 Commands)

### Step 1: Start Backend API
```bash
python -m uvicorn src.main:app --port 8003
```

### Step 2: Start Frontend UI (in a new terminal)
```bash
streamlit run streamlit_app.py --server.port 8501
```

## 🌐 Access Your Platform
- **Frontend UI:** http://localhost:8501
- **Backend API:** http://localhost:8003
- **API Documentation:** http://localhost:8003/docs

## 🔑 What You'll Get

### For Users:
1. **Register** → Get Crypto Key + Z Protocol Consent Key
2. **Login** → Use Crypto Key (no passwords!)
3. **Create Wisdom** → Five-Layer Perception Toolkit
4. **Track Revenue** → 30-50% revenue sharing

### For You (Admin):
1. **Consent Management** → Find users by Z Protocol key
2. **Audit Trail** → Complete compliance logging
3. **Revenue Tracking** → Monitor platform earnings
4. **User Management** → Full user lifecycle

## 🛠️ Troubleshooting

### If Port Already in Use:
```bash
# Kill existing processes
taskkill /f /im python.exe

# Or use different ports
python -m uvicorn src.main:app --port 8004
streamlit run streamlit_app.py --server.port 8502
```

### If Database Issues:
```bash
# Delete old database (will recreate automatically)
del ysense_local.db
```

## 📊 System Status Check
```bash
# Check if backend is running
curl http://localhost:8003/health

# Check if frontend is running
curl http://localhost:8501
```

## 🎉 You're Ready to Launch!

Your platform is production-ready with:
- ✅ Crypto Key Authentication
- ✅ Z Protocol Consent Management
- ✅ Complete Audit Trail
- ✅ Revenue Tracking
- ✅ Multi-Jurisdiction Support
- ✅ Defensive Publication Protection

**Go change the world with ethical AI attribution!** 🌟



