#  الموديول يحتوي على فئة Board ومنطق الشبكة

import numpy as np            #  NumPy لمعالجة المصفوفات
from constants import ROWS, COLS  #  أبعاد الشبكة

class Board:
    def __init__(self, rows=ROWS, cols=COLS):  # تهيئة الأبعاد
        self.rows, self.cols = rows, cols       # تخزين عدد الصفوف والأعمدة
        self.grid = np.zeros((rows, cols), dtype=int)  # إنشاء شبكة ثنائية الأبعاد فارغة

    def drop_piece(self, col, piece):         # إسقاط قطعة في عمود
        """وضع القطعة في أول خلية فارغة في العمود المحدد."""
        if not (0 <= col < self.cols) or self.grid[0, col] != 0:  # عمود غير صالح أو ممتلئ
            raise ValueError(f"العمود {col} غير صالح أو ممتلئ")      # رمي خطأ
        for r in range(self.rows - 1, -1, -1):  # من الصف السفلي إلى الأعلى
            if self.grid[r, col] == 0:          # إذا كانت الخلية فارغة
                self.grid[r, col] = piece      # وضع القطعة
                return                          # الخروج بعد الوضع

    def is_valid_location(self, col):         # التحقق إذا كان يمكن وضع قطعة في العمود
        return 0 <= col < self.cols and self.grid[0, col] == 0  # الخلية العلوية فارغة

    def get_valid_locations(self):            # قائمة الأعمدة غير الممتلئة
        return [c for c in range(self.cols) if self.is_valid_location(c)]  # ترشيح الأعمدة

    def winning_move(self, piece):            # التحقق من أي أربعة على التوالي للقطعة
        # فحص أفقي
        for r in range(self.rows):            # لكل صف
            for c in range(self.cols - 3):    # لكل عمود بداية
                if all(self.grid[r, c + i] == piece for i in range(4)):  # أربعة أفقيًا
                    return True                # فوز

        # فحص عمودي
        for c in range(self.cols):            # لكل عمود
            for r in range(self.rows - 3):    # لكل صف بداية
                if all(self.grid[r + i, c] == piece for i in range(4)):  # أربعة عموديًا
                    return True

        # فحص القطر الإيجابي
        for r in range(self.rows - 3):        # للقطر الصاعد
            for c in range(self.cols - 3):    # لكل بداية
                if all(self.grid[r + i, c + i] == piece for i in range(4)):  # قطري \
                    return True

        # فحص القطر السلبي
        for r in range(3, self.rows):        # للقطر الهابط
            for c in range(self.cols - 3):    # لكل بداية
                if all(self.grid[r - i, c + i] == piece for i in range(4)):  # قطري /
                    return True

        return False                           # لا فوز
