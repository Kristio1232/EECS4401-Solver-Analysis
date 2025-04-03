import time
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
    test_cases = [
        {
            "name": "Empty board (no winning moves)",
            "board": [
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' ']
            ],
            "player": 'r',
            "expected": []
        },
        {
            "name": "Horizontal win (r's turn)",
            "board": [
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                ['b',' ',' ',' ',' ',' ',' '],
                ['r','r','r',' ','b',' ',' ']
            ],
            "player": 'r',
            "expected": [3]
        },
        {
            "name": "Vertical win (b's turn)",
            "board": [
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                ['b',' ',' ',' ',' ',' ',' '],
                ['b','r',' ',' ',' ',' ',' '],
                ['b','r',' ',' ','r',' ',' ']
            ],
            "player": 'b',
            "expected": [0]
        },
        {
            "name": "Diagonal win (r's turn)",
            "board": [
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ','r','b',' ',' ',' '],
                [' ','r','b','r',' ',' ',' '],
                ['r','b','r','b',' ',' ',' ']
            ],
            "player": 'r',
            "expected": [3]
        }
    ]

    average_time = 0
    for i, tc in enumerate(test_cases):
        start_time = time.time()
        
        print(f"\nTest {i+1}: {tc['name']}")
        print_grid(tc["board"])
        result = winning_moves(tc["board"], tc["player"])
        
        end_time = time.time()
        duration = end_time - start_time
        average_time += duration
        print(f"Expected: {tc['expected']}, Got: {result}")
        print(f"Time taken: {duration:.6f} seconds")
        
        assert sorted(result) == sorted(tc["expected"]), \
            f"Test {i+1} failed: Expected {tc['expected']}, Got {result}"
    average_time /= len(test_cases)
    
    print("\nAll test cases passed!")

test_winning_moves()
