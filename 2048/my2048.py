import pygame
import sys
from pygame.locals import *
from random import randint
import copy
import math
from pgu import gui

# defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 480
WINDOWHEIGHT = 640
boxsize = min(WINDOWWIDTH, WINDOWHEIGHT)//4
margin = 5
thickness = 0
# defining the RGB for various colours used
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
DARKGREEN = (0, 155,   0)
DARKGRAY = (40,  40,  40)
LIGHTSALMON = (255, 160, 122)
ORANGE = (221, 118, 7)
LIGHTORANGE = (227, 155, 78)
CORAL = (255, 127, 80)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 150)
colorback = (189, 174, 158)
colorblank = (205, 193, 180)
colorlight = (249, 246, 242)
colordark = (119, 110, 101)

fontSize = [100, 85, 70, 55, 40]
fontSize = [75, 64, 52, 41, 30]
fontSize = [50, 50, 50, 50, 50]

dictcolor1 = {
    0: colorblank,
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 95, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 190, 30),
    8192: (239, 180, 25)}

dictcolor2 = {
    2: colordark,
    4: colordark,
    8: colorlight,
    16: colorlight,
    32: colorlight,
    64: colorlight,
    128: colorlight,
    256: colorlight,
    512: colorlight,
    1024: colorlight,
    2048: colorlight,
    4096: colorlight,
    8192: colorlight}
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


class Button(object):
    def __init__(self, screen: pygame.surface.Surface, text, color, font: pygame.font.Font, x, y, width, height) -> None:
        self.surface_ = font.render(text, True, color)
        self.width_ = width
        self.height_ = height
        self.x_ = x
        self.y_ = y
        self.screen_ = screen

    def display(self) -> None:
        pygame.draw.rect(self.screen_, colorblank,
                         (self.x_, self.y_, self.width_, self.height_))
        text_rect = self.surface_.get_rect()
        text_rect.center = (self.x_ + (self.width_/2),
                            self.y_ + (self.height_/2))
        self.screen_.blit(self.surface_, text_rect)

    def is_clicked(self, position_x, position_y) -> bool:
        x_match = (position_x > self.x_) and (
            position_x < (self.x_ + self.width_))
        y_match = (position_y > self.y_) and (
            position_y < (self.y_ + self.height_))
        if x_match and y_match:
            return True
        else:
            return False


class Label(object):
    def __init__(self, screen: pygame.surface.Surface, text, color, font: pygame.font.Font, x, y, width, height) -> None:
        self.surface_ = font.render(text, True, color)
        self.width_ = width
        self.height_ = height
        self.x_ = x
        self.y_ = y
        self.screen_ = screen

    def display(self) -> None:
        pygame.draw.rect(self.screen_, colorblank,
                         (self.x_, self.y_, self.width_, self.height_))
        text_rect = self.surface_.get_rect()
        text_rect.center = (self.x_ + (self.width_/2),
                            self.y_ + (self.height_/2))
        self.screen_.blit(self.surface_, text_rect)


