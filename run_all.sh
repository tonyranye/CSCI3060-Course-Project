#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="inputs"           # folder with test input files
OUTPUT_DIR="outputs"         # where you want .atf + .out
ACCOUNTS_FILE="accounts/accounts_valid.json"

mkdir -p "$OUTPUT_DIR"

shopt -s nullglob
for f in "$INPUT_DIR"/*; do
    base="$(basename "${f}")"        # e.g. 006_transfer_input.txt
    name="${base%.*}"                # e.g. 006_transfer_input
    
    echo "Running test: $base"
    
    # stdin comes from the input file
    # .atf is passed as the "daily transactions output" argument to your program
    # stdout+stderr go into the terminal log (.out)
    python main.py "$ACCOUNTS_FILE" "$OUTPUT_DIR/$name.atf" < "$f" > "$OUTPUT_DIR/$name.out" 2>&1
done

echo "Done. Outputs are in: $OUTPUT_DIR/"