"""
  minimax.py
  Minimax algorithm implementation
"""

import math
from utils import *

def minimax(state, alpha=-math.inf, beta=math.inf, depth=2):
    if state.is_winning(YELLOW_NUM):
        return WIN_SCORE
    if state.is_winning(RED_NUM):
        return -WIN_SCORE
    if state.is_tie():
        return 0
    if depth == 0:
        # Custom value function that counts potential 4-in-a-rows. Potential rows of length 3 are weighted higher than potential rows of length 2
        # Slight preference for piecs in the center
        return THREE_IN_ROW_MULT * state.count_three_in_row() + TWO_IN_ROW_MULT * state.count_two_in_row() + CENTER_MULT * state.count_center()
    
    legal_actions = state.get_legal_actions(sort=True)
    if state.turn == YELLOW_NUM:
        max_evaluation = -math.inf
        for action in legal_actions:
            evaluation = minimax(state.get_new_state(action), alpha, beta, depth-1)
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(evaluation, alpha)
            if beta <= alpha:
                break
        return max_evaluation
    else:
        min_evaluation = math.inf
        for action in legal_actions:
            evaluation = minimax(state.get_new_state(action), alpha, beta, depth-1)
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(evaluation, beta)
            if beta <= alpha:
                break
        return min_evaluation
