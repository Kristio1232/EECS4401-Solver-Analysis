from z3 import Solver, Or, And, Int, sat

def winning_moves(board, player):
    rows, cols = 6, 7
    winning_cols = []

    def cell_value(char):
        return {' ': 0, 'r': 1, 'b': 2}[char]

    for col in range(cols):
        row = None
        for r in reversed(range(rows)):
            if board[r][col] == ' ':
                row = r
                break
        if row is None:
            continue

        s = Solver()
        cells = [[Int(f'cell_{r}_{c}') for c in range(cols)] for r in range(rows)]

        for r in range(rows):
            for c in range(cols):
                if r == row and c == col:
                    s.add(cells[r][c] == cell_value(player))
                else:
                    s.add(cells[r][c] == cell_value(board[r][c]))
                s.add(Or(cells[r][c] == 0, cells[r][c] == 1, cells[r][c] == 2))

        win_cons = []
        # Horizontal
        for r in range(rows):
            for c in range(cols-3):
                win_cons.append(And(cells[r][c] == cell_value(player),
                                  cells[r][c+1] == cell_value(player),
                                  cells[r][c+2] == cell_value(player),
                                  cells[r][c+3] == cell_value(player)))
        # Vertical
        for r in range(rows-3):
            for c in range(cols):
                win_cons.append(And(cells[r][c] == cell_value(player),
                                  cells[r+1][c] == cell_value(player),
                                  cells[r+2][c] == cell_value(player),
                                  cells[r+3][c] == cell_value(player)))
        # Diagonals
        for r in range(rows-3):
            for c in range(cols-3):
                win_cons.append(And(cells[r][c] == cell_value(player),
                                  cells[r+1][c+1] == cell_value(player),
                                  cells[r+2][c+2] == cell_value(player),
                                  cells[r+3][c+3] == cell_value(player)))
        for r in range(3, rows):
            for c in range(cols-3):
                win_cons.append(And(cells[r][c] == cell_value(player),
                                  cells[r-1][c+1] == cell_value(player),
                                  cells[r-2][c+2] == cell_value(player),
                                  cells[r-3][c+3] == cell_value(player)))

        s.add(Or(*win_cons))
        if s.check() == sat:
            winning_cols.append(col)

    return winning_cols

def print_grid(board):
    rows, cols = len(board), len(board[0])
    print("\nConnect 4 Board:")
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("  " + "   ".join(map(str, range(cols))))

def test_winning_moves():
    # Test 1: Empty board (no winning moves)
    board1 = [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ']
    ]
    print_grid(board1)
    print(f"Test 1: {winning_moves(board1, 'r')}")
    assert winning_moves(board1, 'r') == []

    # Test 2: Horizontal win (r's turn)
    board2 = [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        ['b',' ',' ',' ',' ',' ',' '],
        ['r','r','r',' ','b',' ',' '] 
    ]
    print_grid(board2)
    print(f"Test 2: {winning_moves(board2, 'r')}")
    assert winning_moves(board2, 'r') == [3]

    # Test 3: Vertical win (b's turn)
    board3 = [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        ['b',' ',' ',' ',' ',' ',' '],
        ['b','r',' ',' ',' ',' ',' '],
        ['b','r',' ',' ','r',' ',' '] 
    ]
    print_grid(board3)
    print(f"Test 3: {winning_moves(board3, 'b')}")
    assert winning_moves(board3, 'b') == [0]

    # Test 4: Diagonal win (r's turn)
    board4 = [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ','r','b',' ',' ',' '],
        [' ','r','b','r',' ',' ',' '],
        ['r','b','r','b',' ',' ',' ']  
    ]
    print_grid(board4)
    print(f"Test 4: {winning_moves(board4, 'r')}")
    assert winning_moves(board4, 'r') == [3]

test_winning_moves()
print("All test cases passed!")
