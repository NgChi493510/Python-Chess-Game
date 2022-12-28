"""
This file is a part of VoiceChess application.
In this file, we define the core chess-related functions.
For a better understanding of the variables used here, checkout docs.txt
"""
# Hàm đơn giản để sao chép cách bố trí hiện tại của bàn cờ
def copy(board):
    return [[list(j) for j in board[i]] for i in range(2)]       
        
# Tìm loại của quân cờ dựa vào màu và vị trí, return None nếu không có quân tại vị trí
def getType(side, board, pos):
    for piece in board[side]:
        if piece[:2] == pos: #Nếu vị trí của quân cờ khớp với pos
            return piece[2] #Trả về tên quân cờ
# Dựa vào tên quân cờ (1 trong số các loại hoặc không) để xác định vị trí có quân cờ hay không
def isOccupied(side, board, pos):
    return getType(side, board, pos) is not None #Nếu hàm getType trả về None, tức là không có quân cờ ở vị trí đó

# Xác định 1 hoặc nhiều ô cờ có quân cờ hay không
def isEmpty(board, *poslist): # *poslist cho phép kiểm tra tùy số lượng ô
    for pos in poslist:
        for side in range(2):
            if isOccupied(side, board, pos): #Nếu ô nào có quân cở, trả về False
                return False
    return True # Ngược lại, nếu ô nào không có quân cờ, trả về True

# Xác định Vua của 1 bên có đang bị chiếu hay không
def isChecked(side, board):
    for piece in board[side]:
        if piece[2] == "k":  # Với quân cờ là Vua
            for i in board[not side]:
                if piece[:2] in rawMoves(not side, board, i): # Nếu vị trí của Vua nằm trong đường đi/ăn của BẤT KỲ quân cờ đối phương
                    return True # Chiếu
            return False # Không chiếu

# Xác định tất cả nước đi HỢP LỆ của 1 người chơi
def legalMoves(side, board, flags):
    for piece in board[side]:
        for pos in availableMoves(side, board, piece, flags): # Tìm nước đi hợp lệ của từng quân
            yield [piece[:2], pos] # Trả về lần lượt quân ở vị trí nào, có thể đi đến ô nào
            
# Xác định trận cờ đã kết thúc hay chưa
def isEnd(side, board, flags):
    for _ in legalMoves(side, board, flags):
        return False # Chưa kết thúc nếu còn tồn tại ít nhất 1 bước đi trên cả bàn cờ
    return True

# Hàm cho phép một quân cờ đi từ vị trí A đến vị trí B, đồng thời xử lý
# việc ăn quân, phong hậu và bắt Tốt qua đường
# Lưu ý: Hàm này biến đổi giá trị chung của biến board
# Có thể dùng hàm copy để lưu lại trạng thái cũ của board (sử dụng cho Undo)
def move(side, board, fro, to, promote="p"):
    UP = 8 if side else 1 # Cuối bàn cờ tương đối với người chơi đang có lượt
    DOWN = 1 if side else 8 # Đầu bàn cờ tương đối với người chơi đang có lượt
    ALLOWENP = fro[1] == 4 + side and to[0] != fro[0] and isEmpty(board, to) # Điều kiện bắt Tốt qua đường
    for piece in board[not side]:
        if piece[:2] == to:
            board[not side].remove(piece) # Ăn quân đối phương ở vị trí đến
            break

    for piece in board[side]:
        if piece[:2] == fro:
            piece[:2] = to # Đi đến ô mới

            if piece[2] == "k": # Nếu là Vua
                if fro[0] - to[0] == 2: # Nhập thành
                    move(side, board, [1, DOWN], [4, DOWN]) # Đổi vị trí của Xe trái
                elif to[0] - fro[0] == 2:
                    move(side, board, [8, DOWN], [6, DOWN]) # Đổi vị trí của Xe phải
                    
            if piece[2] == "p": # Nếu là TỐt
                if to[1] == UP: # Ở cuối bàn cờ
                    board[side].remove(piece)
                    board[side].append([to[0], UP, promote]) # Phong hậu: thay Tốt thành một quân mới
                if ALLOWENP: # Được bắt tốt qua đường
                    board[not side].remove([to[0], fro[1], "p"])
            break
    return board

