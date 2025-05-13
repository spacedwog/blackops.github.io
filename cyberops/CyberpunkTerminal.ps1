# Cyberpunk Interface PowerShell Terminal com TCP/IP

function Show-Border {
    Clear-Host
    $width = 80
    $border = '+' + ('=' * ($width - 2)) + '+'
    Write-Host $border -ForegroundColor Magenta
    for ($i = 0; $i -lt 20; $i++) {
        Write-Host "|" -NoNewline -ForegroundColor Cyan
        Write-Host (" " * ($width - 2)) -NoNewline
        Write-Host "|" -ForegroundColor Cyan
    }
    Write-Host $border -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Cyberpunk Command Terminal v1.0" -ForegroundColor Green
    Write-Host "Type 'exit' to quit or 'tcp <ip> <port> <message>' to send TCP." -ForegroundColor Yellow
    Write-Host ""
}

function Send-TCPMessage {
    param(
        [string]$ip,
        [int]$port,
        [string]$message
    )
    try {
        $client = New-Object System.Net.Sockets.TcpClient($ip, $port)
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)

        $writer.AutoFlush = $true
        $writer.WriteLine($message)

        Start-Sleep -Milliseconds 500
        if ($stream.DataAvailable) {
            $response = $reader.ReadLine()
            Write-Host "Received: $response" -ForegroundColor Cyan
        } else {
            Write-Host "Message sent. No response." -ForegroundColor DarkGray
        }

        $writer.Close()
        $reader.Close()
        $client.Close()
    } catch {
        Write-Host "TCP Error: $_" -ForegroundColor Red
    }
}

function Start-Terminal {
    Show-Border
    while ($true) {
        Write-Host ""
        Write-Host ">> " -NoNewline -ForegroundColor Green
        $input = Read-Host

        if ($input -eq "exit") {
            Write-Host "Exiting terminal..." -ForegroundColor Red
            break
        }

        if ($input -like "tcp *") {
            $parts = $input -split " "
            if ($parts.Length -ge 4) {
                $ip = $parts[1]
                $port = [int]$parts[2]
                $message = ($parts[3..($parts.Length - 1)] -join " ")
                Send-TCPMessage -ip $ip -port $port -message $message
            } else {
                Write-Host "Invalid TCP syntax. Use: tcp <ip> <port> <message>" -ForegroundColor Yellow
            }
        } else {
            try {
                $output = Invoke-Expression $input
                if ($output) {
                    $output | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
                }
            } catch {
                Write-Host "Command error: $_" -ForegroundColor Red
            }
        }
    }
}

Start-Terminal