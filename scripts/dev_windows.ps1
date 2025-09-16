
param()
Write-Host "🔧 Setting up virtual environment..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if (-not (Test-Path ".env")) { Copy-Item ".env.sample" ".env" }
Write-Host "📦 Running migrations..." -ForegroundColor Cyan
python manage.py migrate
Write-Host "🚀 Starting dev server at http://127.0.0.1:8000" -ForegroundColor Green
python manage.py runserver
