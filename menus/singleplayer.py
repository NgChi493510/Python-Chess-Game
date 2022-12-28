'''
This file is a part of VoiceChess application.
In this file, we manage the single player menu which is called when user clicks
singleplayer button on main menu.
'''

import os.path
import random

import pygame

from tools.loader import SINGLE, BACK
from tools.utils import rounded_rect

# This shows the screen
def showScreen(win, sel):
    win.fill((140, 139, 193))

    rounded_rect(win, (255, 255, 255), (70, 5, 340, 60), 15, 4)
    win.blit(SINGLE.HEAD, (100, 7))
    win.blit(BACK, (460, 0))

    rounded_rect(win, (255, 255, 255), (10, 100, 480, 380), 12, 4)
    for cnt, i in enumerate(SINGLE.PARA1):
        y = 180 + cnt * 17
        win.blit(i, (20, y))
    win.blit(SINGLE.CHOOSE, (110, 285))
    win.blit(SINGLE.SELECT, (200, 270))
    pygame.draw.rect(win, (50, 100, 150), (200 + sel*50, 270, 50, 50), 3)

    rounded_rect(win, (255, 255, 255), (160, 350, 160, 35), 7, 3)
    win.blit(SINGLE.START, (180, 357))

# This is the main function, called from main menu
def main(win):
    sel = 0
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        showScreen(win, sel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1

                if 270 < y < 320 and 200 < x < 350:
                    sel = (x // 50) - 4

                if 160 < x < 320 and 350 < y < 385:
                    if sel == 2:
                        return True, random.randint(0, 1)
                    else:
                        return True, sel

        pygame.display.update()
