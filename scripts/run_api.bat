@echo off
start cmd.exe /k "chcp 65001 > nul && call venv\Scripts\activate && cd menu_interativo && python api/faq_api.py"
