Write-Host "Setting up the project..."

# Change Execution Policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force


# Function to install Chocolatey
function Install-Chocolatey {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Volé à Lucas Triozon
function Invoke-Utility {
    <#
    .SYNOPSIS
    Invokes an external utility, ensuring successful execution.
    
    .DESCRIPTION
    Invokes an external utility (program) and, if the utility indicates failure by 
    way of a nonzero exit code, throws a script-terminating error.
    
    * Pass the command the way you would execute the command directly.
    * Do NOT use & as the first argument if the executable name is not a literal.
    
    .EXAMPLE
    Invoke-Utility git push
    
    Executes `git push` and throws a script-terminating error if the exit code
    is nonzero.
    #>
      $exe, $argsForExe = $Args
      # Workaround: Prevents 2> redirections applied to calls to this function
      #             from accidentally triggering a terminating error.
      #             See bug report at https://github.com/PowerShell/PowerShell/issues/4002
      $ErrorActionPreference = 'Continue'
      try { & $exe $argsForExe } catch { Throw } # catch is triggered ONLY if $exe can't be found, never for errors reported by $exe itself
      if ($LASTEXITCODE) { Throw "$exe indicated failure (exit code $LASTEXITCODE; full command: $Args)." }
}

# Install Chocolatey if not installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Install-Chocolatey
    choco feature enable -n=allowGlobalConfirmation
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

Import-Module ps2exe

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Set the path to the Program Files directory
Set-Location $Env:Programfiles

# Create project directory if it does not exist
if (-not (Test-Path -Path FaceGen)) {
    New-Item -ItemType Directory -Path FaceGen
}

# Clone the repository
if (-not (Test-Path -Path "FaceGen\.git")) {
    try {
        Invoke-Utility git clone https://github.com/hugoglvs/facegen.git $Env:ProgramFiles\FaceGen
    } catch {
        Write-Error "Failed to clone repository."
    }
} else {
    Write-Host "Repository already cloned."
}

# Change to project directory
Set-Location FaceGen

# Create a virtual environment
if (-not (Test-Path -Path "$Env:ProgramFiles\FaceGen\venv")) {
    python -m venv venv
}

# Activate the virtual environment
& "$Env:ProgramFiles\FaceGen\venv\Scripts\Activate.ps1"

# Install project dependencies
try {
    Write-Output "Installing project dependencies..."
    python -m pip install -r requirements.txt
} catch {
    Write-Error "Failed to install project dependencies."
}

# Create execution file
$runFilePath = Join-Path $Env:ProgramFiles\FaceGen "run.ps1"
if (-not (Test-Path -Path $runFilePath)) {
    New-Item -ItemType File -Path $runFilePath -Value @'
Set-Location $Env:ProgramFiles\FaceGen
& "venv\Scripts\Activate.ps1"

if (Get-Command python -ErrorAction SilentlyContinue) {
    python manage.py migrate
    Start-Process -FilePath python -ArgumentList "manage.py runserver"
    # Wait for the server to start
    Start-Sleep -Seconds 10
    Start-Process -FilePath "C:\Program Files (x86)\Mozilla Firefox\firefox.exe" -ArgumentList "http://127.0.0.1:8000" -WindowStyle Maximized
    
} else {
    Write-Error "Python not found."
}
'@
}

Invoke-ps2exe -inputFile $runFilePath -outputFile $HOME\Desktop\FaceGen.exe -requireAdmin


Write-Host "Setup complete. Project downloaded and dependencies installed."
Write-Host "To run the project, execute the run.ps1 script."
