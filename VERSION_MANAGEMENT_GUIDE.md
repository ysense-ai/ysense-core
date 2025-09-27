# 🎯 **YSense Platform Version Management - Quick Reference**

## 📋 **Current Setup (v3.0 Demo)**

### **Access Points:**
- **Frontend:** http://localhost:8501
- **Backend:** http://localhost:8003
- **API Docs:** http://localhost:8003/docs
- **Database:** `ysense_local.db`

### **Start Commands:**
```bash
# Smart startup (recommended)
.\start_ysense_smart.bat

# Manual startup
python -m uvicorn src.main:app --port 8003
streamlit run streamlit_app.py --server.port 8501
```

## 🚀 **v4.0 Development Setup**

### **Step 1: Backup v3.0 Demo**
```bash
.\backup_v3_demo.bat
```

### **Step 2: Create v4.0 Development Environment**
```bash
.\setup_v4_development.bat
```

### **Step 3: Start v4.0 Development**
```bash
cd YSense_v4.0_Development
python -m uvicorn src.main:app --port 8004
streamlit run streamlit_app.py --server.port 8502
```

## 📊 **Version Comparison**

| Feature | v3.0 Demo | v4.0 Dev |
|---------|-----------|----------|
| **Port (Backend)** | 8003 | 8004 |
| **Port (Frontend)** | 8501 | 8502 |
| **Database** | ysense_local.db | ysense_v4_dev.db |
| **Purpose** | Demo/Stable | Development |
| **Changes** | None | New features |

## 🛠️ **Development Workflow**

### **Daily Work:**
1. **v3.0 Demo:** Keep running for presentations
2. **v4.0 Dev:** Develop new features
3. **Testing:** Test v4.0 thoroughly
4. **Backup:** Regular backups of both versions

### **Feature Development:**
1. **Plan:** Define v4.0 features
2. **Develop:** Implement in v4.0 environment
3. **Test:** Thorough testing
4. **Deploy:** Move to production when ready

## 🎯 **Benefits of This Approach**

### **✅ Preserve v3.0 Demo**
- Stable demonstration environment
- No risk of breaking current functionality
- Client presentations continue uninterrupted

### **✅ Safe v4.0 Development**
- Isolated development environment
- No impact on demo version
- Easy rollback if needed

### **✅ Professional Workflow**
- Version control
- Backup strategy
- Isolated environments
- Clear separation of concerns

## 🚨 **Important Notes**

### **⚠️ Port Conflicts:**
- v3.0 uses ports 8003/8501
- v4.0 uses ports 8004/8502
- Never run both simultaneously on same ports

### **⚠️ Database Separation:**
- v3.0 demo data stays in `ysense_local.db`
- v4.0 dev data goes to `ysense_v4_dev.db`
- No data mixing between versions

### **⚠️ Configuration:**
- Each version has its own configuration
- Port numbers are hardcoded in each version
- Update both if changing ports

## 🎉 **Ready to Upgrade!**

**You now have:**
- ✅ Stable v3.0 demo preserved
- ✅ Isolated v4.0 development environment
- ✅ Clear upgrade path
- ✅ Professional version management

**Start developing v4.0 features while keeping your v3.0 demo running!** 🚀



