@echo off
title DeckMaster - PPT Generator
color 0A

echo.
echo ============================================================
echo 🚀 DeckMaster - AI-Powered PPT Generator
echo ============================================================
echo.
echo ✅ WEBSITE FEATURES:
echo    - Complete PPT generation with real backend API
echo    - 60+ professional design styles
echo    - Visual elements (charts, tables, images)
echo    - 4 subscription plans (Free, Elite, Pro, Premium)
echo    - Admin mode for unlimited access
echo.
echo 🤖 AI GENERATION MODES:
echo    - DEMO MODE: Works without Ollama (basic slides)
echo    - FULL AI MODE: Requires Ollama (intelligent content)
echo.
echo 📋 TO ENABLE FULL AI GENERATION:
echo    1. Install Ollama: https://ollama.ai
echo    2. Run: ollama run qwen2.5:7b-instruct
echo    3. Keep Ollama running in background
echo.

REM Kill any existing processes
taskkill /f /im python.exe >nul 2>&1

echo Starting DeckMaster server...
echo.
venv\Scripts\python.exe app.py

pause