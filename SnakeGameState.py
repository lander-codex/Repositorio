from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Position = Tuple[int, int]

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0),
}


@dataclass
class SnakeGameState:
    width: int = 20
    height: int = 20
    seed: Optional[int] = None
    snake: List[Position] = field(default_factory=list)
    direction: Position = (1, 0)
    next_direction: Position = (1, 0)
    food: Position = (0, 0)
    score: int = 0
    game_over: bool = False
    paused: bool = False

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self.reset()

    def reset(self) -> None:
        cx = self.width // 2
        cy = self.height // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.food = self.place_food()

    def set_direction(self, new_direction: Position) -> None:
        if self.game_over:
            return

        opposite = (-self.direction[0], -self.direction[1])
        if len(self.snake) > 1 and new_direction == opposite:
            return

        self.next_direction = new_direction

    def place_food(self) -> Position:
        occupied = set(self.snake)
        free_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in occupied
        ]

        if not free_cells:
            self.game_over = True
            return self.snake[0]

        return self._rng.choice(free_cells)

    def step(self) -> None:
        if self.game_over or self.paused:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.game_over = True
            return

        grows = new_head == self.food
        body_to_check = self.snake if grows else self.snake[:-1]
        if new_head in body_to_check:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if grows:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()


class SnakeApp:
    CELL_SIZE = 24
    TICK_MS = 130

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Snake")

        self.state = SnakeGameState(width=20, height=20)

        self.score_label = tk.Label(root, text="Score: 0")
        self.score_label.pack(pady=6)

        canvas_w = self.state.width * self.CELL_SIZE
        canvas_h = self.state.height * self.CELL_SIZE
        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="#111", highlightthickness=0)
        self.canvas.pack()

        self.controls = tk.Frame(root)
        self.controls.pack(pady=8)

        self._build_controls()
        self.root.bind("<Key>", self.on_key)

        self.draw()
        self.loop()

    def _build_controls(self) -> None:
        top = tk.Frame(self.controls)
        top.pack()
        mid = tk.Frame(self.controls)
        mid.pack()

        tk.Button(top, text="Up", width=8, command=lambda: self.set_dir((0, -1))).pack()
        tk.Button(mid, text="Left", width=8, command=lambda: self.set_dir((-1, 0))).pack(side="left")
        tk.Button(mid, text="Down", width=8, command=lambda: self.set_dir((0, 1))).pack(side="left")
        tk.Button(mid, text="Right", width=8, command=lambda: self.set_dir((1, 0))).pack(side="left")

        bottom = tk.Frame(self.controls)
        bottom.pack(pady=4)
        tk.Button(bottom, text="Pause/Resume", width=12, command=self.toggle_pause).pack(side="left", padx=4)
        tk.Button(bottom, text="Restart", width=10, command=self.restart).pack(side="left", padx=4)

    def set_dir(self, direction: Position) -> None:
        self.state.set_direction(direction)

    def on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key in DIRECTIONS:
            self.set_dir(DIRECTIONS[key])
            return

        if key == "space":
            self.toggle_pause()
        elif key.lower() == "r":
            self.restart()

    def toggle_pause(self) -> None:
        if self.state.game_over:
            return
        self.state.paused = not self.state.paused

    def restart(self) -> None:
        self.state.reset()
        self.draw()

    def loop(self) -> None:
        self.state.step()
        self.draw()
        self.root.after(self.TICK_MS, self.loop)

    def draw(self) -> None:
        self.canvas.delete("all")

        for x, y in self.state.snake:
            self._draw_cell(x, y, "#2ecc71")

        fx, fy = self.state.food
        self._draw_cell(fx, fy, "#e74c3c")

        self.score_label.config(text=f"Score: {self.state.score}")

        if self.state.game_over:
            self.canvas.create_text(
                (self.state.width * self.CELL_SIZE) // 2,
                (self.state.height * self.CELL_SIZE) // 2,
                text="Game Over - Press R or Restart",
                fill="white",
                font=("Arial", 14, "bold"),
            )
        elif self.state.paused:
            self.canvas.create_text(
                (self.state.width * self.CELL_SIZE) // 2,
                (self.state.height * self.CELL_SIZE) // 2,
                text="Paused",
                fill="white",
                font=("Arial", 14, "bold"),
            )

    def _draw_cell(self, x: int, y: int, color: str) -> None:
        x1 = x * self.CELL_SIZE
        y1 = y * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")


def main() -> None:
    root = tk.Tk()
    SnakeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
