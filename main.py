import pygame
import sys
import random
from time import sleep

# Constants
WIDTH = 400
HEIGHT = 400
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (23, 145, 135)
X_COLOR = (200, 50, 50)
O_COLOR = (50, 200, 50)
FPS = 60

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Fonts
font = pygame.font.SysFont(None, 40)

# Function to draw the grid
def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw X
def draw_x(row, col):
    pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 25, row * SQUARE_SIZE + 25),
                     ((col + 1) * SQUARE_SIZE - 25, (row + 1) * SQUARE_SIZE - 25), 5)
    pygame.draw.line(screen, X_COLOR, ((col + 1) * SQUARE_SIZE - 25, row * SQUARE_SIZE + 25),
                     (col * SQUARE_SIZE + 25, (row + 1) * SQUARE_SIZE - 25), 5)

# Function to draw O
def draw_o(row, col):
    pygame.draw.circle(screen, O_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                       SQUARE_SIZE // 2 - 25, 3)

# Function to check if a move is valid
def is_valid_move(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " "

# Function to check if the board is full
def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Function to check if a player has won
def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# MiniMax Algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, "O"):
        return -10 + depth, None
    elif check_winner(board, "X"):
        return 10 - depth, None
    elif is_board_full(board):
        return 0, None

    if is_maximizing:
        best_score = float("-inf")
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score, _ = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score, _ = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = " "
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move

# Function for AI move
def ai_move(board, level):
    if level == 1:
        # Choose a random move
        return random.choice([(i, j) for i in range(3) for j in range(3) if board[i][j] == " "])
    elif level == 3:
        # Use minimax algorithm with basic evaluation
        _, best_move = minimax(board, 0, True, float("-inf"), float("inf"))
        return best_move
    elif level == 2:
        # Use minimax algorithm with enhanced evaluation and slight randomness
        _, best_move = minimax(board, 0, True, float("-inf"), float("inf"))
        if random.random() > 0.1:
            return best_move
        else:
            # Introduce slight randomness by choosing from top-scoring moves
            top_moves = []
            max_score = float("-inf")
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        score, _ = minimax(board, 0, False, float("-inf"), float("inf"))
                        board[row][col] = " "
                        if score > max_score:
                            max_score = score
                            top_moves = [(row, col)]
                        elif score == max_score:
                            top_moves.append((row, col))
            return random.choice(top_moves)

# Function to draw a button
def draw_button(text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))

# Main function to run the game
def main():
    board = [[" "]*3 for _ in range(3)]
    game_over = False
    mode = 0
    level = 0

    # Button rectangles
    button_width = 200
    button_height = 40
    mode_button1 = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - 60, button_width, button_height)
    mode_button2 = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2, button_width, button_height)
    level_button1 = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - 60, button_width, button_height)
    level_button2 = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 - 20, button_width, button_height)
    level_button3 = pygame.Rect((WIDTH - button_width) // 2, HEIGHT // 2 + 20, button_width, button_height)

    player = "X"

    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 0:
                    if mode_button1.collidepoint(event.pos):
                        mode = 1
                    elif mode_button2.collidepoint(event.pos):
                        mode = 2
                elif mode == 1 and level == 0:
                    if level_button1.collidepoint(event.pos):
                        level = 1
                    elif level_button2.collidepoint(event.pos):
                        level = 2
                    elif level_button3.collidepoint(event.pos):
                        level = 3
                elif mode == 2 or (mode == 1 and level != 0):
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE
                    if is_valid_move(board, mouseY, mouseX):
                        board[mouseY][mouseX] = player
                        if check_winner(board, player):
                            game_over = True
                        elif is_board_full(board):
                            game_over = True
                        else:
                            player = "O" if player == "X" else "X"

        isFinish = False
        if mode == 0:
            draw_button("Play vs AI", mode_button1, LINE_COLOR, WHITE)
            draw_button("Play vs Friend", mode_button2, LINE_COLOR, WHITE)
        elif mode == 1 and level == 0:
            draw_button("Easy", level_button1, LINE_COLOR, WHITE)
            draw_button("Medium", level_button2, LINE_COLOR, WHITE)
            draw_button("Hard", level_button3, LINE_COLOR, WHITE)
        elif mode == 2 or (mode == 1 and level != 0):
            screen.fill(WHITE)
            draw_grid()
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "X":
                        draw_x(row, col)
                    elif board[row][col] == "O":
                        draw_o(row, col)

            if player == "O" and not game_over and mode == 1:
                ai_row, ai_col = ai_move(board, level)
                board[ai_row][ai_col] = "O"
                draw_o(ai_row, ai_col)
                if check_winner(board, "O"):
                    game_over = True
                elif is_board_full(board):
                    game_over = True
                else:
                    player = "X"

            if check_winner(board, "X"):
                isFinish = True
                print("Player X Wins!")
                text = font.render("Player X Wins!", True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            elif check_winner(board, "O"):
                isFinish = True
                print("Player O Wins!")
                text = font.render("Player O Wins!", True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            elif is_board_full(board):
                isFinish = True
                print("It's a draw!")
                text = font.render("It's a draw!", True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
        
        if isFinish:
            sleep(3)
            break

    return main()

if __name__ == "__main__":
    main()