# Thử để xác định bước đi nào sẽ đưa Vua vào chiếu
def moveTest(side, board, fro, to):
    return not isChecked(side, move(side, copy(board), fro, to))

# Thử để xem bước đi nào sẽ hợp lệ
def isValidMove(side, board, flags, fro, to):
    if 0 < to[0] < 9 and 0 < to[1] < 9 and not isOccupied(side, board, to): # Điểm đến phải trong bàn cờ và là ô trống
        piece = fro + [getType(side, board, fro)] # Xác định thông tin của quân cờ
        if to in rawMoves(side, board, piece, flags):
            return moveTest(side, board, fro, to) # Bước nào đưa Vua vào chiếu sẽ return False, là không hợp lệ

# Hàm này rất quan trọng
# Nó xử lý nước đi, cập nhật flags và xoay màn hình sau mỗi lượt
def makeMove(side, board, fro, to, flags, promote="q"):
    newboard = move(side, copy(board), fro, to, promote)
    newflags = updateFlags(side, newboard, fro, to, flags)
    return not side, newboard, newflags

# Hàm cần được chạy SAU MỖI NƯỚC ĐI, để kiểm tra và cập nhật tất cả flags
# Bao gồm nhập thành và bắt Tốt qua đường
def updateFlags(side, board, fro, to, flags):
    castle = list(flags[0]) # Nhập thành
    if [5, 8, "k"] not in board[0] or [1, 8, "r"] not in board[0]:
        castle[0] = False # Đối phương nhập thành trái
    if [5, 8, "k"] not in board[0] or [8, 8, "r"] not in board[0]:
        castle[1] = False # Đối phương nhập thành phải
    if [5, 1, "k"] not in board[1] or [1, 1, "r"] not in board[1]:
        castle[2] = False # Bản thân nhập thành trái
    if [5, 1, "k"] not in board[1] or [8, 1, "r"] not in board[1]:
        castle[3] = False # Bản thân nhập thành phải

    enP = None # Bắt Tốt qua đường
    if getType(side, board, to) == "p":
        if fro[1] - to[1] == 2:
            enP = [to[0], 6] # Bắt Tốt đối phương
        elif to[1] - fro[1] == 2:
            enP = [to[0], 3] # Đối phương bắt Tốt

    return castle, enP

# Cho trước các giá trị side, board and piece, hàm liệt kê TẤT CẢ nước đi HỢP LỆ của quân cờ
# Hàm này bổ sung/làm wrapper cho rawMoves()
def availableMoves(side, board, piece, flags):
    for i in rawMoves(side, board, piece, flags):
        if 0 < i[0] < 9 and 0 < i[1] < 9 and not isOccupied(side, board, i): # Điểm đến phải trong bàn cờ và là ô trống
            if moveTest(side, board, piece[:2], i):
                yield i # i sẽ là 1 trong các nước đi hợp lệ nếu qua điều kiện trên
    
