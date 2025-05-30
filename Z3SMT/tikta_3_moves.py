import time
from z3 import Solver, Int, Or, Sum, sat, If, Array, Store, Select, IntSort

def determine_first_player(board, player):
    x_count = sum(row.count('x') for row in board)
    o_count = sum(row.count('o') for row in board)
    return 'x' if x_count < o_count else 'o' if o_count < x_count else player

def can_win_in_three_moves(selected_player, board):
    first_player = determine_first_player(board, selected_player)
    opponent = 'o' if first_player == 'x' else 'x'
    
    s = Solver()
    cells = Array('cells', IntSort(), IntSort())
    original_empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]

    for i in range(3):
        for j in range(3):
            idx = i * 3 + j  #
            current = board[i][j]
            if current == 'x':
                s.add(Select(cells, idx) == 1)
            elif current == 'o':
                s.add(Select(cells, idx) == -1)
            else:
                s.add(Or(Select(cells, idx) == 0,
                        Select(cells, idx) == 1,
                        Select(cells, idx) == -1))

    moves = [Int(f'move_{i}') for i in range(3)]
    current_player = first_player
    board_state = cells
    
    for move_num, move in enumerate(moves):
        s.add(Or([move == (i*3 + j) for i, j in original_empty]))
        
        for prev in range(move_num):
            s.add(move != moves[prev])
        
        player_val = 1 if current_player == 'x' else -1
        board_state = Store(board_state, move, player_val)
        current_player = opponent if current_player == first_player else first_player

    selected_val = 1 if selected_player == 'x' else -1
    win_conds = []
    
    for i in range(3):
        # Rows
        win_conds.append(Sum([Select(board_state, i*3 + j) for j in range(3)]) == 3 * selected_val)
        # Columns
        win_conds.append(Sum([Select(board_state, j*3 + i) for j in range(3)]) == 3 * selected_val)
    
    # Diagonals
    win_conds.append(Sum([Select(board_state, i*3 + i) for i in range(3)]) == 3 * selected_val)
    win_conds.append(Sum([Select(board_state, i*3 + (2-i)) for i in range(3)]) == 3 * selected_val)

    s.add(Or(win_conds))
    return s.check() == sat

def test_win_in_three():
    test_cases = [
        {
            "board": [
                ['x', 'x', 0],
                ['o', 0, 0],
                [0, 0, 0]
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                ['x', 0, 0],
                [0, 'o', 0],
                [0, 0, 'x']
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                ['x', 'o', 0],
                [0, 'x', 0],
                [0, 0, 'o']
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                [0, 0, 0],
                [0, 'x', 0],
                [0, 0, 'o']
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                [0, 'o', 0],
                ['x', 'x', 0],
                [0, 'o', 0]
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                ['x', 'o', 0],
                [0, 'x', 0],
                [0, 'o', 0]
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                ['x', 'o', 'x'],
                ['x', 'o', 'o'],
                ['o', 'x', 'x']
            ],
            "player": 'o',
            "expected": False
        },
        {
            "board": [
                ['x', 0, 'o'],
                [0, 0, 0],
                [0, 0, 0]
            ],
            "player": 'x',
            "expected": True
        },
        {
            "board": [
                ['x', 0, 0],
                [0, 'o', 0],
                [0, 0, 'x']
            ],
            "player": 'o',
            "expected": True
        }
    ]

    average_time = 0
    for i, tc in enumerate(test_cases):
        start_time = time.time()
        result = can_win_in_three_moves(tc["player"], tc["board"])
        end_time = time.time()
        duration = end_time - start_time
        average_time += duration
        print(f"Test case {i+1}: \n {tc['expected']} vs {result} | Time taken: {duration:.6f} seconds")
        assert result == tc["expected"], \
            f"""Test case {i+1} failed:
            Board: {tc['board']}
            Player: {tc['player']}
            Expected: {tc['expected']}
            Got: {result}"""
    average_time /= len(test_cases)
    print(f"Average time taken for test cases: {average_time:.6f} seconds")
    print("All test cases passed!")

test_win_in_three()
