import numpy as np
import pygame
import sys
import math
import random
# pylint: disable=no-member

# * Global Constant Variables * #
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

ROW_COUNT = 6
COL_COUNT = 7

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
WIDTH = COL_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

WINDOW_LENGTH = 4


# * Function Definitions * #
def create_board():
    """
    This function loads an array of zeros with the demensions of ROW_COUNT x COL_COUNT
    """
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board


def drop_piece(board, row, col, piece):
    """
    This function places a players piece into the board array.
    """
    board[row][col] = piece


def is_valid_location(board, col):
    """
    This function returns True if the column is NOT full, False if it is full.
    """
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    """
    This function returns the next available row in the given column.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    """
    This function prints the board to the command line.
    """
    print(np.flip(board, 0))


def winning_move(board, piece):
    """
    This function checks to see if the player has won.
    """
    # TODO: Make the algorithm for checking who has won more efficient.
    # Check all horizontal locations for win
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    """
    Evaluates the score of next possible move 
    """
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    
    return score

def score_positions(board, piece):
    """
    Evaluates the score for multiple positions
    """
    score = 0

    # Score Center
    centerArray = [int(i) for i in list(board[:, COL_COUNT//2])]
    centerCount = centerArray.count(piece)
    score += centerCount * 6

    # Score Horizontal #
    for r in range(ROW_COUNT):
        rowArray = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = rowArray[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    #  Score Vertical #
    for c in range(COL_COUNT):
        colArray = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = colArray[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):
    """
    Returns all possible columns that can be played.
    """
    validLocations = []
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            validLocations.append(col)
    return validLocations

def pick_best_move(board, piece):
    """
    Picks the best move possible
    """
    validLocations = get_valid_locations(board)
    bestScore = -10000
    bestCol = random.choice(validLocations)
    for col in validLocations:
        row = get_next_open_row(board, col)
        tempBoard = board.copy()
        drop_piece(tempBoard, row, col, piece)
        score = score_positions(tempBoard, piece)
        if score > bestScore:
            bestScore = score
            bestCol = col

    return bestCol
        


def draw_board(board):
    """
    This function draws the board to the screen.
    """
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r * SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT-int(r * SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT-int(r * SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


if __name__ == "__main__":
    # * Initialize Game * #
    board = create_board()
    print_board(board)
    gameOver = False
    turn = random.randint(PLAYER, AI)

    # * Initialize Graphics * #
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    draw_board(board)
    pygame.display.update()
    myFont = pygame.font.SysFont("monospace", 75)

    # * Game Loop * #
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Draw floating piece
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                posX = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            # Place down piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                # Ask for player 1 input
                if turn == PLAYER:
                    posX = event.pos[0]
                    col = int(math.floor(posX/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myFont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            gameOver = True

                        turn = (turn + 1) % 2
                        print_board(board)
                        draw_board(board)

        # AI turn
        if turn == AI and not gameOver:
            # col = random.randint(0, COL_COUNT-1)
            col = pick_best_move(board, AI_PIECE)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myFont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    print_board(board)
                    gameOver = True

                print_board(board)
                draw_board(board)

            turn = (turn + 1) % 2

        if gameOver:
            pygame.time.wait(3000)