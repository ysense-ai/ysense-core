@echo off
echo 🚀 YSense Platform v4.0 - GitHub Deployment Preparation
echo =====================================================
echo.

echo 📋 Creating deployment-ready codebase...
echo.

REM Create deployment folder
if not exist "YSense-v4.0-Deployment" mkdir "YSense-v4.0-Deployment"
cd "YSense-v4.0-Deployment"

echo ✅ Created deployment folder: YSense-v4.0-Deployment
echo.

REM Copy essential files
echo 📁 Copying essential files...

REM Core application files
xcopy "..\src" "src\" /E /I /H /Y
xcopy "..\api" "api\" /E /I /H /Y
xcopy "..\core" "core\" /E /I /H /Y
xcopy "..\scripts" "scripts\" /E /I /H /Y
xcopy "..\tests" "tests\" /E /I /H /Y
xcopy "..\docs" "docs\" /E /I /H /Y

REM Main application files
copy "..\streamlit_app.py" "streamlit_app.py"
copy "..\streamlit_v4_app.py" "streamlit_v4_app.py"
copy "..\requirements.txt" "requirements.txt"
copy "..\working_requirements.txt" "working_requirements.txt"

REM Configuration files
copy "..\docker-compose.yml" "docker-compose.yml"
if exist "..\.env" copy "..\.env" ".env"

REM Documentation
copy "..\README.md" "README.md"
copy "..\DEPLOYMENT_STRATEGY.md" "DEPLOYMENT_STRATEGY.md"

echo ✅ Essential files copied
echo.

REM Create GitHub-specific files
echo 📝 Creating GitHub-specific files...

REM Create .gitignore
echo # YSense Platform v4.0 - .gitignore > .gitignore
echo. >> .gitignore
echo # Python >> .gitignore
echo __pycache__/ >> .gitignore
echo *.py[cod] >> .gitignore
echo *$py.class >> .gitignore
echo *.so >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo wheels/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo. >> .gitignore
echo # Virtual Environment >> .gitignore
echo venv/ >> .gitignore
echo env/ >> .gitignore
echo ENV/ >> .gitignore
echo. >> .gitignore
echo # Database >> .gitignore
echo *.db >> .gitignore
echo *.sqlite >> .gitignore
echo *.sqlite3 >> .gitignore
echo. >> .gitignore
echo # Environment Variables >> .gitignore
echo .env >> .gitignore
echo .env.local >> .gitignore
echo .env.production >> .gitignore
echo. >> .gitignore
echo # IDE >> .gitignore
echo .vscode/ >> .gitignore
echo .idea/ >> .gitignore
echo *.swp >> .gitignore
echo *.swo >> .gitignore
echo. >> .gitignore
echo # OS >> .gitignore
echo .DS_Store >> .gitignore
echo Thumbs.db >> .gitignore
echo. >> .gitignore
echo # Logs >> .gitignore
echo *.log >> .gitignore
echo logs/ >> .gitignore
echo. >> .gitignore
echo # Temporary files >> .gitignore
echo *.tmp >> .gitignore
echo *.temp >> .gitignore
echo temp/ >> .gitignore
echo. >> .gitignore
echo # Backup files >> .gitignore
echo *.bak >> .gitignore
echo *.backup >> .gitignore
echo backup/ >> .gitignore

echo ✅ .gitignore created
echo.

