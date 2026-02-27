#!/usr/bin/env bash
set -euo pipefail

ACCOUNTS_FILE="accounts/accounts_valid.json"
OUTPUT_DIR="results"

mkdir -p "$OUTPUT_DIR"

# Function to run tests for a specific test folder
run_test_folder() {
    local test_folder=$1
    local folder_name=$(basename "$test_folder")
    
    echo "=========================================="
    echo "Running tests in: $folder_name"
    echo "=========================================="
    
    # Create output subdirectory for this test folder
    mkdir -p "$OUTPUT_DIR/$folder_name"
    
    shopt -s nullglob
    for input_file in "$test_folder"/*_input.txt; do
        if [ -f "$input_file" ]; then
            base="$(basename "${input_file}")"
            # Remove _input.txt to get the test name
            name="${base%_input.txt}"
            
            echo "  Running test: $name"
            
            # Run the test
            python main.py "$ACCOUNTS_FILE" "$OUTPUT_DIR/$folder_name/$name.atf" < "$input_file" > "$OUTPUT_DIR/$folder_name/$name.out" 2>&1
            
            echo "  ✓ Complete: $name"
            echo ""
        fi
    done
}

# Run tests for deposit (005_deposit)
if [ -d "tests/005_deposit" ]; then
    run_test_folder "tests/005_deposit"
fi

# Run tests for create_account (006_create_account)
if [ -d "tests/006_create_account" ]; then
    run_test_folder "tests/006_create_account"
fi

echo "=========================================="
echo "All tests complete!"
echo "Results are in: $OUTPUT_DIR/"
echo "=========================================="