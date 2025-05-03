#  الموديول يحتوي على واجهة المستخدم باستخدام Pygame
import pygame                           
from constants import BLUE, BLACK, RED, YELLOW, WIDTH, HEIGHT, SQUARESIZE, RADIUS
from constants import PLAYER_PIECE, AI_PIECE  #  معرفات اللاعبين

class UI:
    def __init__(self, board):        # تهيئة واجهة Pygame
        pygame.init()                   # بدء وحدات Pygame
        pygame.font.init()              # تهيئة نظام الخطوط
        self.board = board             # تخزين مرجع اللوحة
        self.width, self.height = WIDTH, HEIGHT  # أبعاد النافذة
        self.square = SQUARESIZE       # حجم مربع الشبكة
        self.radius = RADIUS           # نصف قطر القطع
        self.screen = pygame.display.set_mode((self.width, self.height))  # إنشاء النافذة
        self.font_main = pygame.font.SysFont("monospace", 75)         # الخط الكبير
        self.font_turn = pygame.font.SysFont("monospace", 36)         # الخط الصغير

    def draw(self):                    # رسم اللوحة في كل إطار
        for c in range(self.board.cols):
            for r in range(self.board.rows):
                pygame.draw.rect(
                    self.screen, BLUE,
                    (c*self.square, r*self.square + self.square, self.square, self.square)
                )                   # رسم خلية الشبكة
                color = BLACK        # افتراضيًا فارغة
                if self.board.grid[r, c] == PLAYER_PIECE: color = RED   # قطعة اللاعب
                if self.board.grid[r, c] == AI_PIECE:     color = YELLOW  # قطعة AI
                pygame.draw.circle(
                    self.screen, color,
                    (c*self.square + self.square//2, r*self.square + self.square + self.square//2),
                    self.radius
                )                   # رسم القطعة
        pygame.display.update()      # تحديث العرض

    def show_winner(self, piece):      # عرض رسالة الفائز
        text = "PLAYER 1 WINS!" if piece == PLAYER_PIECE else "PLAYER 2 WINS!"  # الرسالة
        col  = RED if piece == PLAYER_PIECE else YELLOW    # لون النص
        label = self.font_main.render(text, True, col)     # إنشاء النص
        self.screen.blit(label, (40, 10))                  # رسم النص
        pygame.display.update()                            # تحديث العرض
