"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    lista_aplanada = []

    for sublist in board:
        lista_aplanada.extend(sublist)
        
    if lista_aplanada.count(O) == lista_aplanada.count(X) - 1:
        return O        
    return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    res = set()
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                res.add((i,j))
    return res

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    mod_board = copy.deepcopy(board)
        
    if action not in actions(mod_board):
        raise Exception("Illegal action")
    else:
        mod_board[action[0]][action[1]] = player(mod_board)
        return mod_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Vertically        
    t_board = [list(columna) for columna in zip(*board)]
    
    for row in t_board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O
    
    # Horizontaly
    
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O
    
    # Diagonal

    filas = len(board)
    columnas = len(board[0])

    diag_principal = [board[i][i] for i in range(min(filas, columnas))]
    diag_secundaria = [board[i][columnas - i - 1] for i in range(min(filas, columnas))]

    if all(e == X for e in diag_principal) or all(e == X for e in diag_secundaria):
        return X
    elif all(e == O for e in diag_principal) or all(e == O for e in diag_secundaria):
        return O
    
    # Si no se da nada de lo anterior
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    lista_aplanada = []

    for sublist in board:
        lista_aplanada.extend(sublist)
    
    if winner(board) is None and lista_aplanada.count(EMPTY) > 0:
        return False
    return True
    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def max_value(board):
        v = float('-inf')
        
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        for action in actions(board):
            minval = min_value(result(board, action))[0]
            if minval > v:
                v = minval
                optimal_move = action
        return v, optimal_move
        
    def min_value(board):
        v = float('inf')
        
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        for action in actions(board):
            maxval = max_value(result(board, action))[0]
            if maxval < v:
                v = maxval
                optimal_move = action
        return v, optimal_move
    
    curr_player = player(board)

    if terminal(board):
        return None
    if curr_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]