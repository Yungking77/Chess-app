import chess

class ChessGame:
    def __init__(self):
        # Initializes a standard starting board
        self.board = chess.Board()
        
    def get_legal_moves(self):
        """Returns a list of all legal moves for the current position."""
        return [move.uci() for move in self.board.legal_moves]

    def make_move(self, move_str):
        """Takes a move string like 'e2e4' and applies it if legal."""
        try:
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True, "Move successful"
            return False, "Illegal move"
        except ValueError:
            return False, "Invalid notation"

    def get_game_status(self):
        """Checks if the game is over and returns the state."""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            return f"Checkmate! {winner} wins."
        if self.board.is_stalemate():
            return "Draw by stalemate."
        if self.board.is_check():
            return "Check!"
        
        turn = "White" if self.board.turn else "Black"
        return f"{turn}'s turn"

# Quick test to ensure the backend works
if __name__ == "__main__":
    game = ChessGame()
    print("Game initialized:", game.get_game_status())
    print("Attempting e2e4:", game.make_move("e2e4")[1])
    print("Status now:", game.get_game_status())
