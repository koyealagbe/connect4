"""
  agent.py
  Contains the Agent class which controls the bot
"""

import random
from ai.state import *
from utils import *

class Agent:
    def __init__(self, algorithm="random", depth=None):
        self.algorithm = algorithm
        self.depth = depth

    # Given a state, generate the next move based on the algorithm
    def get_move(self, state):
        if self.algorithm == "random":
          return random.choice(state.get_legal_actions())
        elif self.algorithm == "minimax":
            if self.depth == None:
                return None
            legal_actions = state.get_legal_actions()
            best_action = None
            best_evaluation = WIN_SCORE+1 if state.turn == RED_NUM else -WIN_SCORE-1
            for action in legal_actions:
                new_state = state.get_new_state(action)
                evaluation = new_state.get_evaluation(depth=self.depth)
                if state.turn == YELLOW_NUM:
                    if evaluation > best_evaluation:
                        best_evaluation = evaluation
                        best_action = action
                else:
                    if evaluation < best_evaluation:
                        best_evaluation = evaluation
                        best_action = action
            return best_action
        
        return None
