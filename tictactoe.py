import pygame, random, os,time

pygame.mixer.init()
pygame.font.init()
pygame.init()

MUSIC = pygame.mixer.Sound('Assets/tictactoemusic.mp3')

WIDTH, HEIGHT = 900, 900
BOARD_SIZE = 700
BOARD_POS = ((WIDTH - BOARD_SIZE) // 2, (HEIGHT - BOARD_SIZE) // 2)
CELL_SIZE = BOARD_SIZE // 3

FONT = pygame.font.SysFont('comicsans', 60)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

BOARD = pygame.image.load(os.path.join('Assets', 'Board.png'))
BOARD = pygame.transform.smoothscale(BOARD, (BOARD_SIZE, BOARD_SIZE))

X_IMG = pygame.image.load(os.path.join('Assets', 'X.png'))
X_IMG = pygame.transform.smoothscale(X_IMG, (150, 150))

O_IMG = pygame.image.load(os.path.join('Assets', 'O.png'))
O_IMG = pygame.transform.smoothscale(O_IMG, (150, 150))

BG_COLOR = (214, 211, 227)

board = [[1 + 3 * i + j for j in range(3)] for i in range(3)]
graphicalBoard = [[[None, None] for _ in range(3)] for _ in range(3)]
toMove = 'X'
gameFinished = False

def render_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] in ('X', 'O'):
                img = X_IMG if board[i][j] == 'X' else O_IMG
                center_x = BOARD_POS[0] + j * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_POS[1] + i * CELL_SIZE + CELL_SIZE // 2
                rect = img.get_rect(center=(center_x, center_y))
                
                offset_x = 10  
                offset_y = 0
                rect.center = (center_x + offset_x, center_y + offset_y)
                
                graphicalBoard[i][j] = [img, rect]
                SCREEN.blit(img, rect)

def show_winning_line(cells, winner):
    for r, c in cells:
        img = pygame.image.load(f"Assets/Winning {winner}.png")
        img = pygame.transform.smoothscale(img, (170,170))
        rect = graphicalBoard[r][c][1]
        
        offset_x = -11
        offset_y = -15
        if winner == 'O':
            offset_x = -11  
            offset_y = -10   
        
        rect.center = (rect.centerx + offset_x, rect.centery + offset_y)
        SCREEN.blit(img, rect)
    pygame.display.update()
    time.sleep(0.5)
    SCREEN.fill(BG_COLOR)
    whoWon = f'{winner} has won this game!'
    draw_text = FONT.render(whoWon, 1, (0, 0, 0))
    SCREEN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()

def add_move():
    global toMove
    x, y = pygame.mouse.get_pos()

    if (BOARD_POS[0] <= x <= BOARD_POS[0] + BOARD_SIZE) and (BOARD_POS[1] <= y <= BOARD_POS[1] + BOARD_SIZE):
        col = (x - BOARD_POS[0]) // CELL_SIZE
        row = (y - BOARD_POS[1]) // CELL_SIZE
        row, col = int(row), int(col)

        if board[row][col] not in ('X', 'O'):
            board[row][col] = toMove
            toMove = 'O'
            render_board()

def computer_move():
    global toMove
    if toMove != 'O':
        return
    emptyCells = [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ('X', 'O')]
    if emptyCells:
        i, j = random.choice(emptyCells)
        board[i][j] = 'O'
        toMove = 'X'
        render_board()


def check_win():
    lines = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for line in lines:
        symbols = [board[r][c] for r, c in line]
        if symbols[0] == symbols[1] == symbols[2] and symbols[0] in ('X', 'O'):
            show_winning_line(line, symbols[0])
            return symbols[0]

    if all(cell in ('X', 'O') for row in board for cell in row):
        return "DRAW"

    return None

def reset_game():
    global board, graphicalBoard, toMove, gameFinished
    board = [[1 + 3 * i + j for j in range(3)] for i in range(3)]
    graphicalBoard = [[[None, None] for _ in range(3)] for _ in range(3)]
    toMove = 'X'
    gameFinished = False
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, BOARD_POS)
    time.sleep(0.5)
    render_board()
    pygame.display.update()

# Initial screen setup
SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, BOARD_POS)
pygame.display.update()


while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not gameFinished:
                    if toMove == 'X':
                        add_move()
                        result = check_win()
                        pygame.display.update()

                        if result:
                            gameFinished = True
                        else:
                            pygame.time.delay(300)  # slight pause for realism
                            computer_move()
                            result = check_win()
                            if result:
                                gameFinished = True
                            pygame.display.update()
                else:
                    reset_game()
            if not pygame.mixer.get_busy():
                MUSIC.play()
