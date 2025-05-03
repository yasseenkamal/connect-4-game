# هذا الموديول يحتوي على خوارزمية MinimaxAI مع α–β pruning
import math, random               # استيراد math لللانهاية، وrandom للتعادل
from board import Board            # نسخ حالات اللوحة
from constants import PLAYER_PIECE, AI_PIECE  # استيراد معرفات اللاعبين

class MinimaxAI:
    def __init__(self, depth):     # تهيئة عمق البحث
        self.depth = depth         # تخزين حد العمق

    def score_window(self, window, piece):  # دالة تقييم نافذة من 4 خانات
        score = 0                   # الدرجة الأساسية
        opp = (PLAYER_PIECE if piece == AI_PIECE else AI_PIECE)  # الخصم
        if window.count(piece) == 4:       score += 100         # فوز
        elif window.count(piece) == 3 and window.count(0) == 1: score += 5  # جيد
        elif window.count(piece) == 2 and window.count(0) == 2: score += 2  # مقبول
        if window.count(opp) == 3 and window.count(0) == 1:     score -= 4  # منع
        return score                 # إرجاع نتيجة النافذة

    def evaluate(self, board, piece):  # تقييم اللوحة الكاملة
        score = 0                   # مجموع الدرجات
        center = list(board.grid[:, board.cols//2])  # عمود المركز
        score += center.count(piece) * 6  # تفضيل المركز
        # أفقي
        for r in range(board.rows):
            row = list(board.grid[r, :])
            for c in range(board.cols - 3):
                score += self.score_window(row[c:c+4], piece)
        # عمودي
        for c in range(board.cols):
            col = list(board.grid[:, c])
            for r in range(board.rows - 3):
                score += self.score_window(col[r:r+4], piece)
        # قطر إيجابي
        for r in range(board.rows - 3):
            for c in range(board.cols - 3):
                window = [board.grid[r+i][c+i] for i in range(4)]
                score += self.score_window(window, piece)
        # قطر سلبي
        for r in range(3, board.rows):
            for c in range(board.cols - 3):
                window = [board.grid[r-i][c+i] for i in range(4)]
                score += self.score_window(window, piece)
        return score                 # إرجاع المجموع الكلي

    def is_terminal(self, board):   # التحقق من حالة النهاية
        return (board.winning_move(PLAYER_PIECE)    # فوز بشري؟
                or board.winning_move(AI_PIECE)     # فوز AI؟
                or not board.get_valid_locations())  # لا حركات

    def minimax(self, board, depth, alpha, beta, maximizing):  # البحث التكراري
        valid = board.get_valid_locations()  # الحركات المتاحة
        terminal = self.is_terminal(board)   # التحقق من النهاية
        if depth == 0 or terminal:
            if terminal:
                if board.winning_move(AI_PIECE):    return (None, math.inf)
                if board.winning_move(PLAYER_PIECE): return (None, -math.inf)
                return (None, 0)          # تعادل
            return (None, self.evaluate(board, AI_PIECE))  # حد العمق
        if maximizing:
            value, column = -math.inf, random.choice(valid)  # تهيئة
            for col in valid:
                b_copy = Board(board.rows, board.cols)  # نسخ اللوحة
                b_copy.grid = board.grid.copy()
                b_copy.drop_piece(col, AI_PIECE)        # محاكاة حركة
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:                  # أفضل
                    value, column = new_score, col
                alpha = max(alpha, value)              # تحديث α
                if alpha >= beta: break                # قطع
            return column, value
        else:
            value, column = math.inf, random.choice(valid)
            for col in valid:
                b_copy = Board(board.rows, board.cols)
                b_copy.grid = board.grid.copy()
                b_copy.drop_piece(col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value, column = new_score, col
                beta = min(beta, value)
                if alpha >= beta: break                # قطع
            return column, value

    def get_best_move(self, board):      # الحصول على أفضل عمود
        col, _ = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return col                     # إرجاع العمود المختار
