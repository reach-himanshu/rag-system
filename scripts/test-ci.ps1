# Local CI Check Script
# Run this before pushing to catch errors early!

$ErrorActionPreference = "Stop"

Write-Host "🔍 [1/4] Running Backend Linting..." -ForegroundColor Cyan
cd backend
ruff check .
ruff format --check .
if ($LASTEXITCODE -ne 0) { Write-Error "Backend Linting Failed!"; exit 1 }
cd ..

Write-Host "🧪 [2/4] Running Backend Tests..." -ForegroundColor Cyan
cd backend
python -m pytest
if ($LASTEXITCODE -ne 0) { Write-Error "Backend Tests Failed!"; exit 1 }
cd ..

Write-Host "🎨 [3/4] Running Frontend Tests..." -ForegroundColor Cyan
cd frontend
npm run test -- --passWithNoTests --watch=false
if ($LASTEXITCODE -ne 0) { Write-Error "Frontend Tests Failed!"; exit 1 }
cd ..

Write-Host "🏗️  [4/4] Running Frontend Build (Type Check)..." -ForegroundColor Cyan
cd frontend
npm run build
if ($LASTEXITCODE -ne 0) { Write-Error "Frontend Build Failed!"; exit 1 }
cd ..

Write-Host "✅ All Checks Passed! You are ready to push." -ForegroundColor Green
