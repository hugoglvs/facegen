# runserver.ps1


Get-Variable -Name FACEGEN_PATH -ValueOnly | Set-Location

& "venv\Scripts\Activate.ps1"

if (Get-Command python -ErrorAction SilentlyContinue) {
    python manage.py migrate
    python manage.py runserver
} else {
    Write-Error "Python not found."
}