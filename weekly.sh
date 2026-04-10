#!/bin/bash
#
# weekly.sh - Weekly Banking System Script
#
# PROGRAM INTENTION:
#   Simulates seven consecutive days of banking operations by calling
#   daily.sh once per day. Each day runs a different set of transaction
#   sessions, and the Current Bank Accounts File output from each day
#   is automatically passed in as the input for the next day, so that
#   account balances carry forward across the full week.
#
# USAGE:
#   ./weekly.sh
#   (no arguments required - all paths are configured below)
#
# FILE FLOW PER DAY:
#   Day N input  current : weekly_data/current_day_N.json
#   Day N input  master  : weekly_data/master_day_N.txt
#   Day N output current : weekly_data/current_day_N+1.json  (becomes Day N+1 input)
#   Day N output master  : weekly_data/master_day_N+1.txt    (becomes Day N+1 input)
#   Day N merged ATF     : weekly_data/merged_day_N.atf
#   Day N session ATFs   : weekly_data/day_N/session_1.atf, session_2.atf, ...
#
# SESSIONS PER DAY:
#   Day 1 - Test 013 : Privileged transfer (no limit)
#   Day 2 - Test 015 : Valid paybill to EC
#   Day 3 - Test 022 : Deposit recorded
#   Day 4 - Test 024 : Admin creates a new account
#   Day 5 - Test 036 : Admin changes payment plan
#   Day 6 - Test 031 : Standard user attempts delete (rejected)
#   Day 7 - Test 034 : Admin disables an account
#
# -------------------------------------------------------------------------

set -e

# ---------- configurable paths ----------
FRONTEND="python main.py"
BACKEND="python backend/backend_main.py"

# Seed files - the starting state before Day 1
SEED_CURRENT="accounts/accounts_current.json"
SEED_MASTER="accounts/accounts_master.txt"

# All working files for the week go here
WEEKLY_DIR="weekly_data"

# Session input files - one per day
DAY1_SESSIONS=(
    "tests/003_transfer/013_no_limit_transfers_privileged_mode_input.txt"
)
DAY2_SESSIONS=(
    "tests/004_paybill/015_valid_account_paying_from_input.txt"
)
DAY3_SESSIONS=(
    "tests/005_deposit/022_deposit_recorded_input.txt"
)
DAY4_SESSIONS=(
    "tests/006_create_account/024_create_ok_admin_input.txt"
)
DAY5_SESSIONS=(
    "tests/007_disable_delete_changeplan/036_changepplan_ok_admin_input.txt"
)
DAY6_SESSIONS=(
    "tests/007_disable_delete_changeplan/031_delete_user_standard_mode_input.txt"
)
DAY7_SESSIONS=(
    "tests/007_disable_delete_changeplan/034_disable_ok_admin_input.txt"
)
# ----------------------------------------

# ---- validate seed files ----
if [ ! -f "$SEED_CURRENT" ]; then
    echo "Error: seed current accounts file not found: $SEED_CURRENT"
    exit 1
fi
if [ ! -f "$SEED_MASTER" ]; then
    echo "Error: seed master accounts file not found: $SEED_MASTER"
    exit 1
fi

# ---- set up weekly working directory ----
mkdir -p "$WEEKLY_DIR"

# Copy seed files into weekly_data as Day 1 inputs
cp "$SEED_CURRENT" "$WEEKLY_DIR/current_day_1.json"
cp "$SEED_MASTER"  "$WEEKLY_DIR/master_day_1.txt"

echo "========================================================"
echo "  WEEKLY BANKING SYSTEM RUN"
echo "========================================================"
echo "  Seed current accounts : $SEED_CURRENT"
echo "  Seed master accounts  : $SEED_MASTER"
echo "  Working directory     : $WEEKLY_DIR"
echo "========================================================"

