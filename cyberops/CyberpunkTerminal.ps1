# Cyberpunk Terminal by ChatGPT
# Requisitos: PowerShell 5+, ANSI suporte (Windows Terminal recomendado)

# Tema Neon
$borderColor = "`e[38;5;199m"  # Rosa neon
$inputColor = "`e[38;5;45m"    # Azul neon
$outputColor = "`e[38;5;118m"  # Verde neon
$resetColor = "`e[0m"

# Comandos conhecidos para auto-completar
$comandos = @("ipconfig", "ping", "nslookup", "netstat", "Get-Process", "Get-Service", "exit")

function Draw-Border {
    param (
        [string]$text,
        [string]$color
    )
    $length = ($text.Length + 4)
    $top = "$color┌" + ("─" * $length) + "┐$resetColor"
    $mid = "$color│$resetColor  $text  $color│$resetColor"
    $bot = "$color└" + ("─" * $length) + "┘$resetColor"
    Write-Host $top
    Write-Host $mid
    Write-Host $bot
}

function Auto-Complete {
    param ([string]$input)
    return $comandos | Where-Object { $_ -like "$input*" }
}

function Show-Prompt {
    Write-Host ""
    Draw-Border -text "Digite um comando ou 'exit' para sair" -color $borderColor
    Write-Host -NoNewline "$inputColor> $resetColor"
    return Read-Host
}

function Exec-Comando {
    param ([string]$cmd)
    try {
        $output = Invoke-Expression $cmd 2>&1 | Out-String
        Draw-Border -text "Resultado" -color $borderColor
        Write-Host "$outputColor$output$resetColor"
    } catch {
        Write-Host "$borderColor[ERRO]$resetColor $_"
    }
}

function Test-DNS {
    param ([string]$dnsHost)
    try {
        $dns = Resolve-DnsName $dnsHost -ErrorAction Stop
        Draw-Border -text "DNS de $dnsHost" -color $borderColor
        $dns | Format-Table -AutoSize | Out-String | Write-Host -ForegroundColor Cyan
    } catch {
        Write-Host "$borderColor[ERRO]$resetColor DNS falhou para $dnsHost"
    }
}

function Start-TCPConnection {
    param (
        [string]$server = "127.0.0.1",
        [int]$port = 43
    )
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect($server, $port)
        Draw-Border -text "TCP -> ${server}:${port} OK" -color $borderColor
        $tcp.Close()
    } catch {
        Write-Host "${borderColor}[ERRO]${resetColor} Não foi possível conectar a ${server}:${port}"
    }
}

# ===== LOOP PRINCIPAL =====
Clear-Host
Draw-Border -text "CYBERPUNK TERMINAL v1.0" -color $borderColor

while ($true) {
    $cmd = Show-Prompt

    if ($cmd -eq "exit") {
        Draw-Border -text "Saindo..." -color $borderColor
        break
    }

    # Autocomplete sugestão
    $sugestoes = Auto-Complete -input $cmd
    if ($sugestoes.Count -gt 0 -and $cmd -ne $sugestoes[0]) {
        Write-Host "$inputColor[Auto-complete sugestão]:$resetColor $($sugestoes -join ', ')"
    }

    switch -Wildcard ($cmd) {
        "dns *" {
            $dnsHost = $cmd -replace "dns ", ""
            Test-DNS -dnsHost $dnsHost
        }
        "tcp *" {
            $dest = $cmd -replace "tcp ", ""
            $parts = $dest -split ":", 2
            if ($parts.Count -eq 2) {
                Start-TCPConnection -server $parts[0] -port [int]$parts[1]
            } else {
                Write-Host "$borderColor[ERRO]$resetColor Use formato: tcp 8.8.8.8:53"
            }
        }
        default {
            Exec-Comando -cmd $cmd
        }
    }
}