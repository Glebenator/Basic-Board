from consts import *
import pygame
import os

b_pawn = pygame.image.load(os.path.join("Sprites","Chess_pdt60.png"))
b_rook = pygame.image.load(os.path.join("Sprites","Chess_rdt60.png"))
b_bishop = pygame.image.load(os.path.join("Sprites","Chess_bdt60.png"))
b_knight = pygame.image.load(os.path.join("Sprites","Chess_ndt60.png"))
b_king = pygame.image.load(os.path.join("Sprites","Chess_kdt60.png"))
b_queen = pygame.image.load(os.path.join("Sprites","Chess_qdt60.png"))
w_pawn = pygame.image.load(os.path.join("Sprites","Chess_plt60.png"))
w_rook = pygame.image.load(os.path.join("Sprites","Chess_rlt60.png"))
w_bishop = pygame.image.load(os.path.join("Sprites","Chess_blt60.png"))
w_knight = pygame.image.load(os.path.join("Sprites","Chess_nlt60.png"))
w_king = pygame.image.load(os.path.join("Sprites","Chess_klt60.png"))
w_queen = pygame.image.load(os.path.join("Sprites","Chess_qlt60.png"))

b = [b_pawn, b_rook, b_bishop, b_knight, b_king, b_queen]
w = [w_pawn, w_rook, w_bishop, w_knight, w_king, w_queen]
B = []
W = []
scaleFactor = WIDTH//SIZE
for img in b:
    B.append(pygame.transform.scale(img,(scaleFactor,scaleFactor)))
for img in w:
    W.append(pygame.transform.scale(img,(scaleFactor, scaleFactor)))

class piece:
    img = -1
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.selected = False
        self.squares = []
        self.drag = False
    def move(self):
        pass
    def isSelected(self):
        return self.selected
    def draw_moves(self, win, row, col):
        for move in self.squares:
             #print(move)
             newRow = move // SIZE
             newCol = move % SIZE
             newRect = pygame.Rect(newCol * SQSIZE, newRow * SQSIZE, SQSIZE, SQSIZE)
             pygame.draw.circle(win, pygame.Color('black'), newRect.center, 15)
    def draw_piece(self, win, row, col):
        if self.color == "w":
            drawThis = w[self.img]
        else:
            drawThis = b[self.img]
        img_center = col * SQSIZE + SQSIZE //2 , row * SQSIZE + SQSIZE //2
        win.blit(drawThis, drawThis.get_rect(center=img_center))
        #print(self.drag)
    def draw(self, win, Imcenter=None):
        row = self.pos // SIZE
        col = self.pos % SIZE
        if self.isSelected():

            pygame.draw.rect(win, pygame.Color('black'), (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE), 2)
            self.draw_moves(win, row, col)

            if self.drag == True:
                if self.color == "w":
                    drawThis = b[self.img]
                else:
                    drawThis = w[self.img]
                if Imcenter != None:
                    #win.blit(drawThis, drawThis.get_rect(center=Imcenter))
                    #pygame.draw.circle(win, pygame.Color('Green'), newRect.center, 10)
                    self.draw_piece(win,row,col)
            else:
                self.draw_piece(win, row, col)
        else:
            self.draw_piece(win, row, col)
    @staticmethod
    def CheckRCEdge(*args):
        for arg in args:
            if arg < 0 or arg > SIZE-1:
                return False
        return True
    def CheckEdgeV2(self,x,dir):
        if (dir == 8):#if we are going straight down, edges are [56-63]
            if (56 <= x <= 63):
                return True
        elif(dir == -8):
            if (0 <= x <= 7):
                return True
        elif(dir == -1):
            if x in range (0,64,8):
                return True
        elif (dir == 1):
            if x in range (7, 71, 8):
                return True
        elif (dir == 9):
            if x in range (56, 64):
                return True
            if x in range (7, 71, 8):
                return True
        elif (dir == -9):
            if x in range (0, 64, 8):
                return True
            if x in range (0,8):
                return True
        elif (dir == 7):
            if x in range (0, 64, 8):
                return True
            if x in range (56, 64):
                return True
        elif (dir == -7):
            if x in range(0, 8):
                return True
            if x in range(7, 71, 8):
                return True
    def slide(self, board, dir):
        if(self.CheckEdgeV2(self.pos, dir)):
            return
        if (dir > 0):
            for x in range (self.pos + dir, len(board), dir):
                if board[x] == None:
                    self.squares.append(x)
                    if self.CheckEdgeV2(x, dir):
                        break
                else:
                    if board[x].color == self.color:
                        break
                    else:
                        self.squares.append(x)
                        break
        else:
            for x in range (self.pos + dir, 0+dir, dir):
                if board[x] == None:
                    self.squares.append(x)
                    if self.CheckEdgeV2(x, dir):
                        break
                else:
                    if board[x].color == self.color:
                        break
                    else:
                        self.squares.append(x)
                        break
            
