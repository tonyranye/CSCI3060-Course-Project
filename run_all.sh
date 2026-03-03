# Getting the Path to accounts file
ACCOUNTS_FILE="accounts/accounts_valid.json"
# Folder where test results will be saved
OUTPUT_DIR="results"
# Create results folder if it does not exist already
mkdir -p "$OUTPUT_DIR"

# Function to run all tests inside one test folder
run_test_folder() {
    local testFolder="$1"

    # Get just the folder name
    local folderName
    folderName=$(basename "$testFolder")

    echo -e "\e[36mRunning tests in: $folderName\e[0m"

    # Create matching subfolder inside results
    local outputSubDir="$OUTPUT_DIR/$folderName"
    mkdir -p "$outputSubDir"

    # Get all *_input.txt files in that test folder
    local inputFiles=("$testFolder"/*_input.txt)

    # If no test files found, show warning
    if [ ! -e "${inputFiles[0]}" ]; then
        echo -e "\e[31m  WARNING: No input files found!\e[0m"
        return
    fi

    # Loop through each input file
    for inputFile in "${inputFiles[@]}"; do

        # Remove "_input" from file name
        local baseName
        baseName=$(basename "$inputFile" .txt)
        local name="${baseName%_input}"

        echo -e "\e[33m  Running test: $name\e[0m"

        # Set output file paths
        local atfFile="$outputSubDir/$name.atf"
        local outFile="$outputSubDir/$name.out"

        # Run program using input file
        python main.py "$ACCOUNTS_FILE" "$atfFile" < "$inputFile" > "$outFile" 2>&1

        echo -e "\e[32m  - Complete: $name\e[0m"
    done

    echo ""
}

# Run each test folder
[ -d "tests/001_session_rules-login_logout" ] && run_test_folder "tests/001_session_rules-login_logout"
[ -d "tests/002_withdrawal" ]                 && run_test_folder "tests/002_withdrawal"
[ -d "tests/003_transfer" ]                   && run_test_folder "tests/003_transfer"
[ -d "tests/004_paybill" ]                    && run_test_folder "tests/004_paybill"
[ -d "tests/005_deposit" ]                    && run_test_folder "tests/005_deposit"
[ -d "tests/006_create_account" ]             && run_test_folder "tests/006_create_account"
[ -d "tests/007_disable_delete_changeplan" ]  && run_test_folder "tests/007_disable_delete_changeplan"
[ -d "tests/008_output_format" ]              && run_test_folder "tests/008_output_format"

# Shows the done message once done
echo -e "\e[32mAll tests complete!\e[0m"