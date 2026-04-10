#!/bin/bash
#
# daily.sh - Daily Banking System Script
#
# PROGRAM INTENTION:
#   Simulates one day of banking operations by:
#   (i)  Running the Front End over multiple transaction sessions,
#        saving each session's Bank Account Transaction File separately.
#   (ii) Concatenating all session transaction files into a single
#        Merged Daily Bank Account Transaction File.
#   (iii) Running the Back End with the merged file as input.
#
# USAGE:
#   ./daily.sh <current_accounts_file> <master_accounts_file> \
#              <new_current_accounts_file> <new_master_accounts_file> \
#              <session_input_1> [<session_input_2> ...] \
#              -- \
#              <merged_transaction_file>
#
# EXAMPLE (3 sessions, non-interactive):
#   ./daily.sh \
#     accounts/accounts_current.json \
#     accounts/accounts_master.txt \
#     accounts/accounts_current_new.json \
#     accounts/accounts_master_new.txt \
#     tests/001_session_rules-login_logout/002_only_logout_once_loggedin_input.txt \
#     tests/002_withdrawal/006_withdraws_over_limit_input.txt \
#     tests/005_deposit/022_deposit_recorded_input.txt \
#     -- \
#     daily_merged.atf
#
# NOTES:
#   - Session input files are plain text files whose lines are fed to the
#     Front End via stdin (one session per file).
#   - Pass "INTERACTIVE" instead of an input filename to run a session
#     interactively (the user types at the terminal).
#   - The "--" separator is required to mark the end of session inputs and
#     the start of the merged output filename.
#   - The Front End (main.py) and Back End (backend/backend_main.py) are
#     invoked as separate processes, as required by the spec.
#   - All intermediate transaction files are stored in the WORK_DIR and
#     cleaned up (or kept) based on the KEEP_TEMP variable below.
#
# -------------------------------------------------------------------------

# ---------- configurable paths ----------
FRONTEND="python main.py"
BACKEND="python backend/backend_main.py"
WORK_DIR="daily_tmp"          # temporary folder for per-session ATF files
KEEP_TEMP=true               # set to true to keep per-session files after run
# ----------------------------------------

set -e   # exit immediately on error

# ---- parse arguments ----
if [ "$#" -lt 5 ]; then
    echo "Usage: $0 <current_accounts> <master_accounts> <new_current> <new_master> <session_input|INTERACTIVE> [...] -- <merged_transaction_file>"
    exit 1
fi

CURRENT_ACCOUNTS="$1"
MASTER_ACCOUNTS="$2"
NEW_CURRENT="$3"
NEW_MASTER="$4"
shift 4

# Collect session inputs until we hit "--"
SESSION_INPUTS=()
while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
    SESSION_INPUTS+=("$1")
    shift
done

if [ "$1" != "--" ]; then
    echo "Error: missing '--' separator before merged transaction filename."
    exit 1
fi
shift  # consume "--"

if [ "$#" -ne 1 ]; then
    echo "Error: expected exactly one argument after '--' (merged transaction file)."
    exit 1
fi
MERGED_ATF="$1"

if [ "${#SESSION_INPUTS[@]}" -eq 0 ]; then
    echo "Error: at least one session input must be provided."
    exit 1
fi

# ---- validate input files ----
if [ ! -f "$CURRENT_ACCOUNTS" ]; then
    echo "Error: current accounts file not found: $CURRENT_ACCOUNTS"
    exit 1
fi
if [ ! -f "$MASTER_ACCOUNTS" ]; then
    echo "Error: master accounts file not found: $MASTER_ACCOUNTS"
    exit 1
fi

# ---- set up working directory ----
mkdir -p "$WORK_DIR"

echo "========================================================"
echo "  DAILY BANKING SYSTEM RUN"
echo "========================================================"
echo "  Current accounts  : $CURRENT_ACCOUNTS"
echo "  Master accounts   : $MASTER_ACCOUNTS"
echo "  Sessions          : ${#SESSION_INPUTS[@]}"
echo "  Merged output     : $MERGED_ATF"
echo "========================================================"

# ============================================================
# STEP (i) - Run Front End for each session
# ============================================================
SESSION_ATF_FILES=()

for i in "${!SESSION_INPUTS[@]}"; do
    SESSION_NUM=$((i + 1))
    INPUT="${SESSION_INPUTS[$i]}"
    SESSION_ATF="$WORK_DIR/session_${SESSION_NUM}.atf"

    echo ""
    echo "--- Session $SESSION_NUM ---"

    if [ "$INPUT" = "INTERACTIVE" ]; then
        echo "  Mode: INTERACTIVE (type your transactions below)"
        echo "  Output ATF: $SESSION_ATF"
        $FRONTEND "$CURRENT_ACCOUNTS" "$SESSION_ATF"
    else
        if [ ! -f "$INPUT" ]; then
            echo "Error: session input file not found: $INPUT"
            exit 1
        fi
        echo "  Mode: file  -> $INPUT"
        echo "  Output ATF: $SESSION_ATF"
        $FRONTEND "$CURRENT_ACCOUNTS" "$SESSION_ATF" < "$INPUT"
    fi

    SESSION_ATF_FILES+=("$SESSION_ATF")
    echo "  Session $SESSION_NUM complete."
done

# ============================================================
# STEP (ii) - Concatenate all session ATF files into one
# ============================================================
echo ""
echo "--- Merging ${#SESSION_ATF_FILES[@]} transaction file(s) -> $MERGED_ATF ---"

# Start fresh merged file
> "$MERGED_ATF"

for ATF in "${SESSION_ATF_FILES[@]}"; do
    if [ -f "$ATF" ]; then
        cat "$ATF" >> "$MERGED_ATF"
    else
        echo "Warning: expected session ATF file not found: $ATF"
    fi
done

echo "  Merge complete. Lines in merged file: $(wc -l < "$MERGED_ATF")"

# ============================================================
# STEP (iii) - Run Back End with the merged transaction file
# ============================================================
echo ""
echo "--- Running Back End ---"
echo "  Input master    : $MASTER_ACCOUNTS"
echo "  Input merged ATF: $MERGED_ATF"
echo "  Output master   : $NEW_MASTER"
echo "  Output current  : $NEW_CURRENT"

$BACKEND "$MASTER_ACCOUNTS" "$MERGED_ATF" "$NEW_MASTER" "$NEW_CURRENT"

echo "  Back End complete."

# ---- optional cleanup ----
if [ "$KEEP_TEMP" = false ]; then
    rm -rf "$WORK_DIR"
fi

echo ""
echo "========================================================"
echo "  DAILY RUN FINISHED"
echo "  New current accounts : $NEW_CURRENT"
echo "  New master accounts  : $NEW_MASTER"
echo "========================================================"