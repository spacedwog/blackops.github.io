# Caminho do seu script Streamlit
$scriptPath = "config/firewall_widget.py"

# Verifica se o script está rodando como administrador
$adminCheck = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $adminCheck) {
    # Reexecuta o script como administrador
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Executa o Streamlit como administrador
streamlit run $scriptPath