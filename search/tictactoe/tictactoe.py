"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    y_count = 0
    for row in board:
        x_count += row.count(X)
        y_count += row.count(O)
    return X if x_count == y_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                result.add((i, j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    from copy import deepcopy

    if valid_action(board, action) is False:
        raise Exception("action must be valid")

    (i, j) = action
    copied_board = deepcopy(board)
    copied_board[i][j] = player(board)
    return copied_board


def valid_action(board, action):
    (i, j) = action
    return (
        i >= 0
        and i < len(board)
        and j >= 0
        and j < len(board[0])
        and board[i][j] == EMPTY
    )


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    if board[1][1] != EMPTY and (
        (board[0][0] == board[1][1] == board[2][2])
        or (board[0][2] == board[1][1] == board[2][0])
    ):
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    has_empty = False

    for i in range(len(board)):
        if board[i].count(EMPTY):
            has_empty = True
        if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return True
        if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return True

    if board[1][1] != EMPTY and (
        (board[0][0] == board[1][1] == board[2][2])
        or (board[0][2] == board[1][1] == board[2][0])
    ):
        return True

    return has_empty is False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    _winner = winner(board)
    if _winner == X:
        return 1
    elif _winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    import math

    def max_value(state, alpha=-math.inf, beta=math.inf):
        if terminal(state):
            return (None, utility(state))
        value = -math.inf
        best_action = None
        for action in actions(state):
            _value = min_value(result(state, action))[1]
            if value < _value:
                value = _value
                best_action = action
            alpha = max(value, alpha)
            if beta <= alpha:
                break
        return (best_action, value)

    def min_value(state, alpha=-math.inf, beta=math.inf):
        if terminal(state):
            return (None, utility(state))
        value = math.inf
        best_action = None
        for action in actions(state):
            _value = max_value(result(state, action))[1]
            if value > _value:
                value = _value
                best_action = action
            beta = min(value, beta)
            if beta <= alpha:
                break
        return (best_action, value)

    if player(board) == X:
        return max_value(board)[0]
    else:
        return min_value(board)[0]
