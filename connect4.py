import numpy as np
import pygame
import sys
import math
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
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT-int(r * SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), HEIGHT-int(r * SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


if __name__ == "__main__":
    # * Initialize Game * #
    board = create_board()
    print_board(board)
    gameOver = False
    turn = 0

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
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posX, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            # Place down piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARESIZE))
                # Ask for player 1 input
                if turn == 0:
                    posX = event.pos[0]
                    col = int(math.floor(posX/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myFont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            gameOver = True

                # ask for player 2 input
                else:
                    posX = event.pos[0]
                    col = int(math.floor(posX/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myFont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            gameOver = True

                print_board(board)
                draw_board(board)

                turn = (turn + 1) % 2

                if gameOver:
                    pygame.time.wait(3000)