class My2048(object):
    def __init__(self):
        # score show
        pygame.init()
        self.score_label_ = None
        self.best_label_ = None
        self.best_score_ = 0
        self.current_score_ = 0
        self.window_ = None
        self.new_game_btn_ = None
        self.fps_clock_ = pygame.time.Clock()
        self.window_ = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.basic_font_ = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption("2048")
        self.table_ = copy.deepcopy(TABLE)

    def movedown(self, pi, pj, T):
        justcomb = False
        while pi < 3 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
            if T[pi+1][pj] == 0:
                T[pi+1][pj] = T[pi][pj]
            elif T[pi+1][pj] == T[pi][pj]:
                T[pi+1][pj] += T[pi][pj]
                self.current_score_ += T[pi+1][pj]
                if self.best_score_ < self.current_score_:
                    self.best_score_ = self.current_score_
                justcomb = True
            T[pi][pj] = 0
            pi += 1
        return T

    def moveleft(self, pi, pj, T):
        justcomb = False
        while pj > 0 and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj] and not justcomb)):
            if T[pi][pj-1] == 0:
                T[pi][pj-1] = T[pi][pj]
            elif T[pi][pj-1] == T[pi][pj]:
                T[pi][pj-1] += T[pi][pj]
                self.current_score_ += T[pi][pj-1]
                if self.best_score_ < self.current_score_:
                    self.best_score_ = self.current_score_
                justcomb = True
            T[pi][pj] = 0
            pj -= 1
        return T

    def moveright(self, pi, pj, T):
        justcomb = False
        while pj < 3 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj] and not justcomb)):
            if T[pi][pj+1] == 0:
                T[pi][pj+1] = T[pi][pj]
            elif T[pi][pj+1] == T[pi][pj]:
                T[pi][pj+1] += T[pi][pj]
                self.current_score_ += T[pi][pj+1]
                if self.best_score_ < self.current_score_:
                    self.best_score_ = self.current_score_
                justcomb = True
            T[pi][pj] = 0
            pj += 1
        return T

    def moveup(self, pi, pj, T):
        justcomb = False
        while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
            if T[pi-1][pj] == 0:
                T[pi-1][pj] = T[pi][pj]
            elif T[pi-1][pj] == T[pi][pj]:
                T[pi-1][pj] += T[pi][pj]
                self.current_score_ += T[pi-1][pj]
                if self.best_score_ < self.current_score_:
                    self.best_score_ = self.current_score_
                justcomb = True
            T[pi][pj] = 0
            pi -= 1
        return T

    def key(self, DIRECTION):
        if DIRECTION == 'w':
            for pi in range(1, 4):
                for pj in range(4):
                    if self.table_[pi][pj] != 0:
                        self.table_ = self.moveup(pi, pj, self.table_)
        elif DIRECTION == 's':
            for pi in range(2, -1, -1):
                for pj in range(4):
                    if self.table_[pi][pj] != 0:
                        self.table_ = self.movedown(pi, pj, self.table_)
        elif DIRECTION == 'a':
            for pj in range(1, 4):
                for pi in range(4):
                    if self.table_[pi][pj] != 0:
                        self.table_ = self.moveleft(pi, pj, self.table_)
        elif DIRECTION == 'd':
            for pj in range(2, -1, -1):
                for pi in range(4):
                    if self.table_[pi][pj] != 0:
                        self.table_ = self.moveright(pi, pj, self.table_)
        self.update_current_score()
        self.update_best_score()
        return self.table_

    def update_best_score(self):
        # score label
        self.score_label_ = Label(self.window_, "Score: %4d" % (
            self.current_score_), WHITE, self.basic_font_, 360, 50, 110, 40)
        self.score_label_.display()

    def update_current_score(self):
        # best label
        self.best_label_ = Label(self.window_, "Best: %4d" % (
            self.best_score_), WHITE, self.basic_font_, 360, 10, 110, 40)
        self.best_label_.display()

    def show_outline_info(self):
        # the outline info
        titleFont = pygame.font.Font('freesansbold.ttf', 50)
        titleSurf1 = titleFont.render('2048', True, WHITE, colorback)

        self.window_.fill(colorback)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 6, WINDOWHEIGHT/16)
        self.window_.blit(display_rect, rectangle)

        # score label
        self.update_current_score()
        # best label
        self.update_best_score()
        # new game button
        self.new_game_btn_ = Button(
            self.window_, "New Game", WHITE, self.basic_font_, 360, 100, 110, 40)
        self.new_game_btn_.display()

    def show(self):
        self.show_outline_info()
        # showing the table
        # self.window_.fill(colorback)
        myfont = pygame.font.SysFont("Arial", 60, bold=True)
        position_h = WINDOWHEIGHT - WINDOWWIDTH
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.window_, dictcolor1[self.table_[i][j]], (j*boxsize+margin,
                                                                               i*boxsize+margin + position_h,
                                                                               boxsize-2*margin,
                                                                               boxsize-2*margin),
                                 thickness)
                if self.table_[i][j] != 0:
                    order = int(math.log10(self.table_[i][j]))
                    myfont = pygame.font.SysFont(
                        "Arial", fontSize[order], bold=True)
                    label = myfont.render(
                        "%4s" % (self.table_[i][j]), 1, dictcolor2[self.table_[i][j]])
                    self.window_.blit(label, (j*boxsize + 0.5*boxsize - label.get_rect().width/2,
                                              position_h + i*boxsize + 0.5*boxsize - label.get_rect().height/2))

        pygame.display.update()

    def randomfill(self):
        # search for zero in the game table and randomly fill the places
        flatTABLE = sum(self.table_, [])
        if 0 not in flatTABLE:
            return self.table_
        empty = False
        w = 0
        while not empty:
            w = randint(0, 15)
            if self.table_[w//4][w % 4] == 0:
                empty = True
        z = randint(1, 5)
        if z == 5:
            self.table_[w//4][w % 4] = 4
        else:
            self.table_[w//4][w % 4] = 2
        return self.table_

    def show_gameover_message(self):
        # to show game over self.window_
        # print (" gameover message ")
        self.show_outline_info()
        myfont = pygame.font.SysFont("Arial", 60, bold=True)
        over_surface = myfont.render('Game Over!!!', True, WHITE, colorback)
        over_rect = over_surface.get_rect()
        over_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT*0.6)
        self.window_.blit(over_surface, over_rect)
        pygame.display.update()

    def game_over(self):
        # returns False if a box is empty or two boxes can be merged
        x = [-1, 0, 1, 0]
        y = [0, 1, 0, -1]
        for pi in range(4):
            for pj in range(4):
                if self.table_[pi][pj] == 0:
                    return False
                for point in range(4):
                    if pi+x[point] > -1 and pi+x[point] < 4 and pj+y[point] > -1 and pj+y[point] < 4 and self.table_[pi][pj] == self.table_[pi+x[point]][pj+y[point]]:
                        return False
        return True

    def run(self):
        # print("new game----")
        self.table_ = self.randomfill()
        self.table_ = self.randomfill()
        self.show()
        running = True

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                # print (mouse, click)
                if event.type == QUIT:
                    # print("quit")
                    pygame.quit()
                    sys.exit()

                if self.new_game_btn_ is not None and self.new_game_btn_.is_clicked(mouse[0], mouse[1]) and click[0]:
                    # print ("new game")
                    self.table_ = copy.deepcopy(TABLE)
                    self.current_score_ = 0
                    return self.run()

                if event.type == pygame.KEYDOWN:
                    if running:
                        desired_key = None
                        if event.key == pygame.K_UP:
                            desired_key = "w"
                        if event.key == pygame.K_DOWN:
                            desired_key = "s"
                        if event.key == pygame.K_LEFT:
                            desired_key = "a"
                        if event.key == pygame.K_RIGHT:
                            desired_key = "d"

                        if desired_key is None:
                            continue
                        if self.game_over():
                            self.show_gameover_message()
                            continue
                        new_table = self.key(desired_key)
                        if new_table != TABLE:
                            self.randomfill()
                            self.show()


if __name__ == "__main__":
    mygame = My2048()
    mygame.run()
