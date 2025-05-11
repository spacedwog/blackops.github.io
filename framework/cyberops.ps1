function Show-Panel {
    Clear-Host
    $width = 80
    $border = "═" * $width
    $space = " " * ($width - 2)

    # Estilo Cyberpunk: Cores neon e fontes contrastantes
    Write-Host ""
    Write-Host "╔$border╗" -ForegroundColor Cyan
    Write-Host "║$space║" -ForegroundColor Cyan
    Write-Host "║$(CenterText 'SISTEMA DE GERENCIAMENTO | DASHBOARD V1.0' $width)║" -ForegroundColor Magenta
    Write-Host "║$(CenterText 'INICIANDO...' $width)║" -ForegroundColor Cyan
    Write-Host "║$space║" -ForegroundColor Cyan
    Write-Host "╠$border╣" -ForegroundColor Cyan

    Write-Host "║$(CenterText '[1] Iniciar | [2] Configurações | [3] Relatórios | [4] Sair' $width)║" -ForegroundColor Green
    Write-Host "╚$border╝" -ForegroundColor Cyan
}

function CenterText($text, $width) {
    $pad = [math]::Max(0, ($width - 2 - $text.Length) / 2)
    return (" " * $pad) + $text + (" " * $pad)
}

function Show-SubmenuConfig {
    $configOptions = @(
        "1. Interface (Neon)",
        "2. Rede (Cyberlink)",
        "3. Usuários (Admin)",
        "4. Voltar"
    )
    Show-Submenu -title "Menu: Configurações" -options $configOptions
}

function Show-SubmenuReports {
    $reportOptions = @(
        "1. Relatório Diário",
        "2. Relatório Semanal",
        "3. Relatório Mensal",
        "4. Voltar"
    )
    Show-Submenu -title "Menu: Relatórios" -options $reportOptions
}

function Show-Submenu {
    param (
        [string]$title,
        [string[]]$options
    )

    # Exibição do submenu com cores e estilo futurista
    Write-Host "`n╔═════════════════════ $title ═════════════════════╗" -ForegroundColor Magenta
    foreach ($option in $options) {
        Write-Host ("║  " + $option.PadRight(45) + "║") -ForegroundColor Green
    }
    Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Magenta
}

# Função para exibir as opções no estilo cyberpunk
do {
    Show-Panel
    $opcao = Read-Host "`nSelecione uma opção"

    switch ($opcao) {
        "1" {
            Write-Host "`n✔ Sistema iniciado com sucesso!" -ForegroundColor Green
            Pause
        }
        "2" {
            Show-SubmenuConfig
            $sub = Read-Host "`nEscolha uma opção de Configuração"

            switch ($sub) {
                "1" { Write-Host "`n🎨 Interface configurada com estilo Neon!" -ForegroundColor Cyan }
                "2" { Write-Host "`n🌐 Rede conectada no Cyberlink!" -ForegroundColor Yellow }
                "3" { Write-Host "`n👥 Usuários administrados com sucesso." -ForegroundColor Magenta }
                "4" { Write-Host "`nVoltando..." -ForegroundColor DarkGray }
                Default { Write-Host "`n[!] Opção inválida." -ForegroundColor Red }
            }
            Pause
        }
        "3" {
            Show-SubmenuReports
            $sub = Read-Host "`nEscolha uma opção de Relatório"

            switch ($sub) {
                "1" { Write-Host "`n📅 Relatório Diário gerado com sucesso!" -ForegroundColor Cyan }
                "2" { Write-Host "`n📈 Relatório Semanal gerado!" -ForegroundColor Blue }
                "3" { Write-Host "`n📊 Relatório Mensal disponível!" -ForegroundColor Magenta }
                "4" { Write-Host "`nVoltando..." -ForegroundColor DarkGray }
                Default { Write-Host "`n[!] Opção inválida." -ForegroundColor Red }
            }
            Pause
        }
        "4" {
            Write-Host "`n⚠ Encerrando o sistema..." -ForegroundColor Red
            break
        }
        Default {
            Write-Host "`n[!] Opção inválida." -ForegroundColor Red
            Pause
        }
    }
} while ($true)