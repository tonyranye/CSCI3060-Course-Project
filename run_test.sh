#!/bin/bash


set -e

ACCOUNTS_FILE="accounts/accounts_valid.json"
INPUT_DIR="tests/004_paybill"
OUTPUT_DIR="results"

mkdir -p "$OUTPUT_DIR"

for input_file in "$INPUT_DIR"/*_input.txt
do
    base=$(basename "$input_file" _input.txt)

    python main.py "$ACCOUNTS_FILE" "$OUTPUT_DIR/$base.atf" \
        < "$input_file" \
        > "$OUTPUT_DIR/$base.out"
done

