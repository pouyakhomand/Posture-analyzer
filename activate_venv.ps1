# PowerShell script to activate Python 3.12 Virtual Environment
Write-Host "Activating Python 3.12 Virtual Environment..." -ForegroundColor Green
& "venv312\Scripts\Activate.ps1"

Write-Host "`nVirtual environment activated!" -ForegroundColor Green
Write-Host "Python version: " -NoNewline
python --version

Write-Host "`nTo start the service, run:" -ForegroundColor Yellow
Write-Host "  python start.py" -ForegroundColor Cyan
Write-Host "  or" -ForegroundColor Cyan
Write-Host "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Cyan

Write-Host "`nTo deactivate, run: deactivate" -ForegroundColor Yellow
Write-Host "`nService URLs:" -ForegroundColor Yellow
Write-Host "  Health Check: http://localhost:8000/api/v1/health" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Root: http://localhost:8000/" -ForegroundColor Cyan 