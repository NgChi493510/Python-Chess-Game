'''
This file is a part of VoiceChess application.
In this file, we manage the timer menu to configure the timer for multiplayer
chess.
'''
import pygame

from tools.loader import TIMER, BACK, putLargeNum
from tools.utils import rounded_rect

# This shows the initial prompt message
def start(win, load):
    rounded_rect(win, (255, 255, 255), (120, 180, 260, 100), 10, 4)

    win.blit(TIMER.PROMPT, (150, 200))

    win.blit(TIMER.YES, (150, 245))
    win.blit(TIMER.NO, (307, 245))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 45, 28), 2)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return None
                    elif 300 < event.pos[0] < 350:
                        if load["show_clock"]:
                            return -1, (0, 0)
                        else:
                            return None, None

# This shows the screen
def showScreen(win, sel, sel2):
    win.fill((140, 139, 193))

    rounded_rect(win, (255, 255, 255), (70, 5, 340, 60), 15, 4)
    win.blit(TIMER.HEAD, (100, 12))
    win.blit(BACK, (460, 0))

    rounded_rect(win, (255, 255, 255), (10, 70, 480, 420), 12, 4)
    
    for cnt, i in enumerate(TIMER.TEXT):
        y = 75 + cnt * 18
        win.blit(i, (20, y))
        
    for i in range(6):
        pygame.draw.rect(win, (255, 255, 255), (113 + 39*i, 197, 28, 23), 3)
        
    for i in range(5):
        pygame.draw.rect(win, (255, 255, 255), (114 + 40*i, 287, 28, 23), 3)
        
    pygame.draw.rect(win, (192,193,139), (113 + 39*sel, 197, 28, 23), 3)
    pygame.draw.rect(win, (192,193,139), (114 + 40*sel2, 287, 28, 23), 3)
        
    pygame.draw.rect(win, (255, 255, 255), (312, 414, 50, 23), 3)
    pygame.display.update()

# This is the main function, called from main menu
def main(win, load):
    ret = start(win, load)
    if ret is not None:
        return ret
    
    sel = sel2 = 0
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        showScreen(win, sel, sel2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1
                
                if 312 < x < 362 and 414 < y < 437:
                    if sel == 0:
                        temp = (30 * 60 * 1000,)*2
                    if sel == 1:
                        temp = (15 * 60 * 1000,)*2
                    if sel == 2:
                        temp = (10 * 60 * 1000,)*2
                    if sel == 3:
                        temp = (5 * 60 * 1000,)*2
                    if sel == 4:
                        temp = (3 * 60 * 1000,)*2
                    if sel == 5:
                        temp = (1 * 60 * 1000,)*2
                    return sel2, temp
                
                for i in range(6):
                    if 113 + 39*i < x < 141 + 39*i and 200 < y < 223:
                        sel = i
                        break
                        
                for i in range(5):
                    if 114 + 40*i < x < 142 + 40*i and 290 < y < 313:
                        sel2 = i
                        break
