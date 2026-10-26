"""0/1 Knapsack with dynamic programming and live terminal ASCII visualization.

Run: python3 knapsack.py
Help: python3 knapsack.py --help
"""

import argparse
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "Knapsack_data.txt"
DEFAULT_OUTPUT = BASE_DIR / "result.txt"


def read_test_cases(path):
    """Read #Test-delimited cases: first line n W, then n weight/value pairs."""
    cases = []
    block = []

    def finish_block():
        if not block:
            raise ValueError("A #Test section has no data.")
        try:
            n, capacity = map(int, block[0].split())
        except (ValueError, TypeError) as exc:
            raise ValueError("Expected 'n W' after #Test.") from exc
        if n < 0 or capacity < 0:
            raise ValueError("Number of items and capacity must be nonnegative.")
        if len(block) != n + 1:
            raise ValueError(
                f"Test {len(cases) + 1}: expected {n} item lines, got {len(block) - 1}."
            )
        items = []
        for line in block[1:]:
            try:
                weight, value = map(int, line.split())
            except ValueError as exc:
                raise ValueError(f"Invalid item line: {line!r}") from exc
            if weight < 0 or value < 0:
                raise ValueError("Item weights and values must be nonnegative.")
            items.append((weight, value))
        cases.append((n, capacity, items))

    started = False
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#Test"):
            if started:
                finish_block()
            block = []
            started = True
        elif started:
            block.append(line)
        else:
            raise ValueError("Input must begin with a #Test line.")
    if started:
        finish_block()
    if not cases:
        raise ValueError("No #Test cases found.")
    return cases


def render_table(dp, test_number, n, capacity, processed, current=None):
    """Render the current DP table as plain ASCII, with an optional active cell."""
    width = max(3, len(str(max((max(row) for row in dp), default=0))), len(str(capacity)))
    label_width = max(5, len(str(n)) + 2)
    heading = " " * (label_width + 3) + " ".join(f"{w:>{width}}" for w in range(capacity + 1))
    border = "-" * len(heading)
    lines = [f"Test {test_number} | Items: {n} | Capacity: {capacity}",
             f"Rows processed: {processed}/{n} | Columns: capacities 0..{capacity}",
             "DP[i][w] = best value using first i items and capacity w",
             heading, border]
    for i, row in enumerate(dp):
        if i > processed:
            break
        cells = []
        for w, value in enumerate(row):
            if current == (i, w):
                cells.append(f"[{value:>{width}}]")
            else:
                cells.append(f" {value:>{width}} ")
        lines.append(f"{i:>{label_width}} |" + "".join(cells))
    return "\n".join(lines)


def solve_knapsack(n, capacity, items, test_number, visualize=True, delay=0.12, step="row"):
    """Compute full 2D DP table; visualize each completed row or updated cell."""
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    is_tty = sys.stdout.isatty()

    def show(processed, current=None, note=""):
        if not visualize:
            return
        if is_tty:
            # Clear screen and move cursor home (ANSI supported by modern terminals).
            print("\033[2J\033[H", end="")
        print(render_table(dp, test_number, n, capacity, processed, current))
        if note:
            print(note)
        print(flush=True)
        if delay:
            time.sleep(delay)

    show(0, note="Initial table (no items processed)")
    for i, (weight, value) in enumerate(items, start=1):
        for w in range(capacity + 1):
            without_item = dp[i - 1][w]
            if weight <= w:
                with_item = value + dp[i - 1][w - weight]
                dp[i][w] = max(without_item, with_item)
            else:
                dp[i][w] = without_item
            if step == "cell":
                show(i, current=(i, w), note=f"Processing item {i}: weight={weight}, value={value}; capacity={w}")
        if step == "row":
            show(i, note=f"Completed item {i}: weight={weight}, value={value}")
    return dp[n][capacity]


def main():
    parser = argparse.ArgumentParser(description="0/1 Knapsack DP with live ASCII table visualization")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Input #Test file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Results file")
    parser.add_argument("--delay", type=float, default=0.12, help="Seconds between frames (default: 0.12)")
    parser.add_argument("--step", choices=("row", "cell"), default="row", help="Show each completed row or each cell")
    parser.add_argument("--no-visual", action="store_true", help="Disable animation for fast/batch runs")
    args = parser.parse_args()
    if args.delay < 0:
        parser.error("--delay must be nonnegative")

    try:
        cases = read_test_cases(args.input)
        results = []
        for number, (n, capacity, items) in enumerate(cases, start=1):
            answer = solve_knapsack(n, capacity, items, number,
                                    visualize=not args.no_visual, delay=args.delay, step=args.step)
            result = f"#Test {number} ({n} {capacity}) {answer}"
            results.append(result)
            print(f"Result: {result}", flush=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(results) + "\n", encoding="utf-8")
        print(f"\nSaved {len(results)} results to {args.output}")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
