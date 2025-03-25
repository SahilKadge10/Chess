import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
import os
import io
import chess

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess with AI")

        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack()

        self.board = chess.Board()  # Create chess board
        self.load_images()  # Load chess piece images
        self.draw_board()  # Draw board and pieces

        self.selected_piece = None  # Track selected piece

        # Bind mouse events for clicking and releasing
        self.canvas.bind("<Button-1>", self.on_piece_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_piece_release)

    def load_images(self):
        self.images = {}
        piece_types = ["wK", "wQ", "wR", "wB", "wN", "wP", "bK", "bQ", "bR", "bB", "bN", "bP"]
        
        for piece in piece_types:
            path = os.path.join("pieces", f"{piece}.svg")  # Ensure correct path
            if os.path.exists(path):  
                png_data = cairosvg.svg2png(url=path)  # Convert SVG to PNG
                image = Image.open(io.BytesIO(png_data)).resize((60, 60))
                self.images[piece] = ImageTk.PhotoImage(image)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#EEEED2", "#769656"]

        # Draw chessboard with White at the bottom
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1, y1 = col * 60, (7 - row) * 60  # Flip row for correct orientation
                x2, y2 = x1 + 60, y1 + 60
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw pieces
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, 8)
            piece_symbol = piece.symbol()
            piece_code = f"{'w' if piece_symbol.isupper() else 'b'}{piece_symbol.upper()}"

            if piece_code in self.images:
                x, y = col * 60 + 30, (7 - row) * 60 + 30  # Flip row for correct orientation
                self.canvas.create_image(x, y, image=self.images[piece_code], tags=("piece",))

    def on_piece_click(self, event):
        """Handles selecting a piece"""
        col, row = event.x // 60, 7 - (event.y // 60)  # Flip row to match chess library
        square = chess.square(col, row)
        piece = self.board.piece_at(square)

        if piece:
            self.selected_piece = square  # Store selected piece position

    def on_piece_release(self, event):
        """Handles moving a piece to a new position"""
        if self.selected_piece is None:
            return

        col, row = event.x // 60, 7 - (event.y // 60)  # Flip row to match chess library
        target_square = chess.square(col, row)

        move = chess.Move(self.selected_piece, target_square)
        if move in self.board.legal_moves:
            self.board.push(move)
            self.draw_board()  # Redraw board with updated positions

        self.selected_piece = None  # Reset selection

if __name__ == "__main__":
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
