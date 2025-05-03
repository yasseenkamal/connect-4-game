#  الموديول دوره نقطة الدخول لتشغيل اللعبة كاملة
import sys, random                        #  النظام والعشوائي
import pygame                             #  Pygame لحلقة الأحداث
from constants import *                   #  كل الثوابت
from game import Game                     #  منطق اللعبة
from ui import UI                         #  واجهة المستخدم

if __name__ == "__main__":              # التشغيلةلما اجي انفذ
    mode = None                           # بيجهز الوضع
    while mode not in ("1", "2"):      # بيطلب انهي جيم عايز العبه
        mode = input("Select mode: [1] Human vs. Human, [2] Human vs. AI  ")
    human_vs_human = (mode == "1")       

    while True:                           # لوب إعادة التشغيل
        game = Game(depth=5)              # بيجهز مثال للعبة
        ui = UI(game.board)               # بيعمل واجهة المستخدم
        game_over, turn = False, PLAYER_PIECE  # بيجهز الحالة

        ui.draw()                         # الرسم الأولي

        while not game_over:             # لوب الرئيسية
            ui.screen.fill(BLACK, (0, 0, ui.width, ui.square))  # مسح الشريط اللي فوق
            msg = ("Player 1's turn" if turn == PLAYER_PIECE else "Player 2's turn")  # الرسالة
            colr = (RED if turn==PLAYER_PIECE else YELLOW)   # اللون
            label = ui.font_turn.render(msg, True, colr)     # إنشاء النص
            ui.screen.blit(label, (40, 10))                 # رسم النص
            pygame.display.update((0, 0, ui.width, ui.square))  # بيحث المنطقة

            for event in pygame.event.get():  # بيستعرض الأحداث
                if event.type == pygame.QUIT: sys.exit()    #بينهي لما يقفل 

                if event.type == pygame.MOUSEBUTTONDOWN:   # لما تدوس بالماوس
                    col = event.pos[0] // SQUARESIZE       # حساب العمود
                    if turn == PLAYER_PIECE or human_vs_human:
                        win, err = game.make_move(col)     # تنفيذ الحركة
                        if not err:                        # إذا صالحة
                            ui.draw()                     # إعادة الرسم
                            if win:                       # إذا فوز
                                ui.show_winner(turn)      # عرض الفائز
                                game_over = True          # إنهاء لوب
                            else:
                                turn = AI_PIECE if turn==PLAYER_PIECE else PLAYER_PIECE  # تبديل

            if not human_vs_human and turn == AI_PIECE and not game_over:  # دور computer
                win = game.play_ai()              # حركة computer
                ui.draw()                         # إعادة الرسم
                if win:                           # لو فوز
                    ui.show_winner(AI_PIECE)     # عرض الفائز
                    game_over = True
                else:
                    turn = PLAYER_PIECE          # بيبدل

        # مطالبة ما بعد اللعبة
        prompt = ui.font_turn.render("Press R to restart or Q to quit", True, (200,200,200))  # النص
        ui.screen.blit(prompt, (40, ui.height//2 - 10))  # رسم النص
        pygame.display.update()                           # تحديث

        decision = None
        while decision not in ("R", "Q"):              # انتظار الإدخال
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT: sys.exit()     # إنهاء
                if evt.type == pygame.KEYDOWN:             # الضغط على مفتاح
                    if evt.key == pygame.K_r: decision = "R"  # إعادة تشغيل
                    elif evt.key == pygame.K_q: decision = "Q"  # خروج
        if decision == "Q": sys.exit()                   # إنهاء
        # وإلا تعاد لوب    	