REM Create defensive publication notice
echo 📄 Creating defensive publication notice...
echo # 🛡️ YSense Platform v4.0 - Defensive Publication Notice > DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo **This repository contains the source code for YSense Platform v4.0** >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo ## 📋 Defensive Publication Details >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo - **DOI**: 10.5281/zenodo.17072168 >> DEFENSIVE_PUBLICATION.md
echo - **Publication Date**: September 2024 >> DEFENSIVE_PUBLICATION.md
echo - **License**: Apache 2.0 >> DEFENSIVE_PUBLICATION.md
echo - **Purpose**: Defensive publication to prevent patent theft >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo ## 🎯 What This Protects >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo This defensive publication establishes prior art for: >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo 1. **AI Attribution Infrastructure** - The world's first system for attributing human wisdom in AI training >> DEFENSIVE_PUBLICATION.md
echo 2. **Z Protocol v2.0** - Ethical compliance framework for AI training data >> DEFENSIVE_PUBLICATION.md
echo 3. **Five-Layer Perception Toolkit** - Methodology for extracting human wisdom >> DEFENSIVE_PUBLICATION.md
echo 4. **Crypto Key Authentication** - Secure, passwordless authentication system >> DEFENSIVE_PUBLICATION.md
echo 5. **Revenue Distribution System** - Automated revenue sharing for wisdom contributors >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo ## ⚖️ Legal Protection >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo This defensive publication: >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo - **Prevents patent theft** by establishing prior art >> DEFENSIVE_PUBLICATION.md
echo - **Protects intellectual property** through open source publication >> DEFENSIVE_PUBLICATION.md
echo - **Enables commercial use** under Apache 2.0 license >> DEFENSIVE_PUBLICATION.md
echo - **Ensures attribution** through DOI reference >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo ## 🚀 Commercial Use >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo This code is released under Apache 2.0 license, which allows: >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo - ✅ Commercial use >> DEFENSIVE_PUBLICATION.md
echo - ✅ Modification >> DEFENSIVE_PUBLICATION.md
echo - ✅ Distribution >> DEFENSIVE_PUBLICATION.md
echo - ✅ Patent use >> DEFENSIVE_PUBLICATION.md
echo. >> DEFENSIVE_PUBLICATION.md
echo **For business inquiries, contact: ysenseai.org** >> DEFENSIVE_PUBLICATION.md

echo ✅ Defensive publication notice created
echo.

REM Create production README
echo 📖 Creating production README...
echo # 🚀 YSense Platform v4.0 - Production Deployment > README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo **The world's first AI attribution infrastructure for ethical AI training through human wisdom.** >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ## 🌐 Live Platform >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo - **Website**: https://ysenseai.org >> README_PRODUCTION.md
echo - **API**: https://api.ysenseai.org >> README_PRODUCTION.md
echo - **Documentation**: https://docs.ysenseai.org >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ## ✨ Features >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ### 🧠 AI-Powered Intelligence >> README_PRODUCTION.md
echo - **Orchestrator**: 7 intelligent agents powered by Anthropic Claude >> README_PRODUCTION.md
echo - **Layer Analyzer**: QWEN AI for deep wisdom analysis >> README_PRODUCTION.md
echo - **Dynamic Scoring**: Unique analysis per user input >> README_PRODUCTION.md
echo - **Revenue Calculation**: Market-aware pricing >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ### ⚖️ Ethical Compliance >> README_PRODUCTION.md
echo - **Z Protocol v2.0**: 100% compliance validation >> README_PRODUCTION.md
echo - **Crypto Key Authentication**: Secure, simple login >> README_PRODUCTION.md
echo - **Consent Management**: Complete GDPR/PDPA compliance >> README_PRODUCTION.md
echo - **Attribution Protection**: Immutable wisdom attribution >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ### 🌍 Cultural Sensitivity >> README_PRODUCTION.md
echo - **Cultural Multipliers**: Enhanced valuation for cultural context >> README_PRODUCTION.md
echo - **Malaysian Focus**: Special support for Malaysian wisdom >> README_PRODUCTION.md
echo - **Global Reach**: Universal human wisdom preservation >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ## 🚀 Quick Start >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ### Option 1: One-Click Launch >> README_PRODUCTION.md
echo ```bash >> README_PRODUCTION.md
echo # Double-click any of these files: >> README_PRODUCTION.md
echo LAUNCH_YSENSE.bat              # Standard launcher >> README_PRODUCTION.md
echo LAUNCH_YSENSE_SMART.bat        # Smart launcher (handles port conflicts) >> README_PRODUCTION.md
echo LAUNCH_YSENSE_MANUAL.bat       # Manual launcher (uses ports 8005/8503) >> README_PRODUCTION.md
echo ``` >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ### Option 2: Manual Launch >> README_PRODUCTION.md
echo ```bash >> README_PRODUCTION.md
echo # 1. Install dependencies >> README_PRODUCTION.md
echo pip install -r requirements.txt >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo # 2. Start backend >> README_PRODUCTION.md
echo python -m uvicorn src.main:app --port 8003 --reload >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo # 3. Start frontend (in new terminal) >> README_PRODUCTION.md
echo streamlit run streamlit_app.py --server.port 8501 >> README_PRODUCTION.md
echo ``` >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ## 🛡️ IP Protection >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo - **Defensive Publication**: DOI 10.5281/zenodo.17072168 >> README_PRODUCTION.md
echo - **License**: Apache 2.0 >> README_PRODUCTION.md
echo - **Attribution**: Permanent cryptographic attribution >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo ## 📞 Contact >> README_PRODUCTION.md
echo. >> README_PRODUCTION.md
echo - **Website**: https://ysenseai.org >> README_PRODUCTION.md
echo - **Email**: contact@ysenseai.org >> README_PRODUCTION.md
echo - **GitHub**: https://github.com/ysenseai-org >> README_PRODUCTION.md

