# setup.ps1

Write-Host "Setting up the project..."
# Change Execution Policy to Administrator
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force


# Parameters
param (
    [string]$githubRepoUrl = "https://github.com/hugoglvs/facegen.git", # GitHub repository URL
    [string]$projectDir = "$HOME\FaceGen"
)

Set-Variable -Name FACEGEN_PATH $ -Value $projectDir -Scope global -Description "FaceGen project directory path"

# Function to install Chocolatey
function Install-Chocolatey {
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor  [System.Net.SecurityProtocolType]::Tls12; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Chocolatey if not installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Output "Installing Chocolatey..."
    Install-Chocolatey
}

# Install Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    choco install python --version=3.12.4 -y
} else {
    $pythonVersion = python --version
    Write-Output  "$pythonVersion already installed."
}

# Install Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    choco install git -y
} else {
    $gitVersion = git --version
    Write-Output "$gitVersion already installed."
}

# Create project directory if not exists
if (-not (Test-Path -Path $projectDir)) {
    New-Item -ItemType Directory -Path $projectDir
}

# Clone the repository
git clone $githubRepoUrl $projectDir

# Change to project directory
Set-Location $projectDir

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
& "$projectDir\venv\Scripts\Activate.ps1"

# Install project dependencies
pip install -r requirements.txt

# Create execution file
New-Item -ItemType File -Path $projectDir -Name "run.ps1" -Value "python main.py"

Write-Output "Setup complete. Project downloaded and dependencies installed."
