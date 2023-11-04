# Sudoku Solver

This Python script is an efficient Sudoku puzzle solver using backtracking, constraint propagation, and the minimum remaining value (MRV) heuristic.

## Features

- **Backtracking Algorithm**: Solves the Sudoku puzzle by trying one number after another until the puzzle is solved.
- **Constraint Propagation**: Reduces the search space by applying the Sudoku rules to eliminate possible values for a cell.
- **Minimum Remaining Value (MRV) Heuristic**: Prioritizes cells with the fewest legal moves left to speed up the search process.
- **Performance Measurement**: Calculates the time taken to solve each puzzle, allowing for performance analysis.

## Getting Started

### Prerequisites

You need Python 3.x installed on your system to run this script. You can check your Python version by running:

```bash
python --version
```

### Usage
To solve a single Sudoku puzzle, run the script with the puzzle string as an argument:

```bash
python sudoku.py 'puzzle_string_here'
```

For example:
```bash
python sudoku.py '530070000600195000098000060800060003400803001700020006060000280000419005000080079'
```

The solutions will be written to output.txt in the current directory and will be printed on display.