# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    if board.count_pieces() == 42:
        return True
    for chain in board.get_all_chains():
        if len(chain) >= 4:
            return True
    return False

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""

    if is_game_over_connectfour(board):
        return []

    toReturn = []
    for col in range(0, 7):
        if board.is_column_full(col):
            continue
        toReturn.append(board.copy().add_piece(col))
    return toReturn

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    for chain in board.get_all_chains():
        if len(chain) >= 4:
            if is_current_player_maximizer:
                return -1000
            return 1000
    # if there is no chain of length 4+, it's a tie
    return 0
def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""

    time_penalty = 1000 * board.count_pieces()/42
    for chain in board.get_all_chains():
        if len(chain) >= 4:
            if is_current_player_maximizer:
                return -2000 + time_penalty
            return 2000 - time_penalty
    return 0

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""

    # take length of chains and number of chains into account
    score1 = 0.
    score2 = 0.
    for chain in board.get_all_chains():
        if chain[0] == 1:
            score1 += len(chain)**2
        else:
            score2 += len(chain)**2
    if is_current_player_maximizer:
        return (score1-score2)/(score1+score2) * 1000
    return -1 * (score1-score2)/(score1+score2) * 1000


# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

num_evaluations = 0

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    global num_evaluations
    if state.is_game_over():
        num_evaluations += 1
        return ([state], state.get_endgame_score(), num_evaluations)

    best = ([], 0, 0)
    for nextState in state.generate_next_states():
        temp = dfs_maximizing(nextState)
        temp[0].insert(0, state)
        if temp[1] > best[1]:
            best = (temp[0], temp[1], temp[2])
    best = (best[0], best[1], num_evaluations)
    return best

def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize), 1)

    num_evaluations_minimax = 0

    best = ([], 0, 0)
    if maximize:
        best = ([], -1*INF, 0)
    else:
        best = ([], INF, 0)

    for nextState in state.generate_next_states():
        temp = minimax_endgame_search(nextState, (not maximize))
        num_evaluations_minimax += temp[2]
        temp[0].insert(0, state)
        if maximize:
            if temp[1] > best[1]:
                best = (temp[0], temp[1], temp[2])
        else:
            if temp[1] < best[1]:
                best = (temp[0], temp[1], temp[2])
    best = (best[0], best[1], num_evaluations_minimax)
    return best

# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    if state.is_game_over():
        return ([state], state.get_endgame_score(maximize), 1)
    if depth_limit == 0:
        return ([state], heuristic_fn(state.get_snapshot(), maximize), 1)
    num_evaluations_minimax_real = 0
    best = ([], 0, 0)
    if maximize:
        best = ([], -1*INF, 0)
    else:
        best = ([], INF, 0)
    for nextState in state.generate_next_states():
        temp = minimax_search(nextState, heuristic_fn, depth_limit-1, (not maximize))
        num_evaluations_minimax_real += temp[2]
        temp[0].insert(0, state)
        if maximize:
            if temp[1] > best[1]:
                best = (temp[0], temp[1], temp[2])
        else:
            if temp[1] < best[1]:
                best = (temp[0], temp[1], temp[2])
    best = (best[0], best[1], num_evaluations_minimax_real)
    return best

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    #print(maximize)
    #print(state)
    #print()
    if state.is_game_over():
        #print("Returned: " + str(([state], state.get_endgame_score(maximize), 1)))
        return ([state], state.get_endgame_score(maximize), 1)
    if depth_limit == 0:
        return ([state], heuristic_fn(state.get_snapshot(), maximize), 1)
    worst_score = 0
    if maximize:
        worst_score = -INF
    else:
        worst_score = INF
    best = ([], worst_score, 0)
    num_evaluations_alphabeta = 0
    new_alpha = alpha
    new_beta = beta
    for nextState in state.generate_next_states():
        temp = minimax_search_alphabeta(nextState, new_alpha, new_beta, heuristic_fn, depth_limit-1, (not maximize))
        num_evaluations_alphabeta += temp[2]
        temp[0].insert(0, state)
        if maximize:
            if temp[1] > new_alpha:
                best = (temp[0], temp[1], temp[2])
                new_alpha = temp[1]
        else:
            if temp[1] < new_beta:
                best = (temp[0], temp[1], temp[2])
                new_beta = temp[1]
        if new_alpha >= new_beta:
            break
    best = (best[0], best[1], num_evaluations_alphabeta)
    #print(new_alpha, new_beta)
    #print("returned: " + str((best[0], best[1], num_evaluations_alphabeta)))
    return best

# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    i = 1
    while i <= depth_limit:
        anytime_value.set_value(minimax_search_alphabeta(state, -INF, INF, heuristic_fn, i, True))
        i += 1
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = "Grace Yin"
COLLABORATORS = "Arezu Esmaili, Allison Tam"
HOW_MANY_HOURS_THIS_LAB_TOOK = "5"
WHAT_I_FOUND_INTERESTING = "Minimax"
WHAT_I_FOUND_BORING = "literally nothing. These labs are great :D"
SUGGESTIONS = "Please have mercy...... 3 psets in the span of one week is painful... :'( "
