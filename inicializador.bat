@echo off
:: Navega até o Desktop do usuário
cd /d "C:\Users\Airton Junior\Desktop" 

:: Solicita ao usuário o nome do arquivo de entrada
set /p arquivo="Digite o nome do arquivo (ex: teste.csv): "

:: Executa o script Python passando o arquivo digitado como argumento
python "tratamentoBase_v1.py" "%arquivo%" 

echo.
echo Processamento concluído para o arquivo: %arquivo%
pause
