@echo off
echo ===================================
echo       INICIANDO API FAQ - v1.0
echo ===================================
echo.

REM Configurar codepage para UTF-8 e executar silenciosamente
start cmd.exe /k "chcp 65001 > nul && call venv\Scripts\activate && cd menu_interativo && python api/faq_api.py"
