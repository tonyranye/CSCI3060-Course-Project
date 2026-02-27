$ACCOUNTS_FILE = "accounts/accounts_valid.json"
$OUTPUT_DIR = "results"

New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

function Run-TestFolder {
    param($testFolder)
    
    $folderName = Split-Path $testFolder -Leaf
    
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "Running tests in: $folderName" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    
    $outputSubDir = Join-Path $OUTPUT_DIR $folderName
    New-Item -ItemType Directory -Force -Path $outputSubDir | Out-Null
    
    $inputFiles = Get-ChildItem -Path $testFolder -Filter "*_input.txt"
    
    if ($inputFiles.Count -eq 0) {
        Write-Host "  WARNING: No input files found!" -ForegroundColor Red
        return
    }
    
    foreach ($inputFile in $inputFiles) {
        $name = $inputFile.BaseName -replace "_input$", ""
        
        Write-Host "  Running test: $name" -ForegroundColor Yellow
        
        $atfFile = Join-Path $outputSubDir "$name.atf"
        $outFile = Join-Path $outputSubDir "$name.out"
        
        Get-Content $inputFile.FullName | python main.py $ACCOUNTS_FILE $atfFile *> $outFile
        
        Write-Host "  ✓ Complete: $name" -ForegroundColor Green
    }
    
    Write-Host ""
}

if (Test-Path "tests/001_session_rules-login_logout") {
    Run-TestFolder "tests/001_session_rules-login_logout"
}

if (Test-Path "tests/002_withdrawal") {
    Run-TestFolder "tests/002_withdrawal"
}

if (Test-Path "tests/003_transfer") {
    Run-TestFolder "tests/003_transfer"
}

if (Test-Path "tests/004_paybill") {
    Run-TestFolder "tests/004_paybill"
}

if (Test-Path "tests/005_deposit") {
    Run-TestFolder "tests/005_deposit"
}

if (Test-Path "tests/006_create_account") {
    Run-TestFolder "tests/006_create_account"
}

if (Test-Path "tests/007_disable_delete_changeplan") {
    Run-TestFolder "tests/007_disable_delete_changeplan"
}

if (Test-Path "tests/008_output_format") {
    Run-TestFolder "tests/008_output_format"
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "All tests complete!" -ForegroundColor Green
Write-Host "Results are in: $OUTPUT_DIR/" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
