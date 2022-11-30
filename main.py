import pygame
import sys
from consts import *
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, WIDTH))
        self.game = Game()

    def redraw_gamewindow(self,brd):
        self.game.draw_grid(self.win)
        brd.draw(self.win)
        pygame.display.flip()

    def mainloop(self):
        self.game.brd.LoadPosFromFen(StartFen)
        self.redraw_gamewindow(self.game.brd)
        run = True
        while run:
            #self.redraw_gamewindow(self.game.brd)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.redraw_gamewindow(self.game.brd)
                    mousePos = pygame.mouse.get_pos()
                    posInd = self.game.drag.get_click_pos(mousePos)
                    p = self.game.brd.select(posInd)
                    #if p != None:
                    #    self.game.drag.save_initial(mousePos)
                    #    self.game.drag.drag_piece(p)
                    self.redraw_gamewindow(self.game.brd)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.redraw_gamewindow(self.game.brd)
                    #self.game.drag.stop_drag()
                    self.redraw_gamewindow(self.game.brd)
                #elif event.type == pygame.MOUSEMOTION:
                    if self.game.drag.dragging:
                        self.game.drag.update_mouse(event.pos)
                        #self.redraw_gamewindow(self.game.brd)
                        self.game.drag.update_blit(self.win)

main = Main()
main.mainloop()