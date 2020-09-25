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

    # no. of moves made in total
    played = sum(row.count(EMPTY) for row in board)

    # X's turn if both have played equal moves else O's
    return O if played % 2 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # store a (row, col) tuple where a move can be made
    possible_moves = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            # if current cell is empty then add it as a possible move
            if board[row][col] == EMPTY:
                possible_moves.add((row, col))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # check if action is valid
    if board[i][j] != EMPTY:
        raise NameError("Invalid action!")

    # deep clone so that the internal states are also copied
    board_clone = copy.deepcopy(board)

    # make the move returned by the player() to the cloned board
    board_clone[i][j] = player(board)

    return board_clone


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    col_val = [0, 0, 0]
    getVal = {X: 1, O: -1}
    left_diagonal = 0
    right_diagonal = 0
    length = len(board)

    for row in range(length):
        row_val = 0
        for col in range(len(board[row])):
            val = getVal.get(board[row][col], 0)
            row_val += val
            col_val[col] += val
            if row == col:
                left_diagonal += val
            if length - col - 1 == row:
                right_diagonal += val
        if 3 in [row_val, left_diagonal, right_diagonal, *col_val]:
            return X
        if -3 in [row_val, left_diagonal, right_diagonal, *col_val]:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for col in row:
            if col is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {None: 0, X: 1, O: -1}[winner(board)]


def maximize(board):
    """
    Maximizes the value of the board, i.e. optimal for X
    """
    if terminal(board):
        return utility(board)

    max_val = -math.inf
    for action in actions(board):
        max_val = max(max_val, minimize(result(board, action)))
    return max_val


def minimize(board):
    """
    Minimizes the value of the board, i.e. optimal for O
    """
    if terminal(board):
        return utility(board)

    min_val = math.inf
    for action in actions(board):
        min_val = min(min_val, maximize(result(board, action)))
    return min_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
        return (1, 1)

    current_player = player(board)
    do_action = EMPTY
    if current_player == X:
        X_value = -math.inf
        for action in actions(board):
            O_optimal = minimize(result(board, action))
            if X_value < O_optimal:
                X_value = O_optimal
                do_action = action
    elif current_player == O:
        O_value = math.inf
        for action in actions(board):
            X_optimal = maximize(result(board, action))
            if O_value > X_optimal:
                O_value = X_optimal
                do_action = action
    return do_action
