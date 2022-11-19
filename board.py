import pygame
from piece import Bishop
from piece import King
from piece import Knight
from piece import Pawn
from piece import Queen
from piece import Rook
from consts import *
class Board:
    def __init__(self):
        self.board = ((SIZE * SIZE))*[None]

        #self.board.insert(0,Rook("b", 0, self.width, self.size))
        #self.board.insert(7,Rook("b", 7, self.width, self.size))
    
    def LoadPosFromFen(self, fen):
        file = 0
        rank = SIZE - 1
        PieceDict = {
            'p': Pawn,
            'k': King,
            'n': Knight,
            'b': Bishop,
            'q': Queen,
            'r': Rook
        }
        for char in fen:
            if char == '/':
                file = 0
                rank = rank - 1
            else:
                if char.isnumeric():
                    file = file + int(char)
                else:
                    if char.isupper():
                        color = "w"
                    else:
                        color = "b"
                    pieceType = PieceDict[char.lower()]
                    self.board[rank * SIZE + file]=pieceType(color,rank * SIZE + file)
                    file = file + 1
    def draw(self, win):
        for p,pp in enumerate(self.board):
            if self.board[p]:
                self.board[p].draw(win)
    def draw_legal_squares(self, sq):
        row = sq // SIZE
        col = sq % SIZE
        for square in enumerate(sq):
            pygame.draw.circle()

    def move(self, origPos, newPos):
        self.board[origPos].selected = False
        self.board[origPos].pos = newPos
        if isinstance(self.board[origPos], Pawn):
            self.board[origPos].first = False
        #$print(newPos // SIZE, newPos % SIZE)
        self.board[newPos] = self.board[origPos]
        self.board[origPos] = None
        
    def select(self, pos):
        #if pos clicked is an empty square, and not a legal move for previously selected, clear selected. If it is, move the piece there, then clear selected
        for piece,p in enumerate(self.board):
            if self.board[piece]:
                if self.board[piece].selected:
                    if pos in self.board[piece].squares:
                        self.move(piece, pos)
                        return
                self.board[piece].selected = False
        if self.board[pos]:
            self.board[pos].selected  = True
            self.board[pos].generate_legal_squares(self.board)
            return self.board[pos]