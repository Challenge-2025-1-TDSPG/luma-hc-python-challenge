@echo off
echo ===================================
echo     SETUP E TESTE DO SISTEMA FAQ
echo ===================================
echo.

echo [1/3] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [2/3] Testando importacoes...
cd menu_interativo
python -c "from api_externa import ApiExternaQuotes; print('✓ API Externa importada com sucesso')"
python -c "from banco import FaqDB; print('✓ Banco importado com sucesso')"
python -c "from exportacao import MenuExportacao; print('✓ Exportacao importada com sucesso')"

echo.
echo [3/3] Sistema pronto para uso!
echo Execute run_menu.bat para iniciar o menu interativo
echo Execute run_api.bat para iniciar a API REST
echo.
pause