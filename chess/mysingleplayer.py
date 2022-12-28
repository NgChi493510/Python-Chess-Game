'''
This file is a part of VoiceChess application.
In this file, we manage the chess gameplay for singleplayer section of this
application. This interfaces with a chess engine implemented in pure python.
For the Python Chess Engine, see file at chess.lib.ai

For a better understanding of the variables used here, checkout docs.txt
'''

from chess.lib import *

# Run main code for chess singleplayer
from chess.speech import *

def handle_xy(x,y, event, load, player, side ,board, win, moves, sel, flags, end, prevsel, isSpeech): #Hàm xử lý việc dùng chuột/giọng nói để chơi
    if isSpeech == False:
        x, y = event.pos
    else:
        x = x*50+1
        y=  y*50+1
    if 460 < x < 500 and 0 < y < 50 and prompt(win): #Kích thước bàn cờ 400*400 kích thước mỗi ô là 50*50 #
        return 1

    if 50 < x < 450 and 50 < y < 450:
        x, y = x // 50, y // 50
        if load["flip"] and player: #ngược lại đối với enemy
            x, y = 9 - x, 9 - y

        if isOccupied(side, board, [x, y]): #điểm đó đã có quân ở đấy thì sẽ tạo ra âm thanh "click"
            sound.play_click(load)

        prevsel = sel  #tọa độ trước đó mà mình click -  tọa độ hiện tại mình đang xử lí ->lưu lại giá trị quá khứ
        sel = [x, y]

        if (side == player #Nếu mình là người chơi
                and isValidMove(side, board, flags, prevsel, sel)): #Kiểm tra xem vị trí hiện tại có phải là vị trí hợp lệ hay không?
            promote = getPromote(win, side, board, prevsel, sel)
            animate(win, side, board, prevsel, sel, load, player) #tạo hoạt hình di chuyển

            side, board, flags = makeMove(
                side, board, prevsel, sel, flags, promote) #Make move
            moves.append(encode(prevsel, sel, promote)) #Lưu lại di chuyển

    elif side == player or end:
        sel = [0, 0]
        if 0 < x < 80 and 0 < y < 50 and load["allow_undo"]: #vị trí của UNDO
            moves = undo(moves, 2) if side == player else undo(moves)
            side, board, flags = convertMoves(moves)
    return (event, load, player, side ,board, win, moves, sel, flags, end, prevsel)

def main(win, player, load, movestr=""):
    start(win, load) #Khởi động cửa sổ trò chơi

    moves = movestr.split()
    side, board, flags = convertMoves(moves)

    clock = pygame.time.Clock()
    sel = prevsel = [0, 0]
    while True: #vòng lặp kiểm tra các sự kiện diễn ra theo thời gian thực
        clock.tick(25)
        end = isEnd(side, board, flags)

        for event in pygame.event.get(): #sự kiêện diễn ra trong game: do người dùng tạo ra: click chuột,,,,,,,
            if event.type == pygame.QUIT and prompt(win): #quit = ESC thoát game
                return 0
            elif event.type == pygame.KEYDOWN: #Bấm phím xuoongs: bấm phím bất kì
                if event.key == pygame.K_z: #Phím z: xử lí phaần giọng nói
                    voice_res = recogVoice() # CTRL+click vào hàm <- CTRl+alt+mũi tên<
                    (x, y) = extract_xy(voice_res) #ĐỌC TỌA ĐỘ
                    if x != 0 and y != 0:
                        (event, load, player, side, board, win, moves, sel, flags, end, prevsel) = handle_xy(x, y, event,
                                                                                                             load,
                                                                                                             player, side,
                                                                                                             board,
                                                                                                             win, moves,
                                                                                                             sel, flags,
                                                                                                             end, prevsel,
                                                                                                             True)
            elif event.type == pygame.MOUSEBUTTONDOWN: #click chuột xuống
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    if prompt(win):
                        return 1    #Quay về màn hingh chính
                else:
                    (event, load, player, side ,board, win, moves, sel, flags, end, prevsel) = handle_xy(0,0, event, load, player, side ,board, win, moves, sel, flags, end, prevsel, False)

        showScreen(win, side, board, flags, sel, load, player)#Hiện thị ra màn hình
        
        end = isEnd(side, board, flags)
        if side != player and not end: # Đổi lượt sang máy
            fro, to = miniMax(side, board, flags) # Máy chọn nước đi
            animate(win, side, board, fro, to, load, player)

            promote = getPromote(win, side, board, fro, to, True)
            side, board, flags = makeMove(side, board, fro, to, flags) # Gán 1 số giá trị mới

            moves.append(encode(fro, to, promote))
            sel = [0, 0]
