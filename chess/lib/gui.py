"""
This file is a part of VoiceChess application.
In this file, we define some basic gui-related functions

For a better understanding of the variables used here, checkout docs.txt
"""
import pygame
from tools.loader import CHESS, BACK, putLargeNum
from tools import sound

# Apply 'convert_alpha()' on all pieces to optimise images for speed.
def convertPieces(win):
    for i in range(2):
        for key, val in CHESS.PIECES[i].items():
            CHESS.PIECES[i][key] = val.convert_alpha(win)

# This function displays the choice menu when called, taking user input.
# Returns the piece chosen by the user
def getChoice(win, side): #tọa độ của các quân ở hàng trên cùng góc bên phải
    win.blit(CHESS.CHOOSE, (130, 10))
    win.blit(CHESS.PIECES[side]["q"], (250, 0)) #queen - quân hậu
    win.blit(CHESS.PIECES[side]["b"], (300, 0)) #bishop - quân tượng
    win.blit(CHESS.PIECES[side]["r"], (350, 0)) #knight - quân mã
    win.blit(CHESS.PIECES[side]["n"], (400, 0)) #rook - quân xe
    pygame.display.update((0, 0, 500, 50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #xem người chơi chọn quân nào dựa vào tọa ộ
                if 0 < event.pos[1] < 50 :#xét trong hàng đầu tiên trên cùng (pos[1] là tọa độ của y)
                    if 250 < event.pos[0] < 300: #lây tọa độ x,y từ lệnh pygame.mouse.get_pos() ở file pychess
                        return "q"
                    elif 300 < event.pos[0] < 350:
                        return "b"
                    elif 350 < event.pos[0] < 400:
                        return "r"
                    elif 400 < event.pos[0] < 450:
                        return "n"

def showTimeOver(win, side): #display thông báo hết giờ
    pygame.draw.rect(win, (140, 139, 193), (100, 190, 300, 120))
    pygame.draw.rect(win, (255, 255, 255), (100, 190, 300, 120), 4) #màu trắng
    # surface - color  -  tọa độ - chu vi - border
    win.blit(CHESS.TIMEUP[0], (220, 200))
    win.blit(CHESS.TIMEUP[1], (106, 220))
    win.blit(CHESS.TIMEUP[2], (116, 240))
    
    win.blit(CHESS.OK, (235, 274))
    pygame.draw.rect(win, (255, 255, 255), (225, 270, 50, 30), 2)
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #nếu người chơi chọn OK thì quay lại chơi nốt ván, không tính giờ nữa
                if 225 < event.pos[0] < 275 and 270 < event.pos[1] < 300:
                    return

# Renders countdown time and player icons in Timed Multiplayer
def putClock(win, timer): #hiển thị đồng hồ bấm giờ cho ván 2 người chơi
    if timer is None:
        return
    
    m1, s1 = divmod(timer[0] // 1000, 60) #chuyển thời gian người duùng chọn sang dạng phút và giây
    m2, s2 = divmod(timer[1] // 1000, 60)
    
    putLargeNum(win, format(m1, "02"), (60, 465), False) #lệnh format return giá trị đã được formatted, số 0 lấp vào vị trí trống, 2 là độ rộng của value khi trả về
    win.blit(CHESS.COL, (90, 465))
    putLargeNum(win, format(s1, "02"), (100, 465), False)
    putLargeNum(win, format(m2, "02"), (410, 465), False)
    win.blit(CHESS.COL, (440, 465))
    putLargeNum(win, format(s2, "02"), (450, 465), False)
    
    win.blit(CHESS.PIECES[0]["k"], (10, 447))
    win.blit(CHESS.PIECES[1]["k"], (360, 447)) #hiển thị icon  của bên trắng và đen ở dưới cùng ô window
    
    pygame.display.update()

# This function draws the board
def drawBoard(win):
    win.fill((254,238,230)) #màu nền
    pygame.draw.rect(win, (113,111,169), (50, 50, 400, 400)) #ô nên màu tím
    for y in range(1, 9):
        for x in range(1, 9): #vẽ các ô xanh xen kẽ đè lên nền tím
            if (x + y) % 2 == 0:
                pygame.draw.rect(win, (232,165,201), (50 * x, 50 * y, 50, 50))
                
# This funtion draws all pieces onto the board
def drawPieces(win, board, flip):
    for side in range(2): #side là biến boolean stores lượt chơi, nếu lượt tiếp là quân trắng thì return False
        for x, y, ptype in board[side]:
            if flip:
                x, y = 9 - x, 9 - y
            win.blit(CHESS.PIECES[side][ptype], (x * 50, y * 50))

# This function displays the prompt screen when a user tries to quit
# User must choose Yes or No, this function returns True or False respectively
def prompt(win): #vẽ ô thông báo khi người chơi ấn thoát
    pygame.draw.rect(win, (140, 139, 193), (110, 160, 280, 130)) #nền ô thông báo màu tím
    pygame.draw.rect(win, (255, 255, 255), (110, 160, 280, 130), 4) #viên ô màu trắng

    pygame.draw.rect(win, (255, 255, 255), (120, 160, 260, 60), 2) #viền ô có chữ, màu trắng

    win.blit(CHESS.YES, (148, 244)) #display hai option YES và NO
    win.blit(CHESS.NO, (308, 244))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2) #vẽ viền của 2 ô options
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 50, 28), 2)

    win.blit(CHESS.MESSAGE[0], (145, 166)) #hiển thị dòng thông báo
    win.blit(CHESS.MESSAGE[1], (190, 193))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #xem con chuột chọn YES hay NO
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False

# This function shows a small animation when the game starts, while also
# optimising images for display - call only once per game
def start(win, load):
    convertPieces(win)
    sound.play_start(load)
    clk = pygame.time.Clock()
    for i in range(101):
        clk.tick_busy_loop(140) # chương trình không chạy quá 140 frames một giây
        drawBoard(win)
        
        for j in range(8):
            win.blit(CHESS.PIECES[0]["p"], (0.5 * i * (j + 1), 225 + 1.25 * i)) #vẽ các quân tốt đen và trắng
            win.blit(CHESS.PIECES[1]["p"], (0.5 * i * (j + 1), 225 - 1.25 * i))
            
        for j, pc in enumerate(["r", "n", "b", "q", "k", "b", "n", "r"]):
            win.blit(CHESS.PIECES[0][pc], (0.5 * i * (j + 1), 225 + 1.75 * i))
            win.blit(CHESS.PIECES[1][pc], (0.5 * i * (j + 1), 225 - 1.75 * i))
            
        pygame.display.update()