'''
This file is a part of VoiceChess application.
In this file, we manage the preferences menu which is called when user clicks
preferences button on main menu.

We also define functions to save and load user preferences.
'''

import os.path # os là module để làm việc với các file, thư mục, còn os.path hỗ trợ thao tác trên đường dẫn
import pygame
from tools.loader import PREF, BACK
from tools.utils import rounded_rect

KEYS = ["sounds", "flip", "slideshow", "show_moves", "allow_undo", "show_clock"]

DEFAULTPREFS = {
    "sounds": False,
    "flip": False,
    "show_moves": True,
    "allow_undo": True,
    "show_clock": False        #dic mặc định các chức năng trong preferences, chức năng sẽ được giải thích ở dưới
}

# This function saves user preferences in a text file. Lưu tùy chọn của người chơi vào văn bản preferences.txt
def save(load):
    with open(os.path.join("res", "preferences.txt"), "w") as f:
        for key, val in load.items():
            f.write(key + " = " + str(val) + '\n')  # tạo và add vào dictionry 

# This function loads user preferences from a text file
def load():
    path = os.path.join("res", "preferences.txt")  
    if not os.path.exists(path): # kiểm tra sự tồn tại của file path
        open(path, "w").close()  # nếu file path khong ton tai thi mơ 1 file mới để write sau đó đóng lại để giải phóng tệp
    
    with open(path, "r") as f:  # đọc file path
        mydict = {}  
        for line in f.read().splitlines():    
            lsplit = line.split("=")              # đọc từng dọc và split qua dấu =
            if len(lsplit) == 2:                 # lsplit co 2 phan tử, ở vị trí 0 là như sound, flip, slideshow còn vị trí 1 - tức val chỉ có true, false
                val = lsplit[1].strip().lower()     # strip() dể xóa khoảng trống
                if val == "true":
                    mydict[lsplit[0].strip()] = True   # tức là bật, chẳng hạn, key = sound, val = true, thì mydict = True -> bật sound
                elif val == "false":
                    mydict[lsplit[0].strip()] = False
            
        for key in mydict:
            if key not in KEYS:      # key có trong mydict nhưng ko có trong KEYS (dòng 14) thì bỏ khỏi mydict
                mydict.pop(key)
        
        for key in KEYS:
            if key not in mydict:
                mydict[key] = DEFAULTPREFS[key]   # key có trong KEYs nhưng ko trong mydict thig để chế độ mặc định (line16)
        return mydict

# This function displays the prompt screen when a user tries to quit
# User must choose Yes or No, this function returns True or False respectively
def prompt(win):                         #chức năng hiển thị màn hình để nhắc nhở khi người dùng cố gắng thoát
    rounded_rect(win, (255, 255, 255), (110, 160, 280, 130), 4, 4)   # # win là cái màn hình như này  win = pygame.display.set_mode((500, 500), pygame.SCALED)
                      # màu theo RGB (đen - viền)  # tọa đọ x,y, chiều dài+x, rộng+y), 4,4 là để tạo hình rỗng và nó là linewidth và phần cong 
                      # rounded_rect là cái HCN mà 4 đỉnh là góc hơi tròn (chi tiết gg)         (bỏ pygame.Scaled cx chạy bình thường)
    win.blit(PREF.PROMPT[0], (125, 175))     # hiển thị dòng chứ số 1 của thông báo

    win.blit(PREF.PROMPT[1], (125, 200))    # và dòng thứ 2

    win.blit(PREF.YES, (148, 244))            # BLIT LÀ CÂU LỆNH ĐỂ VẼ CHÈN CHỮ LÊN CÁC Ô ROUNDED_RECT
    win.blit(PREF.NO, (305, 244))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2) # tạo hcn rỗng, linewidth = 2
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 45, 28), 2)

    pygame.display.flip() # cập nhật toàn bộ màn hình.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:   #hàm pygame.MOUSEBUTTONDOWN cho biết người chơi đã nhấn một nút trên chuột
                                                       #khi đó sự kiện ấy sẽ xuất hiện trong danh sách những sự kiện mà chương trình nhận được từ hàm pygame.event.get().
                if 240 < event.pos[1] < 270:     #event.pos ghi vị trí toạ độ nơi bấm chuột event.pos[1] là vị trí của y , event.pos[0] là x
                    if 140 < event.pos[0] < 200: # tức là vùng bấm event.pos[0] trong khoảng 140, 270 --> nó là YES, trả TRUE :   win.blit(PREF.YES, (145, 240))
                        return True
                    elif 300 < event.pos[0] < 350: # tương tự nhứ trên, trong khoảng này, mk bấm vào NO, trả FALSE
                        return False

