# runner-setup.ps1

# Defina os valores do seu repositório e token (copiados do GitHub)
$REPO_URL = "https://github.com/spacedwog/blackops.github.io"
$TOKEN = "BEH4NMD4SPZEY64MOKL7KFDIDZHMQ"

# Cria uma pasta e entra nela
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\actions-runner" | Out-Null
Set-Location "$env:USERPROFILE\actions-runner"

# Baixa o runner (verifique se a versão está atual)
Invoke-WebRequest -Uri "https://github.com/actions/runner/releases/download/v2.314.1/actions-runner-win-x64-2.314.1.zip" -OutFile "actions-runner.zip"
Expand-Archive -Path "actions-runner.zip" -DestinationPath . -Force

# Configura o runner
.\config.cmd --url $REPO_URL --token $TOKEN

# Instala e inicia como serviço
.\svc install
.\svc start

Write-Host "Runner instalado e em execução como serviço!" -ForegroundColor Green