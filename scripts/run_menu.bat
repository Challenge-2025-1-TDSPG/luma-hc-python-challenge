@echo off
start cmd.exe /k "chcp 65001 > nul && call venv\Scripts\activate && python menu_interativo/main.py"