# This function shows the screen   # hiển thị màn hình
def showScreen(win, prefs):
    win.fill((140, 139, 193))          # tô cả cái màn hình bằng màu đen

    rounded_rect(win, (255, 255, 255), (70, 10, 350, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (10, 85, 480, 360), 12, 4)      # vẽ các hình rounded_rect

    win.blit(BACK, (460, 0))  # vị trí của ký tự Back
    win.blit(PREF.HEAD, (110, 23))  # vị trí của HEAD, tức Heading, là dòng chữ tiêu đề
    
    rounded_rect(win, (255, 255, 255), (10, 450, 310, 40), 10, 3)  # tiếp tục là 1 hình rounded_rect ở góc cuối bên trái tròng PREF, ghi các TIP
    win.blit(PREF.TIP, (20, 453))
    win.blit(PREF.TIP2, (55, 470))

    win.blit(PREF.SOUNDS, (110, 106))
    win.blit(PREF.FLIP, (65, 166))
    win.blit(PREF.MOVE, (35, 226))
    win.blit(PREF.UNDO, (45, 286))
    win.blit(PREF.CLOCK, (40, 346)) # Thêm các chữ SOund, flip,... vào màn hình vào các vị trí có tọa đọ (90, 90), (25,150),...
                                        # để ý thấy các tọa độ y của từng option cách đều 60 để hiểu tại sao ở dưới i*60
    for i in range(5):           # đặt dấu : giữ các tùy chọn sound, flip, slideshow và tùy chọn TRUE, FALSE (có 6 lựa chọn)
        win.blit(PREF.COLON, (225, 106 + (i * 60))) # thay vị trí y của từng dáu :
        if prefs[KEYS[i]]:           # nếu i là option đc chọn thì thêm 1 hình round_rect quang options đó
            rounded_rect(
                win, (255, 255, 255), (249, 102 + (60 * i), 80, 40), 8, 2)    # TRUE, chọn 249,102 là tăng thêm chút sai số cho việc bấm vào ô đó chắc chắn
        else:
            rounded_rect(
                win, (255, 255, 255), (359, 102 + (60 * i), 90, 40), 8, 2)
        win.blit(PREF.TRUE, (256, 105 + (i * 60)))
        win.blit(PREF.FALSE, (366, 105 + (i * 60)))         # Vẽ thêm chữ TRUE, FALSE sau dấu : mỗi options

    rounded_rect(win, (255, 255, 255), (350, 452, 85, 40), 10, 2)
    win.blit(PREF.BSAVE, (355, 455))                 # tạo ô và vẽ chữ SAVE ( ô ở cuối góc bên phải)

    x, y = pygame.mouse.get_pos()   #Lấy vị trí chuột và lưu trong biến x,y
    if 100 < x < 220 and 106 < y < 146:
        pygame.draw.rect(win, (140, 139, 193), (30, 106, 195, 40))
        win.blit(PREF.SOUNDS_H[0], (45, 100))
        win.blit(PREF.SOUNDS_H[1], (90, 120))                   # phần này là để khi mình di chuyển đển từng options sound, flip, slideshow,...
                                                                # nó sẽ hiện chức này của các option đó, mn chạy thử game, rồi vào prefence, di chuyển đến từng option
    if 25 < x < 220 and 156 < y < 196:                          # sẽ có các dòng chữ ghi chức năng là hiểu ngay
        pygame.draw.rect(win, (140, 139, 193), (15, 166, 210, 50)) # hcn đặc, nguyên đen rồi blit mấy cái dòng chữ flip_h[0],[1]  vào trong hcn đó
        win.blit(PREF.FLIP_H[0], (50, 166))
        win.blit(PREF.FLIP_H[1], (70, 186))
    if 40 < x < 220 and 216 < y < 256:
        pygame.draw.rect(win, (140, 139, 193), (15, 226, 210, 40))
        win.blit(PREF.MOVE_H[0], (40, 226))
        win.blit(PREF.MOVE_H[1], (30, 246))
    if 25 < x < 220 and 276 < y < 316:
        pygame.draw.rect(win, (140, 139, 193), (15, 286, 210, 40))
        win.blit(PREF.UNDO_H[0], (35, 286))
        win.blit(PREF.UNDO_H[1], (35, 306))
    if 25 < x < 220 and 336 < y < 376:
        pygame.draw.rect(win, (140, 139, 193), (15, 346, 210, 40))
        win.blit(PREF.CLOCK_H[0], (35, 346))
        win.blit(PREF.CLOCK_H[1], (25, 366))


# This is the main function, called by the main menu
def main(win):
    prefs = load()
    clock = pygame.time.Clock()       # só khung hình chạy trong 1s
    while True:
        clock.tick(24)    # cụ thể là 24 khung hình trong 1s
        showScreen(win, prefs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and prompt(win):
                return 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50 and prompt(win):  #x, y này chính là tọa độ ký tự BACK
                    return 1

                if 350 < x < 425 and 450 < y < 490:      # tạo độ SAVE
                    save(prefs)
                    return 1

                for i in range(5):
                    if 105 + i*60 < y < 145 + i*60:
                        if 256 < x < 336:
                            prefs[KEYS[i]] = True                # giống ở phần trên
                        if 366 < x < 436:
                            prefs[KEYS[i]] = False
        pygame.display.update()
