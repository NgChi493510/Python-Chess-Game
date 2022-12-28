"""
This file is a part of VoiceChess application.
In this file, we define a few other non-gui My-PyChess helper functions.
"""

from datetime import datetime
import os
import time

LETTER = ["", "a", "b", "c", "d", "e", "f", "g", "h"]

# encode() essentially converts a form of data used by the game to denote moves
# into the standard full algebraic notation (the kind that is used to
# communicate with a chess engine).
# To know more about the data format used by this game, checkout docs.txt
def encode(fro, to, promote=None):
    data = LETTER[fro[0]] + str(9 - fro[1]) + LETTER[to[0]] + str(9 - to[1])
    if promote is not None:
        return data + promote
    return data

# decode does the opposite of encode()
def decode(data):
    ret = [
        [LETTER.index(data[0]), 9 - int(data[1])],
        [LETTER.index(data[2]), 9 - int(data[3])],
    ]
    if len(data) == 5:
        ret.append(data[4])
    else:
        ret.append(None)
    return ret    
    
# Return the initial state (in which a chess game starts) of the chess variables
# side, board and flags
def initBoardVars():
    side = False
    board = [
        [
            [1, 7, "p"], [2, 7, "p"], [3, 7, "p"], [4, 7, "p"],
            [5, 7, "p"], [6, 7, "p"], [7, 7, "p"], [8, 7, "p"],
            [1, 8, "r"], [2, 8, "n"], [3, 8, "b"], [4, 8, "q"],
            [5, 8, "k"], [6, 8, "b"], [7, 8, "n"], [8, 8, "r"],
        ], [
            [1, 2, "p"], [2, 2, "p"], [3, 2, "p"], [4, 2, "p"],
            [5, 2, "p"], [6, 2, "p"], [7, 2, "p"], [8, 2, "p"],
            [1, 1, "r"], [2, 1, "n"], [3, 1, "b"], [4, 1, "q"],
            [5, 1, "k"], [6, 1, "b"], [7, 1, "n"], [8, 1, "r"],
        ]
    ]
    flags = [[True for _ in range(4)], None]
    return side, board, flags
    
# A simple function to undo, num corresponds to the number of moves to undo.
def undo(moves, num=1):
    if len(moves) in range(num):
        return moves
    else:
        return moves[:-num]

# Get time returned by time perf_counter in rounded millisconds
def getTime():
    return round(time.perf_counter() * 1000)

# Update the game-timer after each move
def updateTimer(side, mode, timer):
    if timer is None:
        return None
    
    ret = list(timer)
    if mode != -1:
        ret[side] += (mode * 1000)
    return ret