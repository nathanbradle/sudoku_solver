#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"
units = {'A': 'ABC', 'B': 'ABC', 'C': 'ABC', 'D': 'DEF', 'E': 'DEF', 'F': 'DEF', 'G': 'GHI', 'H': 'GHI', 'I': 'GHI', '1': '123', '2': '123', '3': '123', '4': '456', '5': '456', '6': '456', '7': '789', '8': '789', '9': '789',}

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    possible_values = initialize_values(board)  #Initialize values for FC
    return backtrack(board, possible_values)

def initialize_values(board):
    possible = {r + c: set(range(1, 10)) for r in ROW for c in COL}  #Any number in any square
    for (r, c), v in board.items():
        if v != 0:
            assign(r + c, v, board, possible)  #Updates by looking through init board
    return possible

def assign(var, value, board, possible):
    board[var] = value
    possible[var] = {value}
    for peer in available(var):
        if board[peer] == 0:
            possible[peer].discard(value)

def available(var):
    row, col = var
    p_row = {r + col for r in ROW}
    p_col = {row + c for c in COL}
    p_box = {r + c for r in units[row] for c in units[col]} - {var}
    neighbors = p_row | p_col | p_box
    return neighbors


def backtrack(board, possible_values):
    if complete(board):
        return board
    var = mrv(board, possible_values)  
    for value in possible_values[var]:
        unique = True
        for peer in available(var):
            if value in possible_values[peer]:
                unique = False
                break
        if unique:
            continue
        old_values = {}
        peers_and_var = available(var).union({var})
        for v in peers_and_var:
            old_values[v] = possible_values[v].copy()

        assign(var, value, board, possible_values)
        result = backtrack(board, possible_values)
        if result is not None:
            return result
        board[var] = 0
        possible_values.update(old_values)
    return None

def mrv(board, possible_values):
    zero_value_variable = []
    for var, value in board.items():
        if value == 0:
            zero_value_variable.append(var)
    minimum = float('inf')
    minimum_v = None
    for zero_var in zero_value_variable:
        current_length = len(possible_values[zero_var])
        if current_length < minimum:
            minimum = current_length
            minimum_v = zero_var
    return minimum_v

    

def consistent(column, row, domain, board):
    if any(domain == board[r + column] for r in ROW):
        return False
    if any(domain == board[row + col] for col in COL):
        return False
    sub_row = 3*(ROW.find(row)//3)
    sub_col = 3*((int(column)-1)//3)
    for i in range(3):
        for j in range(3):
            current_row = ROW[sub_row + i]
            current_col = COL[sub_col + j]
            if current_row == row and current_col == column:
                continue
            if domain == board[current_row + current_col]:
                return False

    return True


def complete(assignment):
    if len(assignment) == 0:
        return False
    for i in assignment:
        if assignment[i] == 0:
            return False
    return True

def values(board, c):
    row = c[0]
    col = c[1]
    initialrc = set(range(1,10))
    row_square = (ord(row) - ord('A')) // 3
    col_square = (int(col)-1) // 3
    row_value = {board[r + col] for r in ROW}
    col_value = {board[row + c] for c in COL}
    box_value = {board[ROW[row_square + i] + COL[col_square + j]] for i in range(3) for j in range(3)}
    result = initialrc - row_value - col_value - box_value
    return result

if __name__ == '__main__':
    number = 0
    timing = []
    if len(sys.argv) > 1:
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        #print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        print(board_to_string(solved_board))
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):


            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            start_time = time.time()

            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            number += 1
            runtime = time.time() - start_time
            timing.append(runtime)

        print("Finishing all boards in file.")