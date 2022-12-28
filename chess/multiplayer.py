'''
This file is a part of VoiceChess application.
In this file, we manage the chess gameplay for multiplayer section of this
application.
'''

from chess.lib import *
from chess.speech import *

# run main code for chess
def handle_xy(x,y, event, load, timedelta, side ,board, win, moves, sel, flags, mode, prevsel, timer, isSpeech): #Hàm xử lý việc dùng chuột/giọng nói để chơi
    if isSpeech == False:
        x, y = event.pos
    else:
        x = x*50+1
        y=  y*50+1
    if 460 < x < 500 and 0 < y < 50: #Kích thước bàn cờ 400*400 kích thước mỗi ô là 50*50 #
        starttime = getTime()
        if prompt(win):
            return 1
        timedelta += getTime() - starttime

    if 50 < x < 450 and 50 < y < 450:
        x, y = x // 50, y // 50
        if load["flip"] and side: #ngược lại đối với enemy
            x, y = 9 - x, 9 - y

        if isOccupied(side, board, [x, y]): #điểm đó đã có quân ở đấy thì sẽ tạo ra âm thanh "click
            sound.play_click(load)

        prevsel = sel #tọa độ trước đó mà mình click -  tọa độ hiện tại mình đang xử lí ->lưu lại giá trị quá khứ
        sel = [x, y]

        if isValidMove(side, board, flags, prevsel, sel): #Kiểm tra xem vị trí hiện tại có phải là vị trí hợp lệ hay không?
            starttime = getTime()
            promote = getPromote(win, side, board, prevsel, sel)
            animate(win, side, board, prevsel, sel, load) #tạo hoạt hình di chuyển

            timedelta += getTime() - starttime #Thời gian còn lại
            timer = updateTimer(side, mode, timer) #cập nhật bộ dếm ngược

            side, board, flags = makeMove(
                side, board, prevsel, sel, flags, promote) #Make move
            moves.append(encode(prevsel, sel, promote)) #Lưu lại di chuyển

    else:
        sel = [0, 0] #reset lựa chọn
        if 350 < x < 500 and 460 < y < 490:
            starttime = getTime()   # tiếp tục đếm giờ
            timedelta += getTime() - starttime

        elif 0 < x < 80 and 0 < y < 50 and load["allow_undo"]:
            moves = undo(moves) #undo
            side, board, flags = convertMoves(moves)

    return (event, load, timedelta, side ,board, win, moves, sel, flags, mode, prevsel, timer)

def main(win, mode, timer, load, movestr=""):
    start(win, load) # Chạy màn hình đánh cờ

    moves = movestr.split()

    side, board, flags = convertMoves(moves)
    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]

    if timer is not None:
        timer = list(timer) # Khởi động bộ đếm giờ
    while True: #vòng lặp kiểm tra các sự kiện diễn ra theo thời gian thực
        looptime = getTime()
        clock.tick(25) #Chạy game 25 fps

        timedelta = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starttime = getTime()
                if prompt(win):
                    return 0 # Thoát trận
                timedelta += getTime() - starttime
            elif event.type == pygame.KEYDOWN: #Phát hiện bấm nút trên bàn phím
                if event.key == pygame.K_z: #Nếu bấm phím Z
                    voice_res = recogVoice() #Lấy từ ngữ từ mic
                    (x, y) = extract_xy(voice_res) #Đọc tọa độ
                    if x != 0 and y != 0: # Thực hiện nước đi
                        (event, load, timedelta, side ,board, win, moves, sel, flags, mode, prevsel, timer) = handle_xy(x,y, event,
                                                                                                                        load,
                                                                                                             timedelta, side ,
                                                                                                             board, win, moves,
                                                                                                             sel, flags,
                                                                                                             mode, prevsel,
                                                                                                             timer, True)

            elif event.type == pygame.MOUSEBUTTONDOWN: #Nếu click chuột
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    if prompt(win):
                        return 1    #Quay về màn hình chính
                else:   # Đi bằng chuột như thường
                    (event, load, timedelta, side, board, win, moves, sel, flags, mode, prevsel, timer) = handle_xy(0, 0,
                                                                                                                event,
                                                                                                                load,
                                                                                                                timedelta,
                                                                                                                side,
                                                                                                                board,
                                                                                                                win,
                                                                                                                moves,
                                                                                                                sel,
                                                                                                                flags,
                                                                                                                mode,
                                                                                                                prevsel,
                                                                                                                timer,
                                                                                                                False)

        showScreen(win, side, board, flags, sel, load) #Cập nhật màn hình
        timer = showClock(win, side, mode, timer, looptime, timedelta) #Cập nhật bộ đếm giờ