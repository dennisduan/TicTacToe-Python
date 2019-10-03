import tkinter as tk
from tkinter import messagebox
import random
import copy
import _thread
import threading

import minimax


def get_screen_size(window):
    return window.winfo_screenwidth(),window.winfo_screenheight()
 
def get_window_size(window):
    return window.winfo_reqwidth(),window.winfo_reqheight()
 
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)

def drawX(x, y, color='black'):
    canvas.create_line(x*50+10, y*50+10, x*50+40, y*50+40, fill=color)
    canvas.create_line(x*50+10, y*50+40, x*50+40, y*50+10, fill=color)
    canvas.pack()
    ttt[x][y] = 'x'

def drawO(x, y, color='black'):
    canvas.create_oval(x*50+10, y*50+10, x*50+40, y*50+40, fill=color)
    canvas.pack()
    ttt[x][y] = 'o'

def gameover_thread(event):
    global canvas, win_pattern, game_winner
    global gameover_flag
    event.wait()

    highlight_winner_pattern(canvas, win_pattern, game_winner)
    if game_winner == 'x':
        root.title('you WIN')
    elif game_winner == 'o':
        root.title('you LOSE')
    elif game_winner == 'd':
        root.title('Draw')
    else:
        root.title('Something went wrong...')

    gameover_flag = True


def btn1_click(event):
    global gameover_flag, ttt, game_winner, gameover_event
    if gameover_flag:    # Game over
        return

    # Calculate "row" and "column" according to x and y
    row = event.x // 50 
    col = event.y // 50

    if ttt[row][col] == '':    # allowed
        drawX(row, col)
        winner = check_result(ttt)
        if winner != '':
            game_winner = winner
            gameover_event.set()
            gameover_event.clear()
        else:
            AI_battle()
            winner = check_result(ttt)
        if winner != '':
            game_winner = winner
            gameover_event.set()
            gameover_event.clear()

def AI_battle():
    global ttt, game_winner
    # Choose a cell to place 'O'
    # record the move
    available_pos = []

    # scan the table
    for i in range(3):
        for j in range(3):
            if ttt[i][j] == '':
                available_pos.append((i,j))

    if len(available_pos) == 0:      # Draw
        game_winner = 'd'
        return

    # Change ttt to 1-demension array
    board = []
    for i in range(3):
        for j in range(3):
            board.append(ttt[i][j])

    best_move, _ = minimax.get_score(board, 'o')
    print(best_move)

    drawO(best_move//3, best_move%3)


def check_result(grid):
    global win_pattern
    winner = ''

    # Check cross
    if grid[0][0] == grid[1][1] == grid[2][2]:
        winner = grid[0][0]
        win_pattern = ((0,0), (1,1), (2,2))
    elif grid[2][0] == grid[1][1] == grid[0][2]:
        winner = grid[2][0]
        win_pattern = ((2,0), (1,1), (0,2))
    
    # Check row / column
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2]:
            winner = grid[i][0]
            win_pattern = ((i,0), (i,1), (i,2))
        if grid[0][i] == grid[1][i] == grid[2][i]:
            winner = grid[0][i]
            win_pattern = ((0,i), (1,i), (2,i))

    # Check if Draw
    None

    return winner

def highlight_winner_pattern(canvas, win_pattern, winner):
    for item in win_pattern:
        if winner == 'x':
            drawX(item[0], item[1], color='red')
        elif winner == 'o':
            drawO(item[0], item[1], color='red')


root = tk.Tk()
# width x height + x_offset + y_offset:
center_window(root, 150, 150)
root.maxsize(150, 150)
root.minsize(150, 150)

ttt = [['']*3,['']*3,['']*3]     # record Tic-Tac-Toe grid
gameover_event = threading.Event()
gameover_flag = False
win_pattern = []
game_winner = ''

_thread.start_new_thread(gameover_thread, (gameover_event,))

# Draw Map
canvas = tk.Canvas(root, height=150, width=150)
canvas.create_line(0, 50, 150, 50)
canvas.create_line(0, 100, 150, 100)
canvas.create_line(50, 0, 50, 150)
canvas.create_line(100, 0, 100, 150)

canvas.pack()
canvas.bind('<Button-1>', btn1_click)

root.mainloop()
