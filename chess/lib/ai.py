from chess.lib.core import legalMoves, makeMove
from chess.lib.heuristics import *

INF = 1000000  # Tượng trưng cho một giá trị cực lớn (infinity)
DEPTH = 2  # Số lượng lượt đi trong tương lai mà hàm minimax sẽ tính toán và dự đoán

# Hàm này gán một giá trị cho mỗi loại quân cờ dựa trên vị trí của nó trên bàn cờ, từ đó biết được tình thế hiện tại
# cuả bàn cờ qua một con số cụ thể
def evaluate(board):
    score = 0
    for x, y, piece in board[0]:
        if piece == "p":
            score += 1 + pawnEvalWhite[y - 1][x - 1]
        elif piece == "b":
            score += 9 + bishopEvalWhite[y - 1][x - 1]
        elif piece == "n":
            score += 9 + knightEval[y - 1][x - 1]
        elif piece == "r":
            score += 14 + rookEvalWhite[y - 1][x - 1]
        elif piece == "q":
            score += 25 + queenEval[y - 1][x - 1]
        elif piece == "k":
            score += 200 + kingEvalWhite[y - 1][x - 1]

    for x, y, piece in board[1]:
        if piece == "p":
            score -= 1 + pawnEvalBlack[y - 1][x - 1]
        elif piece == "b":
            score -= 9 + bishopEvalBlack[y - 1][x - 1]
        elif piece == "n":
            score -= 9 + knightEval[y - 1][x - 1]
        elif piece == "r":
            score -= 14 + rookEvalBlack[y - 1][x - 1]
        elif piece == "q":
            score -= 25 + queenEval[y - 1][x - 1]
        elif piece == "k":
            score -= 200 + kingEvalBlack[y - 1][x - 1]
    return score

# Hàm xử lý các nước đi tiếp theo của AI (bot), dựa trên recursion, bằng cách liệt kê tất cả các nước tiếp theo có thể
# (legalMoves) của cả AI và người chơi theo tổng {depth} lượt tiếp theo, evaluate cả bàn cờ dựa theo mỗi nước đi từ đó
# chọn ra nước đi có lợi nhất cho AI - bất lợi nhất cho người chơi. Mục đích của hàm này là chọn các nước đi có thể
# maximize số điểm của AI (bot), và minimize số điểm của người chơi qua evaluate(board)
def miniMax(side, board, flags, depth=DEPTH, alpha=-INF, beta=INF):
    if depth == 0:
        return evaluate(board)  # khởi động thuật toán (depth == 0) bằng cách evaluate tất cả các quân cờ còn lại
                                # hiện tại trên bàn và gán giá trị cho chúng

    if not side: # tính toán các lượt có thể của AI (bot), hay còn gọi là maximizing player trong minimax algorithm
        bestVal = -INF # -infinity được coi là biến trung gian để so sánh tìm điểm max
        for fro, to in legalMoves(side, board, flags):
            movedata = makeMove(side, board, fro, to, flags)
            nodeVal = miniMax(*movedata, depth - 1, alpha, beta) # nodeVal: best_move của mỗi trường hợp con trong legalMoves
            if nodeVal > bestVal:  # tìm giá trị lớn nhất - nước đi có lợi nhất cho AI
                bestVal = nodeVal
                if depth == DEPTH:
                    bestMove = (fro, to)
            alpha = max(alpha, bestVal)  # alpha-beta pruning, một thuật toán dùng để rút gọn số lượng các phép tính phải
                                         # làm qua việc loại bỏ các trường hợp con mà thuật toán tính ra có thể bị loại
                                         # bỏ từ trường hợp mẹ
            if alpha >= beta:
                break

    else:  # tính toán các lượt có thể của người chơi, hay còn gọi là minimizing player trong minimax algorithm
        bestVal = INF  # infinity được coi là biến trung gian để so sánh tìm điểm min
        for fro, to in legalMoves(side, board, flags):
            movedata = makeMove(side, board, fro, to, flags)
            nodeVal = miniMax(*movedata, depth - 1, alpha, beta)
            if nodeVal < bestVal:  # tìm giá trị nhỏ nhất - nước đi bất lợi nhất cho người chơi
                bestVal = nodeVal
                if depth == DEPTH:
                    bestMove = (fro, to)
            beta = min(beta, bestVal)
            if alpha >= beta:
                break

    if depth == DEPTH:
        return bestMove  # khi depth == DEPTH, vòng lặp đã chạy đủ số lượt yêu cầu và trả lại nước đi tối ưu nhất đã tính
    else:
        return bestVal  # giá trị nước đi tối ưu sau mỗi vòng lặp maximize hoặc minimize
