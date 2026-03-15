from game.game_state import GameState
import pygame
import chess

class Sounds:
    def __init__(self, game):
        pygame.mixer.init()
        self.game = game
        self.enabled = True
        self.last_move_count = 0

        self.sounds = {
            "move": pygame.mixer.Sound("python-chess/ui/assets/sounds/Move.wav"),
            "check": pygame.mixer.Sound("python-chess/ui/assets/sounds/Check.wav"),
            "capture": pygame.mixer.Sound("python-chess/ui/assets/sounds/Capture.wav"),
            # "checkmate": pygame.mixer.Sound("python-chess/ui/assets/sounds/Checkmate.wav"),
            "castle": pygame.mixer.Sound("python-chess/ui/assets/sounds/Castle.wav"),
            "promotion": pygame.mixer.Sound("python-chess/ui/assets/sounds/Promote.wav"),
            "game_over": pygame.mixer.Sound("python-chess/ui/assets/sounds/Game-end.wav")
        }

    def play_move_sound(self):
        if self.enabled == True:
            if not self.game.board.move_stack:
                return
            
            current_move_count = len(self.game.board.move_stack)
            if current_move_count == self.last_move_count:
                return
            
            self.last_move_count = current_move_count

            is_mate = self.game.board.is_checkmate()
            is_check = self.game.board.is_check()
            is_promotion = self.game.is_last_move_promotion()
            game_over = self.game.board.is_checkmate() or self.game.board.is_stalemate()
            #add stalemate sound later

            last_move = self.game.board.pop() 
            
            is_capture = self.game.board.is_capture(last_move)
            is_castle = self.game.board.is_castling(last_move)
            
            self.game.board.push(last_move)

            if is_mate:
                sound_key = "game_over"
            elif is_promotion:
                sound_key = "promotion"
            elif is_check:
                sound_key = "check"
            elif is_capture:
                sound_key = "capture"
            elif is_castle:
                sound_key = "castle"
            else:
                sound_key = "move"

            print(f"DEBUG: sound: {sound_key}")
            try:
                if sound_key in self.sounds:
                    self.sounds[sound_key].play()
            except Exception as e:
                print(f"Помилка відтворення: {e}")

    def stop_all_sounds(self):
        if self.enabled == False:
            pygame.mixer.stop()
            print("DEBUG: all sounds stopped")