Write-Host "Setting up the project..."

# Change Execution Policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force


# Set global variable for project path
Set-Variable -Name FACEGEN_PATH -Value $HOME\FaceGen -Scope Global -Description "FaceGen project directory path"

# Function to install Chocolatey
function Install-Chocolatey {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install Chocolatey if not installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Install-Chocolatey
}

# Install Python if not installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    choco install python --version=3.12.4 -y
} else {
    $pythonVersion = python --version
    Write-Host "$pythonVersion already installed."
}

# Install Git if not installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    choco install git -y
} else {
    $gitVersion = git --version
    Write-Host "$gitVersion already installed."
}

# Create project directory if it does not exist
if (-not (Test-Path -Path $HOME\FaceGen)) {
    New-Item -ItemType Directory -Path $HOME\FaceGen
}

# Clone the repository
if (-not (Test-Path -Path "$HOME\FaceGen\.git")) {
    git clone https://github.com/hugoglvs/facegen.git $HOME\FaceGen
} else {
    Write-Host "Repository already cloned."
}

# Change to project directory
Set-Location $HOME\FaceGen

# Create a virtual environment
if (-not (Test-Path -Path "$HOME\FaceGen\venv")) {
    python -m venv venv
}

# Activate the virtual environment
& "$HOME\FaceGen\venv\Scripts\Activate.ps1"

# Install project dependencies
pip install -r requirements.txt

# Create execution file
$runFilePath = Join-Path $HOME\FaceGen "run.ps1"
if (-not (Test-Path -Path $runFilePath)) {
    New-Item -ItemType File -Path $runFilePath -Value "python main.py"
}

Write-Host "Setup complete. Project downloaded and dependencies installed."
