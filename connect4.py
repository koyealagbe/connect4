"""
  connect4.py
  Main game executable
"""

import pygame
from pygame.locals import *
from gui import *
from utils import *
from game import *
from ai.agent import *

# Main menu screen
def main(screen):
    running = True

    screen.fill(BLACK)
    
    # Menu screen title text element
    title_text = Text("Connect 4!", "Courier New", 48, YELLOW)
    title_text.position_center(SCREEN_WIDTH // 2, 32)

    # 2 player mode button element
    player_button = Button(
        x=SCREEN_WIDTH // 2 - (MENU_BUTTON_WIDTH / 2), y=200, width=MENU_BUTTON_WIDTH, height=MENU_BUTTON_HEIGHT, 
        bg_color=BLUE, text="Player vs. Player", font_name="Courier New", 
        font_size=28, font_color=WHITE
    )

    # AI mode button element
    ai_button = Button(
        x=SCREEN_WIDTH // 2 - (MENU_BUTTON_WIDTH / 2), y=300, width=MENU_BUTTON_WIDTH, height=MENU_BUTTON_HEIGHT, 
        bg_color=RED, text="Player vs. AI", font_name="Courier New", 
        font_size=28, font_color=BLACK
    )

    # Menu screen loop
    while running:

        screen.blit(title_text.obj, title_text.rect)

        player_button.draw(screen)
        ai_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if player_button.is_hovering():
                    play(screen, PLAYER_MODE)
                elif ai_button.is_hovering():
                    play(screen, AI_MODE)
        
        pygame.display.update()

# Game screen
def play(screen, mode):
    # Game object
    game_obj = Connect4Game(game_mode=mode)
    
    if mode == AI_MODE:
        bot = Agent(algorithm="minimax", depth=BOT_DEPTH)

    screen.fill(BLACK)

    # Text element stating whose turn it is
    turn_text = Text("", "Courier New", 32, RED)

    # Game over text element 
    game_over_text = Text("", "Courier New", 48, WHITE)

    # Draw board
    board_width = CIRCLE_RADIUS*2*7 + BOARD_PADDING*8
    board_height = CIRCLE_RADIUS*2*6 + BOARD_PADDING*7
    board_x = SCREEN_WIDTH / 2 - (board_width / 2)
    board_y = 144
    pygame.draw.rect(screen, BLUE, (board_x, board_y, board_width, board_height))
    
    # Create circles
    grid_x = board_x
    grid_y = board_y - (BOARD_PADDING+CIRCLE_RADIUS*2)
    circles = []
    for i in range(7):
        circles.append([])
        for j in range(7):
            circles[i].append(Circle(grid_x + BOARD_PADDING + (BOARD_PADDING+CIRCLE_RADIUS*2)*j, grid_y + BOARD_PADDING + (BOARD_PADDING+CIRCLE_RADIUS*2)*i, CIRCLE_RADIUS))

    # Main game loop
    running = True
    while running:
        # Set text according to turn
        screen.fill(BLACK, turn_text.rect)
        if game_obj.game_mode == PLAYER_MODE:
            turn_text.set_text(f"Player {game_obj.state.turn}'s Turn", RED if game_obj.state.turn == RED_NUM else YELLOW)
        else:
            if game_obj.state.turn == RED_NUM:
                turn_text.set_text("AI's Turn" if game_obj.ai_color == RED_NUM else "Player 1's Turn", RED)
            else:
                turn_text.set_text("AI's Turn" if game_obj.ai_color == YELLOW_NUM else "Player 1's Turn", YELLOW)
        turn_text.position_center(SCREEN_WIDTH / 2, 32)
        screen.blit(turn_text.obj, turn_text.rect)

        # Draw grid of circles
        for i in range(len(circles[0])):
            for j in range(len(circles[0])):
                if i == 0:
                    circles[i][j].draw(screen, BLACK)
                else:
                    # Draw according to board array
                    if game_obj.state.board[i-1][j] == 0:
                        circles[i][j].draw(screen, DARK_BLUE)
                    elif game_obj.state.board[i-1][j] == RED_NUM:
                        circles[i][j].draw(screen, RED)
                    else:
                        circles[i][j].draw(screen, YELLOW)

        # Draw game over text if game over
        if game_obj.game_over:
            if game_obj.winner: # Someone won
                if game_obj.game_mode == PLAYER_MODE:
                    game_over_text.set_text(f"Player {game_obj.winner} Wins!", RED if game_obj.state.turn == RED_NUM else YELLOW)
                else:
                    if game_obj.winner == RED_NUM:
                        game_over_text.set_text("AI Wins!" if game_obj.ai_color == RED_NUM else f"Player 1 Wins!", RED)
                    else:
                        game_over_text.set_text("AI Wins!" if game_obj.ai_color == YELLOW_NUM else f"Player 1 Wins!", YELLOW)
            else: # Tie
                game_over_text.set_text("Tie!", WHITE)
            game_over_text.position_center(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            screen.fill(BLACK, game_over_text.rect)
            screen.blit(game_over_text.obj, game_over_text.rect)
        else: # Game not over
            if not (game_obj.game_mode == AI_MODE and game_obj.state.turn == game_obj.ai_color):
                # For all the circles in the top row, check if mouse is hovering over
                for i in range(len(circles[0])):
                    if circles[0][i].is_hovering():
                        circles[0][i].draw(screen, RED if game_obj.state.turn == RED_NUM else YELLOW)
                    else:
                        circles[0][i].draw(screen, BLACK)
            else: # AI mode, AI's turn, don't do mouse hover check
                pygame.display.update() # Make sure the previous move is made visually before the AI starts thinking

                ai_move = bot.get_move(game_obj.state)

                # For the visuals, hover over the selected move before playing it
                for i in range(ai_move + 1):
                    circles[0][i].draw(screen, RED if game_obj.ai_color == RED_NUM else YELLOW)
                    pygame.display.update()
                    pygame.time.wait(100)
                    circles[0][i].draw(screen, BLACK)
                pygame.time.wait(500)

                game_obj.make_move(ai_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    screen.fill(BLACK)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN: # If a top row circle is clicked, make the corresponding move for the current player
                if not game_obj.game_over:
                    if not (game_obj.game_mode == AI_MODE and game_obj.state.turn == game_obj.ai_color):
                        for i in range(len(circles[0])):
                            if circles[0][i].is_hovering():
                                if game_obj.state.is_legal_action(i):
                                    game_obj.make_move(i)

        pygame.display.update()

# Run the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4!")

# Run the main menu
main(screen=screen)

pygame.quit()