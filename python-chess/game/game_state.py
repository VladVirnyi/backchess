import chess

class GameState:
    def __init__(self):
        self.board = chess.Board()

    def if_legal_move(self, from_sq, to_sq):
        move = chess.Move(from_sq, to_sq)
        return move in self.board.legal_moves
    
    def is_promotion(self, from_sq, to_sq):
        piece = self.board.piece_at(from_sq)
        if not piece or piece.piece_type != chess.PAWN:
            return False

        if piece.color == chess.WHITE and chess.square_rank(to_sq) == 7 and chess.square_rank(from_sq) == 6:
            return True
        if piece.color == chess.BLACK and chess.square_rank(to_sq) == 0 and chess.square_rank(from_sq) == 1:
            return True
            
        return False

    def is_last_move_promotion(self):
        if not self.board.move_stack:
            return False
        return self.board.move_stack[-1].promotion is not None
    
    def make_move(self, from_sq, to_sq, promotion=None):
        if promotion:
            move = chess.Move(from_sq, to_sq, promotion=promotion)
        else:
            move = chess.Move(from_sq, to_sq)

        if move in self.board.legal_moves:
            self.board.push(move)
            return True

        return False

    def status(self):
        if self.board.is_checkmate():
            return "Checkmate"
        if self.board.is_stalemate():
            return "Stalemate"
        if self.board.is_check():
            return "Check"
