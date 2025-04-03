import time
from z3 import Solver, Array, ArraySort, IntSort, Int, Or, And, If, Implies, ForAll, Sum, sat, Store, Select

def can_win_in_three_moves(player, board):
    s = Solver()
    rows, cols = 6, 7
    player_num = 1 if player == 'r' else 2
    opponent_num = 3 - player_num
    k = Int('k')

    inner_array = ArraySort(IntSort(), IntSort())
    Grid = Array('Grid', IntSort(), inner_array)
    
    for i in range(rows):
        row = Array(f'row_{i}', IntSort(), IntSort())
        for j in range(cols):
            val = 1 if board[i][j] == 'r' else (2 if board[i][j] == 'b' else 0)
            row = Store(row, j, val)
        Grid = Store(Grid, i, row)

    player_count = Sum([If(Select(Select(Grid, i), j) == player_num, 1, 0) 
                       for i in range(rows) for j in range(cols)])
    opponent_count = Sum([If(Select(Select(Grid, i), j) == opponent_num, 1, 0)
                         for i in range(rows) for j in range(cols)])

    current_player = Int('current_player')
    s.add(current_player == If(player_count <= opponent_count, player_num, opponent_num))

    for move_num in range(3):
        col = Int(f'col_{move_num}')
        row = Int(f'row_{move_num}')
        
        s.add(0 <= col, col < cols)
        
        row_constraints = []
        for i in range(rows):
            row_constraints.append(
                And(
                    Select(Select(Grid, i), col) == 0,
                    ForAll([k], Implies(
                        And(k > i, k < rows),
                        Select(Select(Grid, k), col) != 0
                    ))
                )
            )
        s.add(Or(row_constraints))
        s.add(row == Sum([If(cond, i, 0) for i, cond in enumerate(row_constraints)]))
        
        new_row = Store(Select(Grid, row), col, current_player)
        Grid = Store(Grid, row, new_row)
        
        current_player = If(current_player == player_num, opponent_num, player_num)

    win_cond = Or(
        # Horizontal
        Or([And(
            Select(Select(Grid, i), j) == player_num,
            Select(Select(Grid, i), j+1) == player_num,
            Select(Select(Grid, i), j+2) == player_num,
            Select(Select(Grid, i), j+3) == player_num
        ) for i in range(rows) for j in range(cols-3)]),
        
        # Vertical
        Or([And(
            Select(Select(Grid, i), j) == player_num,
            Select(Select(Grid, i+1), j) == player_num,
            Select(Select(Grid, i+2), j) == player_num,
            Select(Select(Grid, i+3), j) == player_num
        ) for i in range(rows-3) for j in range(cols)]),
        
        # Diagonal down
        Or([And(
            Select(Select(Grid, i), j) == player_num,
            Select(Select(Grid, i+1), j+1) == player_num,
            Select(Select(Grid, i+2), j+2) == player_num,
            Select(Select(Grid, i+3), j+3) == player_num
        ) for i in range(rows-3) for j in range(cols-3)]),
        
        # Diagonal up
        Or([And(
            Select(Select(Grid, i), j) == player_num,
            Select(Select(Grid, i-1), j+1) == player_num,
            Select(Select(Grid, i-2), j+2) == player_num,
            Select(Select(Grid, i-3), j+3) == player_num
        ) for i in range(3, rows) for j in range(cols-3)])
    )

    s.add(win_cond)
    return s.check() == sat

TEST_CASES = [
    # Test 1: Empty board (player needs 4 moves)
    ('r', [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ']
    ], False),

    
    # Test 3: Vertical win possible (3 in column)
    ('b', [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        ['b',' ',' ',' ',' ',' ',' '],
        ['b',' ','r',' ',' ',' ',' '],
        ['b','r','r',' ',' ',' ',' '],
        ['r','b','r',' ',' ',' ',' ']
    ], True),
    
    # Test 4: Blocked diagonal (3 with blocker)
    ('r', [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ','r','b',' ',' ',' '],
        [' ',' ','b','r',' ',' ',' '],
        [' ','b','r','b',' ',' ',' '],
        ['r','r','b','r',' ',' ',' ']
    ], False),

    
    # Test 6: Alternating pieces (win in 3 moves)
    ('r', [
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ','r',' ',' ',' ',' '],
        [' ','r','b',' ',' ',' ',' '],
        ['r','b','b',' ',' ',' ',' ']
    ], False)
]


def run_tests():
    passed = 0
    average_time = 0
    print("Running tests...")
    for i, (player, board, expected) in enumerate(TEST_CASES, 1):
        print(f"\nTest {i}: {'Horizontal' if i==2 else 'Vertical' if i==3 else 'Diagonal' if i==4 else ''}")
        print(f"Player: {player}")
        for row in board:
            print('|' + '|'.join(row) + '|')
        
        try:
            start_time = time.time()
            result = can_win_in_three_moves(player, board)
            end_time = time.time()
            duration = end_time - start_time
            average_time += duration
            print(f"Result: {result} | Expected: {expected} | Time taken: {duration:.6f} seconds")
            if result == expected:
                passed += 1
            else:
                print("Test Failed")
        except Exception as e:
            print(f"Error: {str(e)}")
    average_time /= len(TEST_CASES)
    print(f"\nAverage time per test: {average_time:.6f} seconds")
    print(f"\nPassed {passed}/{len(TEST_CASES)} tests")

run_tests()