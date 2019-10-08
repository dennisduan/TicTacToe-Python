#encoding:utf8
'''
MiniMax algorithm for TicTacToe game
'''

class Node:
    def __init__(self, board, children, score, flag, depth):
        self.board = board
        self.children = children        # Collection of children nodes
        self.score = score              # value
        self.flag = flag                # flag: 'x' or 'o'
        self.depth = depth              # depth of the node (from 0)


    def print_board(self):
        for i in range(3):
            line = ''
            for j in range(3):
                if self.board[3*i+j] == '':
                    line += '-'
                else:
                    line += self.board[3*i+j]
            print(line)


    def print_all(self):
        self.print_board()
        print(self.children)
        print("Score: " + str(self.score))
        print("Flag: " + str(self.flag))
        print("Depth: " + str(self.depth))

def check_finish(board):
    win_pattern = ([0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6])
    full_flag = True
    # Check if the board is full
    for i in range(3):
        for j in range(3):
            if board[3*i+j] != 'x' and board[3*i+j] != 'o':
                full_flag = False

    for pattern in win_pattern:
        check = ''
        for i in pattern:
            check += board[i]
        if check == 3*'x':
            return 'x'
        elif check == 3*'o':
            return 'o'
        
    if full_flag:
        return 'd'      # Means 'Draw'
    else:
        return 'n'      # Means 'Not Full'


def get_available_pos(board):
    moves = []
    for i in range(3*3):
        if board[i] == '':
            moves.append(i)
    
    return moves


def get_score(board, player):
    # Use regression to get all possible move
    result = check_finish(board)
    
    if result == 'd':
        return -1,0

    elif result == 'x':         # Assure 'x' will always be the player with first move
        return -1,-10

    elif result == 'o':
        return -1,10

    elif result == 'n':
        # Get all available positions
        available_pos = get_available_pos(board)

        moves = {}
    
        for m in available_pos:
            new_board = board[:]
            new_board[m] = player

            if player == aiPlayer:
                _, score = get_score(new_board, huPlayer)
                moves[m] = score
            else:
                _, score = get_score(new_board, aiPlayer)
                moves[m] = score

            new_board[m] = ''       # reset board

        # Find the best move
        bestScore = -100
        bestMove = -100
        if player == aiPlayer:
            bestScore = -1000
            for k in moves.keys():
                if moves[k] > bestScore:
                    bestMove = k
                    bestScore = moves[bestMove]
            return bestMove, bestScore

        else:
            bestScore = 1000
            for k in moves.keys():
                if moves[k] < bestScore:
                    bestMove = k
                    bestScore = moves[bestMove]
            return bestMove, bestScore

# global counter
huPlayer = 'x'
aiPlayer = 'o'

def print_board(board):
    for i in range(3):
        line = ''
        for j in range(3):
            if board[3*i+j] == '':
                line += '-'
            else:
                line += board[3*i+j]
        print(line)
                

if __name__ == '__main__':
    board = ['','','','','','','','','']
    while True:
        bestMove, score = get_score(board, aiPlayer)
        board[bestMove] = aiPlayer
        print('AI moved...')
        print_board(board)

        winner = check_finish(board)
        if winner == aiPlayer:
            print('AI win this game!')
            exit(0)
        elif winner == 'd':
            print('Draw!')
            exit(0)

        while True:
            huPlayer_pos = int(input("It's your turn:"))
            if board[huPlayer_pos] != '':
                print('This position you input is invalid, please retry...')
                continue
            else:
                board[huPlayer_pos] = huPlayer
                print('User moved...')
                print_board(board)
                break
        
        check_finish(board)
        winner = check_finish(board)
        if winner == huPlayer:
            print('You win!')
            exit(0)
