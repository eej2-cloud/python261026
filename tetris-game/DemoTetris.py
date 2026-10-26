import random
import tkinter as tk


CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(0, 0), (1, 0), (2, 0), (1, 1)],  # T
    [(0, 0), (1, 0), (2, 0), (2, 1)],  # L
    [(0, 0), (1, 0), (1, 1), (1, 2)],  # J
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
]

COLORS = ["yellow", "purple", "orange", "blue", "cyan", "green", "red"]


class Piece:
    def __init__(self):
        index = random.randrange(len(SHAPES))
        self.shape = list(SHAPES[index])
        self.color = COLORS[index]
        self.x = 3
        self.y = 0

    def cells(self):
        return [(self.x + dx, self.y + dy) for dx, dy in self.shape]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        rotated = [(-dy, dx) for dx, dy in self.shape]
        min_x = min(x for x, _ in rotated)
        min_y = min(y for _, y in rotated)
        self.shape = [(x - min_x, y - min_y) for x, y in rotated]


class Tetris:
    def __init__(self, master):
        self.master = master
        self.master.title("Tetris")
        self.canvas = tk.Canvas(
            master,
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bg="black",
        )
        self.canvas.pack()

        self.score = 0
        self.board = [[None] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.game_over = False
        self.current_piece = Piece()

        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Up>", self.rotate_piece)

        if self.check_collision(self.current_piece):
            self.game_over = True

        self.update()

    def check_collision(self, piece):
        for x, y in piece.cells():
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return True
            if y >= 0 and self.board[y][x] is not None:
                return True
        return False

    def merge_piece(self):
        for x, y in self.current_piece.cells():
            if y < 0:
                self.game_over = True
                return
            self.board[y][x] = self.current_piece.color

        self.clear_lines()
        self.current_piece = Piece()

        if self.check_collision(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        remaining = [row for row in self.board if not all(row)]
        cleared = BOARD_HEIGHT - len(remaining)

        if cleared:
            self.board = [[None] * BOARD_WIDTH for _ in range(cleared)] + remaining
            self.score += cleared * 100

    def move_left(self, event=None):
        self.try_move(-1, 0)

    def move_right(self, event=None):
        self.try_move(1, 0)

    def move_down(self, event=None):
        if self.game_over:
            return

        self.current_piece.move(0, 1)
        if self.check_collision(self.current_piece):
            self.current_piece.move(0, -1)
            self.merge_piece()

    def try_move(self, dx, dy):
        if self.game_over:
            return

        self.current_piece.move(dx, dy)
        if self.check_collision(self.current_piece):
            self.current_piece.move(-dx, -dy)

    def rotate_piece(self, event=None):
        if self.game_over:
            return

        old_shape = self.current_piece.shape[:]
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = old_shape

    def update(self):
        if not self.game_over:
            self.current_piece.move(0, 1)
            if self.check_collision(self.current_piece):
                self.current_piece.move(0, -1)
                self.merge_piece()

        self.draw()
        if not self.game_over:
            self.master.after(500, self.update)

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        self.canvas.create_rectangle(
            x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
            fill=color, outline="gray",
        )

    def draw(self):
        self.canvas.delete("all")

        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                if color is not None:
                    self.draw_cell(x, y, color)

        if not self.game_over:
            for x, y in self.current_piece.cells():
                if y >= 0:
                    self.draw_cell(x, y, self.current_piece.color)

        self.canvas.create_text(
            5, 5, anchor="nw", fill="white",
            text=f"점수: {self.score}",
        )

        if self.game_over:
            self.canvas.create_text(
                BOARD_WIDTH * CELL_SIZE // 2,
                BOARD_HEIGHT * CELL_SIZE // 2,
                text="게임 종료",
                fill="red",
                font=("Arial", 24, "bold"),
            )


if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()