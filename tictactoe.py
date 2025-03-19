import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    def max_value(board):
        if terminal(board):
            return utility(board), None  
        v = -math.inf
        best_move = None
        for action in actions(board):
            value, _ = min_value(result(board, action)) 
            if value > v:
                v = value
                best_move = action
        return v, best_move  

    def min_value(board):
        if terminal(board):
            return utility(board), None  
        v = math.inf
        best_move = None
        for action in actions(board):
            value, _ = max_value(result(board, action))  
            if value < v:
                v = value
                best_move = action
        return v, best_move 

    _, move = max_value(board) if current_player == X else min_value(board) 
    return move


def print_board(board):
    for row in board:
        print(" ".join([cell if cell is not None else "-" for cell in row]))
    print()

def play_game():
    board = initial_state()
    while not terminal(board):
        print_board(board)
        if player(board) == X:
            row, col = map(int, input("Enter your move (row col): ").split())
            if (row, col) in actions(board):
                board = result(board, (row, col))
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is making a move...")
            move = minimax(board)
            if move:
                board = result(board, move)
    
    print_board(board)
    if winner(board):
        print(f"Winner: {winner(board)}")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