class Pawn(piece):
    img = 0
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.first = True
        self.queen = False
    def generate_legal_squares(self,board):
        self.squares.clear()
        pos = self.pos
        b = board
        index = SIZE
        if self.color == "b":
            index = SIZE * -1
        if self.first:
            #if this is a first pawn moves, legal squares are 1 or 2 squares ahead, unless there is a piece in front.
            if board[pos+index] == None:
                self.squares.append(pos+index)
                if board[pos + (2*index)] == None:
                    self.squares.append(pos + (2*index))
            if board[pos+index-1] != None:
                if self.CheckEdgeV2(pos, index-1):
                    return
                if self.color != board[pos+index-1].color:
                    self.squares.append(pos+index-1)
            if board[pos+index+1] != None:
                if self.CheckEdgeV2(pos, index+1):
                    return
                if self.color != board[pos+index+1].color:
                    self.squares.append(pos+index+1)
        else:
            if board[pos+index] == None:
                self.squares.append(pos + index)
            if board[pos+index+1] != None:
                if self.CheckEdgeV2(pos, index+1):
                    return
                if self.color != board[pos+index+1].color:
                    self.squares.append(pos+index+1)
            if board[pos+index-1] != None:
                if self.CheckEdgeV2(pos, index-1):
                    return
                if self.color != board[pos+index-1].color:
                    self.squares.append(pos+index-1)
        return self.squares
class Rook(piece):
    img = 1
    def generate_legal_squares(self,board):
        self.squares.clear()
        self.slide(board, SIZE)
        self.slide(board, (SIZE * -1))
        self.slide(board, 1)
        self.slide(board, (-1))
class Bishop(piece):
    img = 2
    def generate_legal_squares(self,board):
        self.squares.clear()
        self.slide(board, SIZE + 1)
        self.slide(board, SIZE - 1)
        self.slide(board, (SIZE * -1) + 1)
        self.slide(board, (SIZE * -1) - 1 )
class Knight(piece):
    img = 3
    def generate_legal_squares(self,board):
        self.squares.clear()
        row = self.pos // SIZE
        col = self.pos % SIZE
        possible_moves = [(row-2, col+1), (row-1, col+2), (row+1, col+2), (row+2, col+1), (row+2, col-1), (row+1, col-2), (row-1, col-2), (row-2, col-1)]
        for move in possible_moves:
            move_row, move_col = move
            if piece.CheckRCEdge(move_row, move_col):
                board_pos = move_row * SIZE + move_col
                if board[board_pos] == None:
                    self.squares.append(board_pos)
                if board[board_pos] != None:
                    if board[board_pos].color != self.color:
                        self.squares.append(board_pos)
    
class King(piece):
    img = 4
    def generate_legal_squares(self, board):
        self.squares.clear()
        row = self.pos // SIZE
        col = self.pos % SIZE
        possible_moves = [(row+1, col+1), (row+1, col), (row+1, col-1), (row, col+1), (row, col-1), (row-1, col+1), (row-1, col), (row-1, col-1)]
        for move in possible_moves:
            move_row, move_col = move
            if piece.CheckRCEdge(move_row, move_col):
                board_pos = move_row * SIZE + move_col
                if board[board_pos] == None:
                    self.squares.append(board_pos)
                if board[board_pos] != None:
                    if board[board_pos].color != self.color:
                        self.squares.append(board_pos)
class Queen(piece):
    img = 5
    def generate_legal_squares(self,board):
        self.squares.clear()
        self.slide(board, SIZE + 1)
        self.slide(board, SIZE - 1)
        self.slide(board, (SIZE * -1) + 1)
        self.slide(board, (SIZE * -1) - 1 )
        self.slide(board, SIZE)
        self.slide(board, (SIZE * -1))
        self.slide(board, 1)
        self.slide(board, (-1))