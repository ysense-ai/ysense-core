# 🚀 YSense Platform v4.0 - One-Click Launch

**Choose your preferred launch method:**

## 🖱️ **Option 1: Double-Click Launch (Recommended)**

### **Windows:**
- **Batch File:** Double-click `launch_ysense_v4.bat`
- **PowerShell:** Right-click `launch_ysense_v4.ps1` → "Run with PowerShell"

### **Cross-Platform:**
- **Python Script:** Double-click `launch_ysense_v4.py` (requires Python)

---

## ⌨️ **Option 2: Command Line Launch**

### **Windows:**
```cmd
# Batch file
launch_ysense_v4.bat

# PowerShell
.\launch_ysense_v4.ps1

# Python script
python launch_ysense_v4.py
```

### **Mac/Linux:**
```bash
# Python script
python3 launch_ysense_v4.py

# Or make executable and run
chmod +x launch_ysense_v4.py
./launch_ysense_v4.py
```

---

## 🎯 **What Happens When You Launch:**

1. ✅ **Checks Python** - Verifies Python 3.8+ is installed
2. ✅ **Creates Virtual Environment** - Sets up isolated Python environment
3. ✅ **Installs Dependencies** - Installs all required packages
4. ✅ **Creates Database** - Initializes SQLite database
5. ✅ **Starts Backend** - Launches FastAPI on port 8003
6. ✅ **Starts Frontend** - Launches Streamlit on port 8501
7. ✅ **Opens Browser** - Automatically opens the platform

---

## 🌐 **Access Your Platform:**

- **Frontend UI:** http://localhost:8501
- **Backend API:** http://localhost:8003
- **API Documentation:** http://localhost:8003/docs

---

## 🛑 **To Stop the Platform:**

1. **Close the terminal/command windows** that opened
2. **Or press Ctrl+C** in each window
3. **Or close the browser tabs**

---

## 🔧 **Troubleshooting:**

### **If Python is not found:**
- Install Python 3.8+ from https://python.org
- Make sure to check "Add Python to PATH" during installation

### **If virtual environment fails:**
- Make sure you have write permissions in the project folder
- Try running as administrator (Windows) or with sudo (Mac/Linux)

### **If ports are busy:**
- Close other applications using ports 8003 or 8501
- Or modify the port numbers in the launch scripts

### **If packages fail to install:**
- Check your internet connection
- Try running: `pip install --upgrade pip`
- Then run the launcher again

---

## 🎉 **Ready to Launch!**

**Choose any method above and launch YSense Platform v4.0 with a single click!**

**Your AI-powered, ethically compliant wisdom attribution platform is ready to go!** 🚀



