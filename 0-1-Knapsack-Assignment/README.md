# 0/1 Knapsack — Dynamic Programming with Live ASCII Visualization

This project reads all `#Test`-separated cases from the supplied dataset, solves each **0/1 Knapsack** problem using a **2D dynamic programming table**, displays the table being built in the terminal, prints each optimal value, and saves the results to `result.txt`.

## Requirements

- Python 3.8 or newer
- No external packages

## Run

Open a terminal in this project directory and run:

```bash
python3 knapsack.py
```

The default animation updates the table **after each item (row)**, showing the DP construction step by step. In an interactive terminal the display refreshes in place. The program handles all 10 tests automatically and writes `result.txt` in this directory.

Other useful options:

```bash
python3 knapsack.py --step cell --delay 0.02  # Animate each calculated DP cell
python3 knapsack.py --delay 0                # Show row updates without pausing
python3 knapsack.py --no-visual              # Fast calculation without animation
python3 knapsack.py --help                   # List all options
```

You can also specify custom input/output paths with `--input` and `--output`.

## Input format

Each test begins with a line starting with `#Test` (trailing spaces are accepted). The next nonblank line gives `n W` (number of items and capacity), followed by exactly `n` lines of `weight value` pairs:

```text
#Test
4 10
5 60
3 50
4 70
2 30
```

## Algorithm

`dp[i][w]` stores the greatest value obtainable from the first `i` items with capacity `w`.

- Base case: `dp[0][w] = 0` and `dp[i][0] = 0` for the supplied positive-weight dataset.
- If item `i` is too heavy: `dp[i][w] = dp[i-1][w]`.
- Otherwise: `dp[i][w] = max(dp[i-1][w], value[i] + dp[i-1][w-weight[i]])`.
- Answer: `dp[n][W]`.

Each item is either taken **once** or not taken; items cannot be divided. The table is updated progressively, with a row or current cell visible as the calculation proceeds.

**Time complexity:** `O(nW)` per test. **Space complexity:** `O(nW)` per test.

## Output format

The program prints each result and creates `result.txt` containing one line per test:

```text
#Test 1 (4 10) 150
#Test 2 (5 15) 100
```

The format records the test number, the original `(n W)` input, and the optimal result. All 10 test results are included in the committed `result.txt` and regenerated each time the script runs.

## Project files

- `knapsack.py` — input parsing, 0/1 DP solution, live ASCII table, and results writer
- `Knapsack_data.txt` — original supplied test cases (10 total)
- `result.txt` — generated maximum values for all test cases
- `README.md` — usage and explanation

## Note about visualization

For the smoothest animation, run the program in a regular terminal (macOS Terminal, Windows Terminal, VS Code terminal, etc.). With output redirected to a file, each frame is printed sequentially rather than clearing the screen. For wide tables, maximize the terminal window or reduce its font size. The default row animation is easy to follow; use `--step cell` to watch every individual cell update.