# ============================================================
# run_day <day_number> <session_input_files...>
#
#   Runs one full Daily cycle for the given day number using
#   whatever session input files are passed in.
#   Reads  : weekly_data/current_day_N.json
#            weekly_data/master_day_N.txt
#   Writes : weekly_data/current_day_N+1.json
#            weekly_data/master_day_N+1.txt
#            weekly_data/merged_day_N.atf
#            weekly_data/day_N/session_K.atf  (one per session)
# ============================================================
run_day() {
    local DAY="$1"
    shift
    local SESSIONS=("$@")

    local NEXT_DAY=$((DAY + 1))

    local CURRENT_IN="$WEEKLY_DIR/current_day_${DAY}.json"
    local MASTER_IN="$WEEKLY_DIR/master_day_${DAY}.txt"
    local CURRENT_OUT="$WEEKLY_DIR/current_day_${NEXT_DAY}.json"
    local MASTER_OUT="$WEEKLY_DIR/master_day_${NEXT_DAY}.txt"
    local MERGED_ATF="$WEEKLY_DIR/merged_day_${DAY}.atf"
    local SESSION_DIR="$WEEKLY_DIR/day_${DAY}"

    echo ""
    echo "========================================================"
    echo "  DAY $DAY"
    echo "  Sessions : ${#SESSIONS[@]}"
    echo "========================================================"

    mkdir -p "$SESSION_DIR"

    # Step (i): run Front End for each session 
    local SESSION_ATF_FILES=()

    for i in "${!SESSIONS[@]}"; do
        local SESSION_NUM=$((i + 1))
        local INPUT="${SESSIONS[$i]}"
        local SESSION_ATF="$SESSION_DIR/session_${SESSION_NUM}.atf"

        echo ""
        echo "  --- Day $DAY | Session $SESSION_NUM ---"

        if [ "$INPUT" = "INTERACTIVE" ]; then
            echo "  Mode: INTERACTIVE"
            echo "  Output ATF: $SESSION_ATF"
            $FRONTEND "$CURRENT_IN" "$SESSION_ATF"
        else
            if [ ! -f "$INPUT" ]; then
                echo "  Error: session input file not found: $INPUT"
                exit 1
            fi
            echo "  Input : $INPUT"
            echo "  Output ATF: $SESSION_ATF"
            $FRONTEND "$CURRENT_IN" "$SESSION_ATF" < "$INPUT"
        fi

        SESSION_ATF_FILES+=("$SESSION_ATF")
        echo "  Session $SESSION_NUM complete."
    done

    # ---- Step (ii): merge all session ATFs ----
    echo ""
    echo "  --- Day $DAY | Merging ${#SESSION_ATF_FILES[@]} session file(s) -> $MERGED_ATF ---"
    > "$MERGED_ATF"
    for ATF in "${SESSION_ATF_FILES[@]}"; do
        if [ -f "$ATF" ]; then
            cat "$ATF" >> "$MERGED_ATF"
        else
            echo "  Warning: session ATF not found: $ATF"
        fi
    done
    echo "  Merge complete. Lines: $(wc -l < "$MERGED_ATF")"

    # ---- Step (iii): run Back End ----
    echo ""
    echo "  --- Day $DAY | Running Back End ---"
    echo "  Master in  : $MASTER_IN"
    echo "  Merged ATF : $MERGED_ATF"
    echo "  Master out : $MASTER_OUT"
    echo "  Current out: $CURRENT_OUT"
    $BACKEND "$MASTER_IN" "$MERGED_ATF" "$MASTER_OUT" "$CURRENT_OUT"
    echo "  Back End complete."

    echo ""
    echo "  Day $DAY finished."
    echo "  -> Tomorrow's current accounts : $CURRENT_OUT"
    echo "  -> Tomorrow's master accounts  : $MASTER_OUT"
}

# ============================================================
# Run all 7 days
# ============================================================
run_day 1 "${DAY1_SESSIONS[@]}"
run_day 2 "${DAY2_SESSIONS[@]}"
run_day 3 "${DAY3_SESSIONS[@]}"
run_day 4 "${DAY4_SESSIONS[@]}"
run_day 5 "${DAY5_SESSIONS[@]}"
run_day 6 "${DAY6_SESSIONS[@]}"
run_day 7 "${DAY7_SESSIONS[@]}"

echo ""
echo "========================================================"
echo "  WEEKLY RUN COMPLETE"
echo "  Final current accounts : $WEEKLY_DIR/current_day_8.json"
echo "  Final master accounts  : $WEEKLY_DIR/master_day_8.txt"
echo "  Per-day merged ATFs    : $WEEKLY_DIR/merged_day_1.atf ... merged_day_7.atf"
echo "  Per-session ATFs       : $WEEKLY_DIR/day_1/ ... day_7/"
echo "========================================================"