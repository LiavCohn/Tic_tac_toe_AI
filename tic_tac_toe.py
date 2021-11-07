import pygame
from pygame.draw import rect
#import sys
#import math
pygame.init()
pygame.font.init()
images = []
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
ROWS = 3
WIDTH = 450
HEIGHT = 480
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 150
#CIRCLE_RADIUS = 60
#CIRCLE_WIDTH = 15
#CROSS_WIDTH = 25
#SPACE = 55
TURNS_FONT= pygame.font.SysFont('comicsans', 15)

BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x_img.png"), (100, 100))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o_img.png"), (100, 100))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)
PLAYER = 'O'
AI = 'X'

scores = {'X':1, 'O':-1, 'tie':0}
current_player = PLAYER
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("tic tac toe")

board = [[None, None, None], [None, None, None], [None, None, None]]

def draw_lines():	
    
	pygame.draw.line(WIN, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)	
	pygame.draw.line(WIN, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
	pygame.draw.line(WIN, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
	pygame.draw.line(WIN, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def get_clicked_pos(pos,rows,width):
    #global images

    gap = width//rows
    y,x = pos

    col = y//gap
    row = x//gap

    #locate where to put the image, based on the position of the mouse
    x,y,char,full = board[row][col]
    
    if full:
        return
    else:
        images.append((x,y,O_IMAGE))
        board[row][col] = (x,y,PLAYER,True)

def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the board

    for i in range(len(board)):
        for j in range(len(board[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding center coordinates
            #center x,center y, AI/player,is taken
            board[i][j] = (x, y, "", False)

def render():
        
    WIN.fill(WHITE)
    draw_lines()
    for image in images:
        x,y,img = image
        WIN.blit(img, (x-img.get_width()//2,y-img.get_height()//2))

    display_msg(current_player)
    pygame.display.update()

def minimax(depth, isMaximizing):
    result  = check_winner()
    if result is not None:
        score = scores[result]
        return score

    if isMaximizing:
        best_score = -1000
        for row in range(ROWS):
            for col in range(ROWS):
                if board[row][col][3] ==False:
                    l = list(board[row][col])
                    l[2] = AI
                    l[3] = True
                    board[row][col] = tuple(l)
                    score = minimax(depth+1,False)
                    l[2] = ""
                    l[3] = False
                    board[row][col] = tuple(l)
                    best_score = max(best_score,score)
        return best_score

    else:
        best_score = 1000  
        for row in range(ROWS):
            for col in range(ROWS):
                if board[row][col][3] == False:
                    l = list(board[row][col])
                    l[2] = PLAYER
                    l[3] = True
                    board[row][col] = tuple(l)
                    score = minimax(depth+1,True)
                    l[2] = ""
                    l[3] = False
                    board[row][col] = tuple(l)
                    best_score = min(best_score,score)
        return best_score
    

def best_move():
    best_score = -1000
    move = None
    global board
    for row in range(ROWS):
        for col in range(ROWS):
            if board[row][col][3] == False:
                l = list(board[row][col])
                l[2] = AI
                l[3] = True
                board[row][col] = tuple(l)
                score = minimax(0,False)
                l[2] = ""
                l[3] = False
                board[row][col] = tuple(l)
                if score > best_score:
                    best_score = score
                    move = row,col

    row , col = move #deconstruct
    x,y,char,full = board[row][col]
    images.append((x,y,X_IMAGE))
    board[row][col] = (x,y,AI,True)
    

def check_winner():
    winner = None

    #check all the rows
    for row in board:
        if row[0][2]==row[1][2]==row[2][2] and row[0][2]!="":
            winner = row[0][2]
            #print(winner)
            

    #check all the columns
    for column in zip(*board):
        if column[0][2]==column[1][2]==column[2][2] and column[0][2]!="":
            winner = column[0][2]
            #print(winner)
            

    #check main diagonal
    if board[0][0][2] == board[1][1][2] == board[2][2][2] and board[0][0][2]!="":
        winner = board[0][0][2]
        #print(winner)
        

    #check other diagonal
    if board[0][2][2] == board[1][1][2] == board[2][0][2] and board[0][2][2]!="":
        winner = board[0][2][2]
        #print(winner)
        

    if winner is None and is_draw():
        return "tie"
    else : return winner

def display_msg(content):

    pygame.draw.rect(WIN, BLACK, (0, HEIGHT-50, WIDTH, 20))
    turns_text= TURNS_FONT.render(content +"'s Turns", 1,WHITE,BLACK)
    WIN.blit(turns_text, (WIDTH//2-30 , HEIGHT-turns_text.get_height()-35))
    pygame.display.update()
    
def print_draw():
    pygame.draw.rect(WIN, BLACK, (0, HEIGHT-50, WIDTH, 20))
    turns_text= TURNS_FONT.render("It's a draw!", 1,WHITE,BLACK)
    WIN.blit(turns_text, (WIDTH//2-30 , HEIGHT-turns_text.get_height()-35))
    pygame.display.update()

def print_winner(winner):
    
    pygame.draw.rect(WIN, BLACK, (0, HEIGHT-50, WIDTH, 20))
    turns_text= TURNS_FONT.render(winner+"'s the winner!", 1,WHITE,BLACK)
    WIN.blit(turns_text, (WIDTH//2-30 , HEIGHT-turns_text.get_height()-35))
    pygame.display.update()

def is_draw():
    for i in range(ROWS):
        for j in range(ROWS):
            if board[i][j][2] == "":
                return False


    return True

def main():

    global current_player
    run = True

    initialize_grid()
    while run:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] and current_player==PLAYER: #left mouse button
                pos = pygame.mouse.get_pos()
                get_clicked_pos(pos,ROWS,WIDTH)
                current_player = AI
                

            elif current_player == AI:
                best_move()
                pygame.time.delay(500)               
                current_player = PLAYER
                

        render()
        res = check_winner()
        if res is not None:
            if(res == "tie"):
                print_draw()
                pygame.time.delay(1500)
                run = False
            else: 
                print_winner(res)
                pygame.time.delay(1500)
                run = False
            
    pygame.quit()
main()