"""
    state.py
    Contains the GameState class which keeps track of the internal game state
"""

import numpy as np
from ai.minimax import minimax
from utils import YELLOW_NUM, RED_NUM

ACTIONS = [0, 1, 2, 3, 4, 5, 6]

class GameState:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn

    def change_turn(self):
        self.turn = RED_NUM if self.turn == YELLOW_NUM else YELLOW_NUM
    
    def is_winning(self, player_num):
        # check horizontals
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if self.board[i][j] == player_num and self.board[i][j+1] == player_num and self.board[i][j+2] == player_num and self.board[i][j+3] == player_num:
                    return True
                
        # Check verticals
        for j in range(self.board.shape[1]):
            for i in range(self.board.shape[0]-3):
                if self.board[i][j] == player_num and self.board[i+1][j] == player_num and self.board[i+2][j] == player_num and self.board[i+3][j] == player_num:
                    return True
        
        # Check positive diagonals
        for i in range(3, self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if self.board[i][j] == player_num and self.board[i-1][j+1] == player_num and self.board[i-2][j+2] == player_num and self.board[i-3][j+3] == player_num:
                    return True
                
        # Check negative diagonals
        for i in range(self.board.shape[0]-3):
            for j in range(self.board.shape[1]-3):
                if self.board[i][j] == player_num and self.board[i+1][j+1] == player_num and self.board[i+2][j+2] == player_num and self.board[i+3][j+3] == player_num:
                    return True

        return False

    def is_tie(self):
        return np.count_nonzero(self.board==0) == 0
    
    def is_legal_action(self, action):
        return self.board[0][action] == 0
    
    def get_legal_actions(self, sort=False):
        legal_actions = []
        for action in ACTIONS:
            if self.is_legal_action(action):
                legal_actions.append(action)
        if not sort:
            return legal_actions
        
        # If sort == True, sort actions by depth 0 evaluation
        return sorted(legal_actions, key=lambda x: minimax(self.get_new_state(x), depth=0))
    
    def get_new_state(self, action):
        if self.is_legal_action(action):
            new_board = self.board.copy()
            for i in range(new_board.shape[0]-1, -1, -1):
                if new_board[i][action] == 0:
                    new_board[i][action] = self.turn
                    break
            return GameState(new_board, YELLOW_NUM if self.turn == RED_NUM else RED_NUM)
        return self
    
    def get_evaluation(self, depth=2):
        return minimax(self, depth=depth) # Potentially substitute for different algorithm
    
    def count_three_in_row(self):
        count = 0
        # Horizontal
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == 0):
                    count -= 1
                
        # Vertical
        for j in range(self.board.shape[1]):
            for i in range(self.board.shape[0]-3):
                if (self.board[i][j] == 0 and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == 0):
                    count -= 1
        
        # Positive diagonal
        for i in range(3, self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == 0):
                    count -= 1
                
        # Negative diagonal
        for i in range(self.board.shape[0]-3):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == 0):
                    count -= 1
        
        return count

    def count_two_in_row(self):
        count = 0
        # Horizontal
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i][j+1] == 0 and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == 0 and self.board[i][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == YELLOW_NUM and self.board[i][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i][j+1] == YELLOW_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i][j+1] == 0 and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == 0 and self.board[i][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == 0 and self.board[i][j+2] == RED_NUM and self.board[i][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i][j+1] == RED_NUM and self.board[i][j+2] == 0 and self.board[i][j+3] == 0):
                    count -= 1
                
        # Vertical
        for j in range(self.board.shape[1]):
            for i in range(self.board.shape[0]-3):
                if (self.board[i][j] == 0 and self.board[i+1][j] == 0 and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == 0 and self.board[i+3][j] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == YELLOW_NUM and self.board[i+3][j] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j] == YELLOW_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i+1][j] == 0 and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == 0 and self.board[i+3][j] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == 0 and self.board[i+2][j] == RED_NUM and self.board[i+3][j] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j] == RED_NUM and self.board[i+2][j] == 0 and self.board[i+3][j] == 0):
                    count -= 1
        
        # Positive diagonal
        for i in range(3, self.board.shape[0]):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == YELLOW_NUM and self.board[i-3][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i-1][j+1] == YELLOW_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == 0 and self.board[i-2][j+2] == RED_NUM and self.board[i-3][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i-1][j+1] == RED_NUM and self.board[i-2][j+2] == 0 and self.board[i-3][j+3] == 0):
                    count -= 1
                
        # Negative diagonal
        for i in range(self.board.shape[0]-3):
            for j in range(self.board.shape[1]-3):
                if (self.board[i][j] == 0 and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == YELLOW_NUM) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == YELLOW_NUM and self.board[i+3][j+3] == 0) or \
                    (self.board[i][j] == YELLOW_NUM and self.board[i+1][j+1] == YELLOW_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == 0):
                    count += 1
                elif (self.board[i][j] == 0 and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == 0 and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == RED_NUM) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == 0 and self.board[i+2][j+2] == RED_NUM and self.board[i+3][j+3] == 0) or \
                    (self.board[i][j] == RED_NUM and self.board[i+1][j+1] == RED_NUM and self.board[i+2][j+2] == 0 and self.board[i+3][j+3] == 0):
                    count -= 1
        
        return count
    
    def count_center(self):
        count = 0
        j = 3
        for i in range(self.board.shape[0]):
            if self.board[i][j] == YELLOW_NUM:
                count += 1
            elif self.board[i][j] == RED_NUM:
                count -= 1

        return count
    