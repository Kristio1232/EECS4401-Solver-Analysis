import time
from z3 import Solver, Int, Or, And, If, Sum, sat
def winning_moves(player, board):
    s = Solver()
    cells = [[Int(f'cell_{i}_{j}') for j in range(3)] for i in range(3)]
    player_val = 1 if player == 'x' else -1
    original_empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]

    for i in range(3):
        for j in range(3):
            current = board[i][j]
            if current == 'x':
                s.add(cells[i][j] == 1)
            elif current == 'o':
                s.add(cells[i][j] == -1)
            else:
                s.add(Or(cells[i][j] == 0, cells[i][j] == player_val))

    s.add(Sum([If(cells[i][j] == player_val, 1, 0) for (i, j) in original_empty]) == 1)

    win_conds = []
    for i in range(3):
        # Rows
        win_conds.append(Sum(cells[i][0], cells[i][1], cells[i][2]) == 3 * player_val)
        # Columns
        win_conds.append(Sum(cells[0][i], cells[1][i], cells[2][i]) == 3 * player_val)
    # Diagonals
    win_conds.append(Sum(cells[0][0], cells[1][1], cells[2][2]) == 3 * player_val)
    win_conds.append(Sum(cells[0][2], cells[1][1], cells[2][0]) == 3 * player_val)

    s.add(Or(win_conds))
    
    moves = []
    while s.check() == sat:
        model = s.model()
        move = None
        for (i, j) in original_empty:
            if model.evaluate(cells[i][j]).as_long() == player_val:
                move = (i, j)
                break
        if move:
            moves.append(move)
            s.add(cells[move[0]][move[1]] != player_val)
        else:
            break
    return moves


def test_winning_moves():
    test_cases = [
        # Horizontal win (single move)
        {
            "board": [
                ['x', 'x', 0],
                ['o', 0, 'o'],
                [0, 0, 0]
            ],
            "player": 'x',
            "expected": [(0, 2)]
        },
        # Vertical win (two possible moves)
        {
            "board": [
                ['o', 0, 0],
                ['o', 'x', 0],
                [0, 'x', 0]
            ],
            "player": 'o',
            "expected": [(2, 0)]
        },
        # Diagonal win (center move)
        {
            "board": [
                ['x', 'o', 0],
                [0, 0, 'o'],
                [0, 0, 'x']
            ],
            "player": 'x',
            "expected": [(1, 1)]
        },
        # No winning moves
        {
            "board": [
                ['x', 'o', 'x'],
                ['o', 'o', 'x'],
                ['x', 'x', 'o']
            ],
            "player": 'o',
            "expected": []
        }
    ]

    average_time = 0
    for i, tc in enumerate(test_cases):
        start_time = time.time()
        result = winning_moves(tc["player"], tc["board"])
        end_time = time.time()
        duration = end_time - start_time
        average_time += duration
        print(f"Test {i+1}: {tc['expected']} vs {result} | Time taken: {duration:.6f} seconds")
        assert sorted(result) == sorted(tc["expected"]), \
            f"Test {i+1} failed: Expected {tc['expected']}, Got {result}"
    average_time /= len(test_cases)
    print(f"\nAverage time taken: {average_time:.6f} seconds")
    print("All tests passed!")

test_winning_moves()
