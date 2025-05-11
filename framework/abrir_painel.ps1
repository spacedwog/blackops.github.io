@"
Clear-Host
$border = "═" * 50
$space = " " * 48

Write-Host ""
Write-Host "╔$border╗" -ForegroundColor Cyan
Write-Host "║$space║" -ForegroundColor Cyan
Write-Host "║           SISTEMA DE GERENCIAMENTO           ║" -ForegroundColor Cyan
Write-Host "║               -= Painel V1.0 =-              ║" -ForegroundColor Cyan
Write-Host "║$space║" -ForegroundColor Cyan
Write-Host "╠$border╣" -ForegroundColor Cyan

Write-Host "║ [1] Iniciar Sistema                           ║" -ForegroundColor Yellow
Write-Host "║ [2] Configuracoes                             ║" -ForegroundColor Yellow
Write-Host "║ [3] Relatorios                                ║" -ForegroundColor Yellow
Write-Host "║ [4] Sair                                      ║" -ForegroundColor Yellow
Write-Host "╚$border╝" -ForegroundColor Cyan

\$opcao = Read-Host "`nDigite a opcao desejada"

switch (\$opcao) {
    "1" {
        Write-Host "`n[✔] Sistema iniciado com sucesso!" -ForegroundColor Green
    }
    "2" {
        Write-Host "`n--- Configuracoes ---"
        Write-Host "1. Ajustes de Interface"
        Write-Host "2. Rede"
        Write-Host "3. Usuarios"
        Write-Host "4. Voltar"
        \$subop = Read-Host "Escolha uma subopcao"
        Write-Host "Voce escolheu a opcao: \$subop" -ForegroundColor Magenta
    }
    "3" {
        Write-Host "`n[Relatorio] Gerando relatorios..." -ForegroundColor Blue
    }
    "4" {
        Write-Host "`n[Saida] Encerrando sistema..." -ForegroundColor Red
        exit
    }
    Default {
        Write-Host "`n[!] Opcao invalida." -ForegroundColor Red
    }
}
"@ | Out-File -FilePath .\abrir_painel.ps1 -Encoding utf8