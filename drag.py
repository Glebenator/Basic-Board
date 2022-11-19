import pygame
from consts import *

class Drag:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.init_pos = 0
        self.dragging = False
        self.piece = None
    
    def update_blit(self,win):
        #make texture a bit bigger
        center = (self.mouseX, self.mouseY)
        self.piece.drag = self.dragging
        self.piece.draw(win, center)


    def update_mouse(self,mousePos):
        self.mouseX,self.mouseY = mousePos
    def get_click_pos(self,mousePos):
        self.update_mouse(mousePos)
        row = (self.mouseX//(SQSIZE))
        col = (self.mouseY//(SQSIZE))
        return (row)+SIZE*(col)
    def save_initial(self,mousePos):
        self.init_pos = self.get_click_pos(mousePos)
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
        self.piece.drag = True
    def stop_drag(self):
        self.piece.drag = False
        #elf.piece = None
        self.dragging = False