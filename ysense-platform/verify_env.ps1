Write-Host "Checking .env file..." -ForegroundColor Yellow

# Check if file exists
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
    
    # Check file size
    $fileInfo = Get-Item ".env"
    Write-Host "  File size: $($fileInfo.Length) bytes" -ForegroundColor Cyan
    
    # Read and display first few lines
    Write-Host "
First 5 lines of .env:" -ForegroundColor Yellow
    Get-Content ".env" -Head 5
    
    # Test if Python can read it
    Write-Host "
Testing Python dotenv loading:" -ForegroundColor Yellow
    .\venv\Scripts\python.exe -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'Platform Version: {os.getenv(\"PLATFORM_VERSION\")}'); print(f'Environment: {os.getenv(\"ENVIRONMENT\")}'); print('✓ .env loaded successfully!')"
    
} else {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    
    # Check for common mistakes
    if (Test-Path ".env.txt") {
        Write-Host "Found .env.txt - needs to be renamed to .env" -ForegroundColor Yellow
    }
    if (Test-Path "env.txt") {
        Write-Host "Found env.txt - needs to be renamed to .env" -ForegroundColor Yellow
    }
}