# Cho trước các giá trị side, board and piece, hàm liệt kê TẤT CẢ nước đi TRONG KHẢ NĂNG của quân cờ
# Nếu có flag, trả về thêm nước đi đặc biệt
# Có tồn tại những nước đi KHÔNG HỢP LỆ trong số những nước đi hàm trả về
# Chỉ dùng trong backend
def rawMoves(side, board, piece, flags=[None, None]):  
    x, y, ptype = piece
    if ptype == "p": # Luật đi của Tốt
        if not side: # Đối phương đi
            if y == 7 and isEmpty(board, [x, 6], [x, 5]): # Đang đứng ở hàng Tốt, trước mặt có 2 ô trống
                yield [x, 5] # Tiến 2 bước
            if isEmpty(board, [x, y - 1]): # Đang đứng ở hàng Tốt, trước mặt có 1 ô trống
                yield [x, y - 1] # Tiến 1 bước
                
            for i in ([x + 1, y - 1], [x - 1, y - 1]): # Nếu có quân của đối phương (theo góc nhìn của đối phương) ở 2 ô chéo trước mặt
                if isOccupied(1, board, i) or flags[1] == i:
                    yield i # Có thể đi
        else: # Bản thân đi
            if y == 2 and isEmpty(board, [x, 3], [x, 4]): # Đang đứng ở hàng Tốt, trước mặt có 2 ô trống
                yield [x, 4] # Tiến 2 bước
            if isEmpty(board, [x, y + 1]): # Đang đứng ở hàng Tốt, trước mặt có 1 ô trống
                yield [x, y + 1]  # Tiến 1 bước

            for i in ([x + 1, y + 1], [x - 1, y + 1]): # Nếu có quân của đối phương ở 2 ô chéo trước mặt
                if isOccupied(0, board, i) or flags[1] == i:
                    yield i # Có thể đi

    elif ptype == "n": # Luật đi của Mã
        yield from (
            [x + 1, y + 2], [x + 1, y - 2], [x - 1, y + 2], [x - 1, y - 2],
            [x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1]
        ) # Điểm đến là đuôi chữ L tính từ vị trí của Mã

    elif ptype == "b": # Luật đi của Tượng
        for i in range(1, 8):
            yield [x + i, y + i] # Chéo lên, sang phải
            if not isEmpty(board, [x + i, y + i]):
                break # Dừng khi có vật cản trên đường đi
        for i in range(1, 8):
            yield [x + i, y - i] # Chéo xuống, sang phải
            if not isEmpty(board, [x + i, y - i]):
                break
        for i in range(1, 8):
            yield [x - i, y + i] # Chéo lên, sang trái
            if not isEmpty(board, [x - i, y + i]):
                break
        for i in range(1, 8):
            yield [x - i, y - i] # Chéo xuống, sang trái
            if not isEmpty(board, [x - i, y - i]):
                break

    elif ptype == "r": # Luật đi của Xe
        for i in range(1, 8):
            yield [x + i, y] # Sang phải
            if not isEmpty(board, [x + i, y]):
                break # Dừng khi có vật cản trên đường đi
        for i in range(1, 8):
            yield [x - i, y] # Sang trái
            if not isEmpty(board, [x - i, y]):
                break
        for i in range(1, 8):
            yield [x, y + i] # Đi thẳng
            if not isEmpty(board, [x, y + i]):
                break
        for i in range(1, 8):
            yield [x, y - i] # Đi lùi
            if not isEmpty(board, [x, y - i]):
                break

    elif ptype == "q": # Luật đi của Hậu
        yield from rawMoves(side, board, [x, y, "b"]) # Thừa hưởng luật đi của Tượng
        yield from rawMoves(side, board, [x, y, "r"]) # và của Xe

    elif ptype == "k": # Luật đi của Vua
        if flags[0] is not None and not isChecked(side, board): # Trong điều kiện có thể nhập thành và không bị chiếu
            if flags[0][0] and isEmpty(board, [2, 8], [3, 8], [4, 8]): # Phải có ô trống giữa Vua và Xe (đối phương)
                if moveTest(0, board, [5, 8], [4, 8]): # Nếu bước đi này không đưa Vua vào chiếu
                    yield [3, 8] # Nhập thành trái
            if flags[0][1] and isEmpty(board, [6, 8], [7, 8]):
                if moveTest(0, board, [5, 8], [6, 8]):
                    yield [7, 8] # Nhập thành phải
            if flags[0][2] and isEmpty(board, [2, 1], [3, 1], [4, 1]): # Điều kiện cho bản thân
                if moveTest(1, board, [5, 1], [4, 1]):
                    yield [3, 1] # Nhập thành trái
            if flags[0][3] and isEmpty(board, [6, 1], [7, 1]):
                if moveTest(1, board, [5, 1], [6, 1]):
                    yield [7, 1] # Nhập thành phải

        yield from (
            [x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x - 1, y],
            [x - 1, y + 1], [x, y + 1], [x + 1, y + 1], [x + 1, y]
        ) # Đi 1 ô về 8 hướng xung quanh