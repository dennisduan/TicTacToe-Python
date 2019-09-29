import tkinter as tk
from tkinter import messagebox
import random
from functools import partial
import copy
import time
    
def btn1_click(event, x, y):
    if ttt[x][y] == 0:    # allowed
        drawX(x, y)
        winner = check_result(ttt)
        if winner != 0:
            show_winner(winner)
            exit(0)

        AI_battle()
        winner = check_result(ttt)
        if winner != 0:
            show_winner(winner)

def AI_battle():
    # Choose a cell to place 'O'
    # record the move
    empty_corners = []
    empty_others = []

    # scan the table
    for i in range(3):
        for j in range(3):
            if ttt[i][j] == 0 and ((i,j) in ((0,0), (0,2), (2,0), (2,2))):
                empty_corners.append((i,j))
            elif ttt[i][j] == 0:
                empty_others.append((i,j))

    if len(empty_corners) == 0 and len(empty_others) == 0:
        return

    # Check if there's cell "win" this game
    for (x,y) in empty_corners + empty_others:
        temp_ttt = copy.deepcopy(ttt)
        temp_ttt[x][y] = 2
        winner = check_result(temp_ttt)
        if winner == 2: # computer win
            drawO(x, y)

    # No cell can win the game at this moment
    if ttt[1][1] == 0:
        drawO(1, 1)
    elif len(empty_corners) > 0:
        p = empty_corners[random.randint(0,len(empty_corners)-1)]
        drawO(p[0], p[1])
    elif len(empty_others) > 0:
        p = empty_others[random.randint(0,len(empty_others)-1)]
        drawO(p[0], p[1])
    else:
        tk.messagebox.showinfo("Game", "Draw!!")
        exit(0)

def drawX(x, y):
    canvas = canvases[x*3+y]
    canvas.create_line(10, 10, 40, 40)
    canvas.create_line(40, 10, 10, 40)
    ttt[x][y] = 1

def drawO(x, y):
    canvas = canvases[x*3+y]
    canvas.create_oval(10, 10, 40, 40)
    ttt[x][y] = 2

def check_result(grid):
    winner = 0;
    # Check cross
    if grid[0][0] == grid[1][1] == grid[2][2]:
        winner = grid[0][0]
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2]:
            winner = grid[i][0]
        if grid[0][i] == grid[1][i] == grid[2][i]:
            winner = grid[0][i]

    return winner

def show_winner(winner):
    if winner == 1:
        tk.messagebox.showinfo("Game", "YOU WIN!!!")
    else:
        tk.messagebox.showinfo("Game", "YOU LOSE!!!")

root = tk.Tk()
# width x height + x_offset + y_offset:
root.geometry("200x200+40+40")

canvases = []
ttt = [[0,0,0],[0,0,0],[0,0,0]]     # record Tic-Tac-Toe grid

for i in range(3):
    for j in range(3):
        canvas = tk.Canvas(root, height = 50, width = 50, relief=tk.RAISED)
        canvas.grid(row=i, column=j)
        canvas.create_rectangle(3,3,50,50)
        canvas.bind('<Button-1>', partial(btn1_click, x=i, y=j))
        canvases.append(canvas)

root.mainloop()
