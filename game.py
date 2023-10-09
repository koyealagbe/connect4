"""
    game.py
    Contains the Connect4Game class which keeps track of game infomration
"""

import numpy as np
import random
from ai.state import *
from utils import PLAYER_MODE, AI_MODE

class Connect4Game():
    def __init__(self, game_mode=PLAYER_MODE):
        self.state = GameState(np.zeros((6, 7)), YELLOW_NUM)
        self.game_mode = game_mode
        self.ai_color = None
        self.winner = None
        self.game_over = False
        if self.game_mode == AI_MODE:
            self.ai_color = random.choice([YELLOW_NUM, RED_NUM])

    def make_move(self, col):
        for i in range(self.state.board.shape[0]-1, -1, -1):
            if self.state.board[i][col] == 0:
                self.state.board[i][col] = self.state.turn
                break
        if self.state.is_winning(self.state.turn):
            self.winner = self.state.turn
            self.game_over = True
            return
        elif self.state.is_tie():
            self.game_over = True
            return

        self.state.change_turn()