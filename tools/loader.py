"""
This file is a part of VoiceChess application.
This file loads all the images and texts that are used.

Most of the scripts in this application import specific classes from this
module. Each class is a collection of resources for a particular script.
All font-related stuff is done in this file, the functions to put a number
on the screen and display date and time are also defined here
"""

import os.path #used for different purposes such as for merging, normalizing and retrieving path names in python .
import pygame

# Initialize pygame.font module and load the font file.
pygame.font.init()
FONT = os.path.join("res", "LeagueSpartan-Bold.otf") # join various path components

# Load different sizes of the font.
head = pygame.font.Font(FONT, 60)
large = pygame.font.Font(FONT, 45)
medium = pygame.font.Font(FONT, 28)
small = pygame.font.Font(FONT, 20)
vsmall = pygame.font.Font(FONT, 15)

# Define RGB color constants for use.
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (200, 20, 20)
VIOLET = (133,113,148)


# Define a few constants that contain loaded texts of numbers and chararters.
LNUM = [small.render(str(i), True, WHITE) for i in range(10)] #hàm render trong pyBox
BLNUM = [small.render(str(i), True, BLACK) for i in range(10)]
COLON = vsmall.render(":", True, WHITE)

# This function displays a number in a position, Small sized text used.
def putLargeNum(win, num, pos, white=True):
    for cnt, i in enumerate(list(str(num))):
        if white:
            win.blit(LNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))
        else:
            win.blit(BLNUM[int(i)], (pos[0] + (cnt * 14), pos[1]))

# Defined important globals for loading background image sprites.
PSPRITE = pygame.image.load(os.path.join("res", "img", "piecesprite.png"))

# Load global image for back
BACK = pygame.image.load(os.path.join("res", "img", "back.png"))

class CHESS:
    PIECES = ({}, {})
    for i, ptype in enumerate(["k", "q", "b", "n", "r", "p"]):
        for side in range(2):
            PIECES[side][ptype] = PSPRITE.subsurface((i * 50, side * 50, 50, 50))

    CHECK = small.render("CHECK!", True, BLACK)
    STALEMATE = small.render("STALEMATE!", True, BLACK)
    CHECKMATE = small.render("CHECKMATE!", True, BLACK)
    LOST = small.render("LOST", True, BLACK)
    CHOOSE = small.render("CHOOSE:", True, BLACK)
    UNDO = small.render("Undo", True, BLACK)

    SPEAK = (
        vsmall.render("Press Z, wait for 2 seconds", True, BLACK),
        vsmall.render("and say a grid", True, BLACK)
    )
    X_AXIS = (
        vsmall.render("a", True, VIOLET),
        vsmall.render("b", True, VIOLET),
        vsmall.render("c", True, VIOLET),
        vsmall.render("d", True, VIOLET),
        vsmall.render("e", True, VIOLET),
        vsmall.render("f", True, VIOLET),
        vsmall.render("g", True, VIOLET),
        vsmall.render("h", True, VIOLET)
    )

    Y_AXIS = (
        vsmall.render("1", True, VIOLET),
        vsmall.render("2", True, VIOLET),
        vsmall.render("3", True, VIOLET),
        vsmall.render("4", True, VIOLET),
        vsmall.render("5", True, VIOLET),
        vsmall.render("6", True, VIOLET),
        vsmall.render("7", True, VIOLET),
        vsmall.render("8", True, VIOLET)
    )
    MESSAGE = (
        small.render("Do you want to quit", True, WHITE),
        small.render("this game?", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

    TURN = (
        small.render("Others turn", True, BLACK),
        small.render("Your turn", True, BLACK),
    )

    DRAW = small.render("Draw", True, BLACK)
    RESIGN = small.render("Resign", True, BLACK)
    
    TIMEUP = (
        vsmall.render("Time Up!", True, WHITE),
        vsmall.render("Technically the game is over, but you", True, WHITE),
        vsmall.render("can still continue if you wish to - :)", True, WHITE),
    )
    
    OK = small.render("Ok", True, WHITE)
    COL = small.render(":", True, BLACK)


class MAIN:
    HEADING = head.render("VoiceChess", True, WHITE)
    VERSION = vsmall.render("Group 7", True, WHITE)
    ICON = pygame.image.load(os.path.join("res", "img", "icon.gif"))
    BG = pygame.image.load(os.path.join("res", "img", "bgr.jpg"))

    SINGLE = medium.render("SinglePlayer", True, WHITE)
    MULTI = medium.render("MultiPlayer", True, WHITE)
    PREF = medium.render("Preferences", True, WHITE)

    SINGLE_H = medium.render("SinglePlayer", True, GREY)
    MULTI_H = medium.render("MultiPlayer", True, GREY)
    PREF_H = medium.render("Preferences", True, GREY)


class PREF:
    HEAD = large.render("Preferences", True, WHITE)

    SOUNDS = medium.render("Sounds", True, WHITE)
    FLIP = medium.render("Flip screen", True, WHITE)
    CLOCK = medium.render("Show Clock", True, WHITE)
    MOVE = medium.render("Show Moves", True, WHITE)
    UNDO = medium.render("Allow undo", True, WHITE)

    COLON = medium.render(":", True, WHITE)

    TRUE = medium.render("True", True, WHITE)
    FALSE = medium.render("False", True, WHITE)

    SOUNDS_H = (
        vsmall.render("Play different sounds", True, WHITE),
        vsmall.render("and music", True, WHITE),
    )
    FLIP_H = (
        vsmall.render("This flips the screen", True, WHITE),
        vsmall.render("after each move", True, WHITE),
    )
    CLOCK_H = (
        vsmall.render("Show a clock in chess", True, WHITE),
        vsmall.render("when timer is disabled", True, WHITE),
    )
    MOVE_H = (
        vsmall.render("This shows all the legal", True, WHITE),
        vsmall.render("moves of a selected piece", True, WHITE),
    )
    UNDO_H = (
        vsmall.render("This allows undo if", True, WHITE),
        vsmall.render("set to be true", True, WHITE),
    )

    BSAVE = medium.render("Save", True, WHITE)
    TIP = vsmall.render("TIP: Hover the mouse over the feature", True, WHITE)
    TIP2 = vsmall.render("name to know more about it.", True, WHITE)

    PROMPT = (
        vsmall.render("Are you sure you want to leave?", True, WHITE),
        vsmall.render("Any changes will not be saved.", True, WHITE),
    )

    YES = small.render("YES", True, WHITE)
    NO = small.render("NO", True, WHITE)

class SINGLE:
    HEAD = large.render("Singleplayer", True, WHITE)
    SELECT = pygame.image.load(os.path.join("res", "img", "select.jpg"))
    CHOOSE = small.render("Choose:", True, WHITE)
    START = small.render("Start Game", True, WHITE)
    
    with open(os.path.join("res", "texts", "single1.txt")) as f:
        PARA1 = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]


class TIMER:
    HEAD = large.render("Timer Menu", True, WHITE)
    
    YES = small.render("Yes", True, WHITE)
    NO = small.render("No", True, WHITE)
    
    PROMPT = vsmall.render("Do you want to set timer?", True, WHITE)

    with open(os.path.join("res", "texts", "timer.txt"), "r") as f:
        TEXT = [vsmall.render(i, True, WHITE) for i in f.read().splitlines()]
    

pygame.font.quit()