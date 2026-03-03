

INPUT_DIR="tests_indv" # Getting the inputs  from tests dir
OUTPUT_DIR="results/indv" #Slecting where we want to put our output
ACCOUNTS_FILE="accounts/accounts_valid.json" #Getting the user data

mkdir -p "$OUTPUT_DIR" #Making the out dir

for f in "$INPUT_DIR"/*; do #looping through the n number of input dir in tests
  [ -f "$f" ] || continue

  base=$(basename "$f")
  name=${base%.*}

  echo "Running $base"
# Run the program with the accounts and it takes input from the test input file and Save all output into a .out file

  python main.py "$ACCOUNTS_FILE" "$OUTPUT_DIR/$name.atf" < "$f" > "$OUTPUT_DIR/$name.out" 2>&1
done

echo "Done"
