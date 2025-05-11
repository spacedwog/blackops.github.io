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
Write-Host "║ [2] Configurações                             ║" -ForegroundColor Yellow
Write-Host "║ [3] Relatórios                                ║" -ForegroundColor Yellow
Write-Host "║ [4] Sair                                      ║" -ForegroundColor Yellow
Write-Host "╚$border╝" -ForegroundColor Cyan

$opcao = Read-Host "`nDigite a opção desejada"

switch ($opcao) {
    "1" {
        Write-Host "`n[✔] Sistema iniciado com sucesso!" -ForegroundColor Green
    }
    "2" {
        Write-Host "`n--- Configurações ---"
        Write-Host "1. Ajustes de Interface"
        Write-Host "2. Rede"
        Write-Host "3. Usuários"
        Write-Host "4. Voltar"
        $subop = Read-Host "Escolha uma subopção"
        Write-Host "Você escolheu a opção: $subop" -ForegroundColor Magenta
    }
    "3" {
        Write-Host "`n[📊] Gerando relatórios..." -ForegroundColor Blue
    }
    "4" {
        Write-Host "`n[⚠] Encerrando sistema..." -ForegroundColor Red
        exit
    }
    Default {
        Write-Host "`n[!] Opção inválida." -ForegroundColor Red
    }
}
