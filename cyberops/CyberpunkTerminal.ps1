Add-Type -AssemblyName PresentationFramework

# XAML (interface estilo cyberpunk)
[xml]$xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        Title="Cyberpunk Terminal" Height="500" Width="800" Background="Black"
        FontFamily="Consolas" Foreground="Lime">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <TextBlock Grid.Row="0" Text="🧠 CYBERPUNK TERMINAL" FontSize="20" Foreground="Cyan" Margin="0,0,0,10"/>

        <ScrollViewer Grid.Row="1" Name="OutputScroll" VerticalScrollBarVisibility="Auto" Background="#111111">
            <TextBox Name="OutputBox" IsReadOnly="True" TextWrapping="Wrap" Background="#111111" Foreground="Lime" BorderThickness="0" />
        </ScrollViewer>

        <DockPanel Grid.Row="2" Margin="0,10,0,0">
            <TextBox Name="InputBox" Height="30" Width="600" Margin="0,0,10,0"/>
            <Button Name="ExecuteButton" Content="Execute" Width="100" Background="Magenta" Foreground="Black"/>
        </DockPanel>
    </Grid>
</Window>
"@

# Carregar XAML
$reader = (New-Object System.Xml.XmlNodeReader $xaml)
$window = [Windows.Markup.XamlReader]::Load($reader)

# Acessar controles
$InputBox = $window.FindName("InputBox")
$OutputBox = $window.FindName("OutputBox")
$ExecuteButton = $window.FindName("ExecuteButton")

function Append-Output($text, $color = "Lime") {
    $OutputBox.AppendText(">> $text`r`n")
    $OutputBox.ScrollToEnd()
}

function Send-TCPMessage {
    param([string]$ip, [int]$port, [string]$message)
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
            Append-Output "Received: $response" "Cyan"
        } else {
            Append-Output "Message sent. No response." "DarkGray"
        }

        $writer.Close()
        $reader.Close()
        $client.Close()
    } catch {
        Append-Output "TCP Error: $_" "Red"
    }
}

function Resolve-DNSQuery {
    param (
        [string]$domain,
        [string]$type = "A"
    )

    try {
        Append-Output "Resolving DNS for '$domain' (type: $type)..."

        if ($type -eq "A") {
            $addresses = [System.Net.Dns]::GetHostAddresses($domain)
            foreach ($addr in $addresses) {
                Append-Output "IPv4: $($addr.IPAddressToString)"
            }
        } else {
            # Usar nslookup para tipos diferentes
            $output = nslookup -type=$type $domain 2>&1
            $output | ForEach-Object {
                if ($_ -match ".*") {
                    Append-Output $_ "DarkCyan"
                }
            }
        }
    } catch {
        Append-Output "DNS Error: $_" "Red"
    }
}

# Evento do botão
$ExecuteButton.Add_Click({
    $cmd = $InputBox.Text.Trim()
    Append-Output $cmd
    $InputBox.Text = ""

    if ($cmd -eq "exit") {
        $window.Close()
        return
    }

    if ($cmd -like "tcp *") {
        $parts = $cmd -split " "
        if ($parts.Length -ge 4) {
            $ip = $parts[1]
            $port = [int]$parts[2]
            $message = ($parts[3..($parts.Length - 1)] -join " ")
            Send-TCPMessage -ip $ip -port $port -message $message
        } else {
            Append-Output "Invalid TCP syntax. Use: tcp <ip> <port> <message>" "Yellow"
        }
    } elseif ($cmd -like "dns *") {
        $parts = $cmd -split " "
        if ($parts.Length -ge 2) {
            $domain = $parts[1]
            $type = if ($parts.Length -ge 3) { $parts[2] } else { "A" }
            Resolve-DNSQuery -domain $domain -type $type
        } else {
            Append-Output "Invalid DNS syntax. Use: dns <domain> [type]" "Yellow"
        }
    } else {
        try {
            $output = Invoke-Expression $cmd
            if ($output) {
                $output | ForEach-Object { Append-Output $_ }
            }
        } catch {
            Append-Output "Command error: $_" "Red"
        }
    }
})

# Exibir GUI
$window.ShowDialog()