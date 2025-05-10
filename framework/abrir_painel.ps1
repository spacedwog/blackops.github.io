# abrir_painel.ps1

Write-Host "Iniciando Painel Tecnológico no navegador..."
Start-Process "http://localhost:8502"
streamlit run .\painel_tecnologico.py