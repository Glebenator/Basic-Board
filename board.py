import pygame
from piece import Bishop
from piece import King
from piece import Knight
from piece import Pawn
from piece import Queen
from piece import Rook
from consts import *
def charPosToBoardPos(str):
    #e3 should be 20
    PosDict = {
        'a':0,
        'b':1,
        'c':2,
        'd':3,
        'e':4,
        'f':5,
        'g':6,
        'h':7
    }
    return ((int(str[1])-1) * SIZE + PosDict[str[0]])
class Board:
    def __init__(self):
        self.board = ((SIZE * SIZE))*[None]
        self.turn = "w"
        self.HalfMove = 0
        self.numMoves = 0
        self.EP_square = None
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
        splitFen = fen.split()
        self.turn = splitFen[1]
        self.HalfMove = int(splitFen[4])
        self.numMoves = int(splitFen[5])
        if splitFen[3] != '-':
            self.EP_square = charPosToBoardPos(splitFen[3])
            #print(self.EP_square)
        for char in splitFen[0]:
            if char == '/':
                file = 0
                rank = rank - 1
            else:
                if char.isnumeric():
                    file = file + int(char)
                else:
                    pieceType = PieceDict[char.lower()]
                    if char.isupper():
                        color = "w"
                        if pieceType == King:
                            WK = rank*SIZE + file
                    else:
                        color = "b"
                        if pieceType == King:
                            BK = rank*SIZE + file
                    
                    self.board[rank * SIZE + file]=pieceType(color,rank * SIZE + file)
                    file = file + 1
        for char in splitFen[2]:
            if char == '-':
                self.board[WK].Short_Castle = False
                self.board[WK].Long_Castle = False
                self.board[BK].Short_Castle = False
                self.board[BK].Long_Castle = False
            if char == "K":
                self.board[WK].Short_Castle = True
            if char == "Q":
                self.board[WK].Long_Castle = True
            if char == "k":
                self.board[BK].Short_Castle = True
            if char == "q":
                self.board[BK].Long_Castle = True
        




    def draw(self, win):
        for p,pp in enumerate(self.board):
            if self.board[p]:
                self.board[p].draw(win)
    def draw_legal_squares(self, sq):
        row = sq // SIZE
        col = sq % SIZE
        for square in enumerate(sq):
            pygame.draw.circle()
    def Castle(self, kingPos, rookPos):
        if rookPos - kingPos == 3:
            #short castle
            self.performMove(kingPos, kingPos + 2)
            self.performMove(rookPos, rookPos - 2)
            self.incrementMove()
            pass
        if rookPos - kingPos == -4:
            #long Castle
            self.performMove(kingPos, kingPos - 2)
            self.performMove(rookPos, rookPos + 3)
            self.incrementMove()
            pass
    def move(self, origPos, newPos):
        if self.board[origPos].color == self.turn:
            self.board[origPos].selected = False
            if isinstance(self.board[origPos], King):
                if isinstance(self.board[newPos], Rook):
                    if self.board[origPos].color == self.board[newPos].color:
                        self.Castle(origPos, newPos)
                        return
            if newPos == self.EP_square:
                #here just need to delete the pawn above/below the EP square
                if self.board[origPos].color == "w":
                    #EP square should be "above" the pawn. 
                    self.board[newPos - SIZE] = None
                else: self.board[newPos + SIZE] = None
            self.performMove(origPos, newPos)
            self.incrementMove()
            if isinstance(self.board[newPos], Pawn):
                #adding en passant Square
                if abs(newPos - origPos) == 2 * SIZE:
                    #if the pawn moved 2 squares # the squared it skipped is the EP square
                    if self.board[newPos].color == 'w':
                        if origPos//SIZE != 1:
                            return
                        else: self.EP_square = origPos + SIZE
                    elif self.board[newPos].color == 'b':
                        if origPos//SIZE != 7:
                            self.EP_square = origPos - SIZE
        else: return
    def incrementMove(self):
        if self.turn == "w":
            self.turn = "b"
        else: self.turn = "w"
        if self.EP_square != None:
            self.EP_square = None
        self.numMoves = self.numMoves + 0.5
        if self.numMoves.is_integer():
            #print(self.numMoves)
            pass
    def performMove(self, origPos, newPos):
        self.board[origPos].pos = newPos
        self.board[newPos] = self.board[origPos]
        if self.board[origPos].hasMoved == False:
            self.board[origPos].hasMoved = True
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
            if self.board[pos].color == self.turn:
                self.board[pos].selected  = True
                self.board[pos].generate_legal_squares(self.board, self.EP_square)
                return self.board[pos]
            else: return