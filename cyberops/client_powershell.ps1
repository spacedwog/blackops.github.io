# ----------------------------
# client_powershell.ps1
# ----------------------------

$hostAddress = "127.0.0.1"
$port = 443

function Connect-AndSendCommand {
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect($hostAddress, $port)
    $stream = $client.GetStream()
    $writer = New-Object System.IO.StreamWriter($stream)
    $reader = New-Object System.IO.StreamReader($stream)

    Write-Host "Conectado ao servidor TCP (${hostAddress}:${port})."
    Write-Host "Digite comandos PowerShell para executar remotamente (digite 'exit' para sair):`n"

    while ($true) {
        Write-Host -NoNewline "PS> "
        $cmd = Read-Host
        if ($cmd -eq "exit") {
            break
        }
        $writer.WriteLine($cmd)
        $writer.Flush()
        
        Start-Sleep -Milliseconds 100
        $response = ""
        while ($stream.DataAvailable) {
            $response += $reader.ReadLine() + "`n"
        }
        Write-Host "`nResposta:"
        Write-Host $response
    }

    $writer.Close()
    $reader.Close()
    $stream.Close()
    $client.Close()
    Write-Host "Conexão encerrada."
}

Connect-AndSendCommand