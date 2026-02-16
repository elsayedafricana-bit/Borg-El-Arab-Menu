@echo off
cd /d "%~dp0"
python -m streamlit run menu_app.py --global.developmentMode=false
pause