echo ✅ Production README created
echo.

REM Create deployment scripts
echo 🔧 Creating deployment scripts...

REM Create GitHub initialization script
echo @echo off > init_github.bat
echo echo 🚀 Initializing GitHub repository... >> init_github.bat
echo echo. >> init_github.bat
echo git init >> init_github.bat
echo git add . >> init_github.bat
echo git commit -m "Initial commit: YSense Platform v4.0" >> init_github.bat
echo echo. >> init_github.bat
echo echo ✅ Repository initialized >> init_github.bat
echo echo. >> init_github.bat
echo echo Next steps: >> init_github.bat
echo echo 1. Create repository on GitHub >> init_github.bat
echo echo 2. Add remote: git remote add origin [REPO_URL] >> init_github.bat
echo echo 3. Push: git push -u origin main >> init_github.bat
echo pause >> init_github.bat

echo ✅ GitHub initialization script created
echo.

REM Create deployment launcher
echo @echo off > LAUNCH_YSENSE.bat
echo echo 🚀 YSense Platform v4.0 - Production Launch >> LAUNCH_YSENSE.bat
echo echo ========================================== >> LAUNCH_YSENSE.bat
echo echo. >> LAUNCH_YSENSE.bat
echo echo Starting YSense Platform v4.0... >> LAUNCH_YSENSE.bat
echo echo. >> LAUNCH_YSENSE.bat
echo echo Backend: http://localhost:8003 >> LAUNCH_YSENSE.bat
echo echo Frontend: http://localhost:8501 >> LAUNCH_YSENSE.bat
echo echo. >> LAUNCH_YSENSE.bat
echo start "YSense Backend" cmd /k "python -m uvicorn src.main:app --port 8003 --reload" >> LAUNCH_YSENSE.bat
echo timeout /t 3 /nobreak ^>nul >> LAUNCH_YSENSE.bat
echo start "YSense Frontend" cmd /k "streamlit run streamlit_app.py --server.port 8501" >> LAUNCH_YSENSE.bat
echo echo. >> LAUNCH_YSENSE.bat
echo echo ✅ YSense Platform v4.0 is starting! >> LAUNCH_YSENSE.bat
echo echo Access your platform at: http://localhost:8501 >> LAUNCH_YSENSE.bat
echo pause >> LAUNCH_YSENSE.bat

echo ✅ Deployment launcher created
echo.

echo 🎉 Deployment preparation complete!
echo =================================
echo.
echo 📁 Deployment folder: YSense-v4.0-Deployment
echo.
echo Next steps:
echo 1. Review the prepared files
echo 2. Run init_github.bat to initialize Git
echo 3. Create GitHub repositories
echo 4. Deploy to production
echo.
echo 📚 Documentation:
echo - DEPLOYMENT_STRATEGY.md (deployment guide)
echo - DEFENSIVE_PUBLICATION.md (IP protection)
echo - README_PRODUCTION.md (production README)
echo.
echo Ready for GitHub deployment! 🚀
echo.
pause


