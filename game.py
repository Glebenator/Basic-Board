import os
import pygame
import piece
from board import Board
from drag import Drag
from consts import *
Light = pygame.Color('gray')
Dark = pygame.Color('red')



class Game:
    def __init__(self):
        self.brd = Board()
        self.drag = Drag()

    def draw_grid(self, win):
        for file in range (SIZE):
            for rank in range(SIZE):
                isLightSq = (file + rank) % 2 != 0
                if isLightSq:
                    squareColor = Light
                else: squareColor = Dark
                position = pygame.Rect(SQSIZE*rank,SQSIZE*file,SQSIZE,SQSIZE)
                pygame.draw.rect(win, squareColor, position)
                