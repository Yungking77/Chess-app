import chess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from backend import ChessGame

# Unicode symbols for rendering clean chess pieces without external images
UNICODE_PIECES = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
}

class ChessSquare(Button):
    def __init__(self, square_id, is_light, **kwargs):
        super().__init__(**kwargs)
        self.square_id = square_id  # Integer 0..63
        self.square_name = chess.square_name(square_id)  # e.g. "e2"
        self.is_light = is_light
        
        # Board theme colors (RGBA)
        self.light_color = (0.94, 0.85, 0.71, 1)   # Classic light beige
        self.dark_color = (0.71, 0.53, 0.39, 1)    # Classic dark wood
        self.selected_color = (0.96, 0.96, 0.41, 1)# Highlight yellow
        
        self.background_normal = ''
        self.font_size = '36sp'
        self.reset_color()

    def reset_color(self):
        self.background_color = self.light_color if self.is_light else self.dark_color

    def highlight(self):
        self.background_color = self.selected_color


class ChessUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.game = ChessGame()
        self.selected_square = None
        self.squares_dict = {}

        # 1. Top status label
        self.status_label = Label(
            text=self.game.get_game_status(),
            size_hint_y=0.1,
            font_size='20sp',
            bold=True
        )
        self.add_widget(self.status_label)

        # 2. 8x8 Board Grid
        self.board_grid = GridLayout(cols=8, size_hint_y=0.8)
        self.create_board()
        self.add_widget(self.board_grid)

        # 3. Bottom controls
        controls = BoxLayout(size_hint_y=0.1, padding=10, spacing=10)
        reset_btn = Button(text="New Game", font_size='18sp')
        reset_btn.bind(on_press=self.reset_game)
        controls.add_widget(reset_btn)
        self.add_widget(controls)

        self.update_board_ui()

    def create_board(self):
        # Create squares rank by rank from 8 down to 1
        for row in range(7, -1, -1):
            for col in range(8):
                sq_id = row * 8 + col
                is_light = (row + col) % 2 != 0
                btn = ChessSquare(square_id=sq_id, is_light=is_light)
                btn.bind(on_press=self.on_square_click)
                self.squares_dict[sq_id] = btn
                self.board_grid.add_widget(btn)

    def update_board_ui(self):
        """Reads current state from backend and updates piece icons."""
        for sq_id, btn in self.squares_dict.items():
            piece = self.game.board.piece_at(sq_id)
            if piece:
                btn.text = UNICODE_PIECES.get(piece.symbol(), '')
                # Dark text for black pieces, bright text for white pieces
                btn.color = (0.1, 0.1, 0.1, 1) if piece.color == chess.BLACK else (1, 1, 1, 1)
            else:
                btn.text = ''

    def on_square_click(self, instance):
        if self.selected_square is None:
            # First tap: Select piece
            piece = self.game.board.piece_at(instance.square_id)
            if piece and piece.color == self.game.board.turn:
                self.selected_square = instance
                instance.highlight()
        else:
            # Second tap: Target square move attempt
            from_sq = self.selected_square.square_name
            to_sq = instance.square_name
            move_uci = f"{from_sq}{to_sq}"

            # Auto-promote pawn to Queen when reaching last rank
            piece = self.game.board.piece_at(self.selected_square.square_id)
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and instance.square_id >= 56) or \
                   (piece.color == chess.BLACK and instance.square_id <= 7):
                    move_uci += "q"

            # Execute move via backend logic
            success, message = self.game.make_move(move_uci)

            # Reset selection highlight
            self.selected_square.reset_color()
            self.selected_square = None

            if success:
                self.update_board_ui()
                self.status_label.text = self.game.get_game_status()
            else:
                self.status_label.text = f"Invalid move! {self.game.get_game_status()}"

    def reset_game(self, instance):
        self.game = ChessGame()
        if self.selected_square:
            self.selected_square.reset_color()
            self.selected_square = None
        self.update_board_ui()
        self.status_label.text = self.game.get_game_status()


class ChessApp(App):
    def build(self):
        return ChessUI()

if __name__ == '__main__':
    ChessApp().run()
