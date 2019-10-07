import math

# global variables
huPlayer = 'x'
aiPlayer = 'o'

change_player = {huPlayer:aiPlayer, aiPlayer:huPlayer}

def check_finish(board):
    # if there's no room for new move, game is end
    global huPlayer, aiPlayer

    hu_count = 0
    ai_count = 0

    for i in len(board):
        for j in len(board[0]):
            item = board[i][j]
            if not item in [huPlayer, aiPlayer]:
                return {huPlayer:-1, aiPlayer:-1}          # game not end
            else:
                if item == huPlayer:
                    hu_count += 1
                else:
                    ai_count += 1
    
    return {huPlayer:hu_count, aiPlayer:ai_count}


def print_board(board):
    head = ' '
    for i in range(len(board)):
        head += (str(i) + ' ')
    print(head)

    for i in range(len(board)):
        line = '|'
        for j in range(len(board[0])):
            line += (board[i][j] + ' ')
        line += '|'
        print(line)
    print('----Board end----')


def place_piece(board, player, pos_x, pos_y):
    global huPlayer, aiPlayer

    if pos_x >= len(board) or pos_y >= len(board[0]):
        print('You cannot place piece out of board...')
        return

    if board[pos_x][pos_y] in [huPlayer, aiPlayer]:
        print('There is already another piece...')
        return 

    board[pos_x][pos_y] = player
    # reverse corresponding pieces 
    reverse_pieces(board, player, pos_x, pos_y)


def is_on_board(board, x, y):
    if x < 0 or x >= len(board):
        return False

    if y < 0 or y >= len(board[0]):
        return False

    return True


def reverse_pieces(board, player, pos_x, pos_y):

    global change_player
    
    start_x = pos_x
    start_y = pos_y
    
    for xdirection, ydirection in ([0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]):
        x = start_x
        y = start_y

        x += xdirection
        y += ydirection

        to_be_changed = []
        while is_on_board(board, x, y) and board[x][y] == change_player[player]:
            to_be_changed.append((x,y))
            x += xdirection
            y += ydirection
        
        if is_on_board(board, x, y):
            for pos in to_be_changed:
                board[pos[0]][pos[1]] = player


if __name__ == '__main__':
    board = [['-','o','x','o'],['o','o','o','-'],['o','o','o','o'],['x','-','-','x']]
    print('Orignal board:')
    print_board(board)
    place_piece(board, 'x', 0, 0)
    print('After move:')
    print_board(board)
    
