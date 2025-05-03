# هذا الموديول يحتوي على فئة Game لإدارة منطق اللعب وأدوار اللاعبين
from board import Board           # استيراد Board لعمليات الشبكة
from ai import MinimaxAI         # استيراد AI لحركات الكمبيوتر
from constants import PLAYER_PIECE, AI_PIECE  # استيراد معرفات اللاعبين

class Game:
    def __init__(self, depth=5):  # تهيئة لعبة جديدة
        self.board = Board()       # إنشاء مثيل للوحة
        self.current_turn = PLAYER_PIECE  # البدء بلاعب بشري
        self.ai = MinimaxAI(depth)        # إنشاء AI مع عمق البحث

    def switch_turn(self):         # تبديل الدور الحالي
        self.current_turn = (AI_PIECE if self.current_turn == PLAYER_PIECE  
                              else PLAYER_PIECE)  # تبديل اللاعبين

    def validate_move(self, col):  # التحقق من صحة الإدخال
        try:
            c = int(col)          # التحويل إلى عدد صحيح
        except ValueError:
            return False          # إدخال غير صالح
        return self.board.is_valid_location(c)  # التحقق من مساحة اللوحة

    def make_move(self, col):     # تنفيذ حركة اللاعب
        if not self.validate_move(col):      # إدخال غير صالح
            return False, "Invalid move. Choose another column."  # خطأ
        c = int(col)                        # التحويل إلى عدد صحيح
        self.board.drop_piece(c, self.current_turn)  # إسقاط القطعة
        won = self.board.winning_move(self.current_turn)  # التحقق من الفوز
        return won, None                   # إرجاع النتيجة

    def play_ai(self):            # قيام الذكاء الاصطناعي بحركة
        c = self.ai.get_best_move(self.board)  # اختيار العمود بواسطة AI
        self.board.drop_piece(c, self.current_turn)  # إسقاط قطعة AI
        return self.board.winning_move(self.current_turn)  # إرجاع علم الفوز
