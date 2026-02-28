# Getting the Path to accounts file
$ACCOUNTS_FILE = "accounts/accounts_valid.json"

# Folder where test results will be saved
$OUTPUT_DIR = "results"

# Create results folder if it does not  exist already
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

# Function to run all tests inside one test folder
function Run-TestFolder {
    param($testFolder)
    
    # Get just the folder name 
    $folderName = Split-Path $testFolder -Leaf
    
    Write-Host "Running tests in: $folderName" -ForegroundColor Cyan
    
    # Create matching subfolder inside results
    $outputSubDir = Join-Path $OUTPUT_DIR $folderName
    New-Item -ItemType Directory -Force -Path $outputSubDir | Out-Null
    
    # Get all *_input.txt files in that test folder
    $inputFiles = Get-ChildItem -Path $testFolder -Filter "*_input.txt"
    
    # If no test files found, show warning
    if ($inputFiles.Count -eq 0) {
        Write-Host "  WARNING: No input files found!" -ForegroundColor Red
        return
    }
    
    # Loop through each input file
    foreach ($inputFile in $inputFiles) {
        
        # Remove "_input" from file name
        $name = $inputFile.BaseName -replace "_input$", ""
        
        Write-Host "  Running test: $name" -ForegroundColor Yellow
        
        # Set output file paths
        $atfFile = Join-Path $outputSubDir "$name.atf"
        $outFile = Join-Path $outputSubDir "$name.out"
        
        # Run program using input file
       
        Get-Content $inputFile.FullName | python main.py $ACCOUNTS_FILE $atfFile *> $outFile
        
        Write-Host "  - Complete: $name" -ForegroundColor Green
    }
    
    Write-Host ""
}

# Run each test folder if it exists
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

# Shows the done message once done
Write-Host "All tests complete!" -ForegroundColor Green