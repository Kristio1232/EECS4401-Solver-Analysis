from z3 import Solver, Int, Or, And, If, Sum, sat

def analyze_tictactoe(board):
    solver = Solver()
    
    # Create Z3 variables (0=empty, 1=X, 2=O)
    z3_board = [[Int(f'cell_{i}_{j}') for j in range(3)] for i in range(3)]
    
    x_count = sum(1 for row in board for cell in row if cell == 'X')
    o_count = sum(1 for row in board for cell in row if cell == 'O')
    
    if abs(x_count - o_count) > 1:
        return "Invalid move count"
    
    current_player = 1 if x_count == o_count else 2
    
    move_diff = []
    for i in range(3):
        for j in range(3):
            current = board[i][j]
            if current == 'X':
                solver.add(z3_board[i][j] == 1)
            elif current == 'O':
                solver.add(z3_board[i][j] == 2)
            else:
                solver.add(Or(z3_board[i][j] == 0, z3_board[i][j] == current_player))
                move_diff.append(If(z3_board[i][j] == current_player, 1, 0))

    solver.add(Sum(move_diff) == 1)

    win_cond = Or(
        # Rows
        *[And(z3_board[i][0] == current_player, 
             z3_board[i][1] == current_player,
             z3_board[i][2] == current_player) for i in range(3)],
        # Columns
        *[And(z3_board[0][j] == current_player,
             z3_board[1][j] == current_player,
             z3_board[2][j] == current_player) for j in range(3)],
        # Diagonals
        And(z3_board[0][0] == current_player,
            z3_board[1][1] == current_player,
            z3_board[2][2] == current_player),
        And(z3_board[0][2] == current_player,
            z3_board[1][1] == current_player,
            z3_board[2][0] == current_player)
    )
    solver.add(win_cond)
    if solver.check() == sat:
        model = solver.model()
        return [(i, j) for i in range(3) for j in range(3)
                if model.eval(z3_board[i][j]).as_long() == current_player
                and board[i][j] == ' ']
    return None

def run_tests(test_cases):
    for idx, test_case in enumerate(test_cases):
        print(f"Running Test {idx + 1}: {test_case['description']}")
        result = analyze_tictactoe(test_case["board"])
        if result:
            print(f"Winning moves: {result}")
        else:
            print("No winning moves available")
        print("-" * 40)

test_cases = [
        {
            "board": [
                ['X', ' ', 'O'],
                [' ', 'X', ' '],
                [' ', ' ', ' ']
            ],
            "description": "Test case where X can win with a diagonal move"
        },
        {
            "board": [
                ['X', 'O', 'X'],
                ['O', 'X', 'O'],
                [' ', ' ', 'X']
            ],
            "description": "Test case where X has already won"
        },
        {
            "board": [
                ['X', 'O', 'X'],
                ['O', 'X', 'O'],
                [' ', ' ', 'O']
            ],
            "description": "Test case where O can win with a vertical move"
        },
        {
            "board": [
                ['X', 'O', 'X'],
                ['O', 'X', 'O'],
                ['O', ' ', 'X']
            ],
            "description": "Test case where no winning moves are possible"
        },
        {
            "board": [
                [' ', ' ', ' '],
                [' ', ' ', ' '],
                [' ', ' ', ' ']
            ],
            "description": "Empty board test case"
        }
    ]

run_tests(test_cases)
