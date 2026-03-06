from game.game_state import GameState
import pygame

class Sounds:
    def __init__(self, game):
        pygame.mixer.init()
        self.game = game

        self.sounds = {
            "move": pygame.mixer.Sound("python-chess/ui/assets/sounds/Move.wav"),
            "check": pygame.mixer.Sound("python-chess/ui/assets/sounds/Check.wav"),
            "capture": pygame.mixer.Sound("python-chess/ui/assets/sounds/Capture.wav"),
            # "checkmate": pygame.mixer.Sound("python-chess/ui/assets/sounds/Checkmate.wav"),
            "castle": pygame.mixer.Sound("python-chess/ui/assets/sounds/Castle.wav"),
            # "promotion": pygame.mixer.Sound("python-chess/ui/assets/sounds/Promotion.wav"), #will add
            # "game_over": pygame.mixer.Sound("python-chess/ui/assets/sounds/GameOver.wav")
        }

    def play_move_sound(self):
        if not self.game.board.move_stack:
            return
        
        # 1. Спершу перевіряємо ШАХ та МАТ (це треба робити на актуальній дошці)
        is_mate = self.game.board.is_checkmate()
        is_check = self.game.board.is_check()
        
        # 2. А тепер перевіряємо ВЗЯТТЯ та РОКИРОВКУ
        # Для цього ми тимчасово забираємо останній хід з дошки
        last_move = self.game.board.pop() 
        
        # Тепер дошка в стані "ДО ходу", і ми можемо чесно запитати, чи був хід взяттям
        is_capture = self.game.board.is_capture(last_move)
        is_castle = self.game.board.is_castling(last_move)
        
        # Повертаємо хід назад на дошку, щоб нічого не зламати
        self.game.board.push(last_move)

        # 3. Визначаємо ключ звуку за пріоритетом
        if is_mate:
            sound_key = "game_over"
        elif is_check:
            sound_key = "check"
        elif is_capture:
            sound_key = "capture"
        elif is_castle:
            sound_key = "castle"
        else:
            sound_key = "move"

        # 4. Програємо звук
        print(f"DEBUG: sound: {sound_key}")
        try:
            if sound_key in self.sounds:
                self.sounds[sound_key].play()
        except Exception as e:
            print(f"Помилка відтворення: {e}")