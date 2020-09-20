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

    # no. of moves made by X
    x_played = sum(row.count(X) for row in board)

    # no. of moves made by O
    o_played = sum(row.count(O) for row in board)

    # X's turn if both have played equal moves else O's
    return X if x_played == o_played else O


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
    i = action[0]
    j = action[1]

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

    # TODO check for winner!

    # for row in range(len(board)):
    #     for col in range(len(board[row])):
    #         val =

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
