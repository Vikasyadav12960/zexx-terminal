from __future__ import annotations

import os
import random
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ============================================================
# CONFIGURATION
# ============================================================

BOARD_WIDTH = 30
BOARD_HEIGHT = 16

STARTING_LENGTH = 3
INITIAL_SPEED = 0.14
MIN_SPEED = 0.055
SPEED_INCREMENT = 0.004

FOOD_SCORE = 10


# ============================================================
# TYPES
# ============================================================

Position = tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    def is_opposite(self, other: "Direction") -> bool:
        return (
            self.dx == -other.dx
            and self.dy == -other.dy
        )


class GameState(Enum):
    READY = "ready"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    WON = "won"
    QUIT = "quit"


# ============================================================
# GAME CONFIG
# ============================================================

@dataclass
class GameConfig:
    width: int = BOARD_WIDTH
    height: int = BOARD_HEIGHT

    starting_length: int = STARTING_LENGTH

    initial_speed: float = INITIAL_SPEED
    minimum_speed: float = MIN_SPEED
    speed_increment: float = SPEED_INCREMENT

    food_score: int = FOOD_SCORE


# ============================================================
# SNAKE
# ============================================================

class Snake:
    def __init__(
        self,
        start: Position,
        length: int,
        direction: Direction,
    ):
        self.direction = direction
        self.next_direction = direction

        x, y = start

        self.body: list[Position] = []

        for i in range(length):
            self.body.append(
                (x - i, y)
            )

    @property
    def head(self) -> Position:
        return self.body[0]

    def change_direction(self, direction: Direction) -> None:
        """
        Queue a direction change.

        Prevents the snake from immediately reversing into itself.
        """
        if direction.is_opposite(self.direction):
            return

        self.next_direction = direction

    def move(self, grow: bool = False) -> Position:
        """
        Move the snake one step.

        Returns the new head position.
        """
        self.direction = self.next_direction

        head_x, head_y = self.head

        new_head = (
            head_x + self.direction.dx,
            head_y + self.direction.dy,
        )

        self.body.insert(0, new_head)

        if not grow:
            self.body.pop()

        return new_head

    def occupies(self, position: Position) -> bool:
        return position in self.body

    def occupies_except_tail(self, position: Position) -> bool:
        return position in self.body[:-1]


# ============================================================
# FOOD
# ============================================================

class Food:
    def __init__(self):
        self.position: Optional[Position] = None

    def spawn(
        self,
        width: int,
        height: int,
        occupied: list[Position],
    ) -> bool:
        occupied_set = set(occupied)

        available = [
            (x, y)
            for y in range(height)
            for x in range(width)
            if (x, y) not in occupied_set
        ]

        if not available:
            self.position = None
            return False

        self.position = random.choice(available)

        return True

    def is_eaten(self, position: Position) -> bool:
        return self.position == position


# ============================================================
# INPUT
# ============================================================

class InputManager:

    KEY_MAP = {
        "w": Direction.UP,
        "s": Direction.DOWN,
        "a": Direction.LEFT,
        "d": Direction.RIGHT,

        "up": Direction.UP,
        "down": Direction.DOWN,
        "left": Direction.LEFT,
        "right": Direction.RIGHT,
    }

    def read_key(self) -> Optional[str]:
        if os.name == "nt":
            return self._read_windows_key()

        return self._read_unix_key()

    def _read_windows_key(self) -> Optional[str]:
        import msvcrt

        if not msvcrt.kbhit():
            return None

        key = msvcrt.getch()

        # Windows special keys / arrows
        if key in (b"\x00", b"\xe0"):
            special = msvcrt.getch()

            return {
                b"H": "up",
                b"P": "down",
                b"K": "left",
                b"M": "right",
            }.get(special)

        try:
            return key.decode("utf-8").lower()

        except UnicodeDecodeError:
            return None

    def _read_unix_key(self) -> Optional[str]:
        import select

        ready, _, _ = select.select(
            [sys.stdin],
            [],
            [],
            0,
        )

        if not ready:
            return None

        return sys.stdin.read(1).lower()

    def get_direction(self, key: Optional[str]) -> Optional[Direction]:
        if key is None:
            return None

        return self.KEY_MAP.get(key)


# ============================================================
# RENDERER
# ============================================================

class Renderer:

    WALL_TOP_LEFT = "╔"
    WALL_TOP_RIGHT = "╗"
    WALL_BOTTOM_LEFT = "╚"
    WALL_BOTTOM_RIGHT = "╝"
    WALL_HORIZONTAL = "═"
    WALL_VERTICAL = "║"

    EMPTY = " "
    FOOD = "●"
    HEAD = "█"
    BODY = "▓"

    def clear(self) -> None:
        os.system(
            "cls" if os.name == "nt" else "clear"
        )

    def render(
        self,
        game: "SnakeGame",
    ) -> None:

        self.clear()

        print()
        print(
            f"  ZEXX SNAKE"
            f"    SCORE: {game.score}"
            f"    HIGH: {game.high_score}"
        )

        print(
            "  "
            + self.WALL_TOP_LEFT
            + self.WALL_HORIZONTAL * game.config.width
            + self.WALL_TOP_RIGHT
        )

        snake_set = set(game.snake.body)

        for y in range(game.config.height):

            row = []

            for x in range(game.config.width):

                position = (x, y)

                if position == game.food.position:
                    row.append(self.FOOD)

                elif position == game.snake.head:
                    row.append(self.HEAD)

                elif position in snake_set:
                    row.append(self.BODY)

                else:
                    row.append(self.EMPTY)

            print(
                "  "
                + self.WALL_VERTICAL
                + "".join(row)
                + self.WALL_VERTICAL
            )

        print(
            "  "
            + self.WALL_BOTTOM_LEFT
            + self.WALL_HORIZONTAL * game.config.width
            + self.WALL_BOTTOM_RIGHT
        )

        self.render_status(game)

    def render_status(
        self,
        game: "SnakeGame",
    ) -> None:

        print()

        if game.state == GameState.READY:
            print("  Press W/A/S/D or Arrow Keys to start.")

        elif game.state == GameState.PLAYING:
            print("  WASD / ARROWS  Move")
            print("  P              Pause")
            print("  Q              Quit")

        elif game.state == GameState.PAUSED:
            print("  ╔══════════════════════╗")
            print("  ║        PAUSED        ║")
            print("  ╚══════════════════════╝")
            print()
            print("  P = Resume")
            print("  Q = Quit")

        elif game.state == GameState.GAME_OVER:
            print("  ╔══════════════════════╗")
            print("  ║      GAME OVER       ║")
            print("  ╚══════════════════════╝")
            print()
            print(f"  Final Score: {game.score}")
            print()
            print("  R = Restart")
            print("  Q = Quit")

        elif game.state == GameState.WON:
            print("  ╔══════════════════════╗")
            print("  ║       YOU WIN!       ║")
            print("  ╚══════════════════════╝")
            print()
            print(f"  Final Score: {game.score}")
            print()
            print("  R = Restart")
            print("  Q = Quit")


# ============================================================
# GAME
# ============================================================

class SnakeGame:

    def __init__(
        self,
        config: Optional[GameConfig] = None,
    ):
        self.config = config or GameConfig()

        self.input = InputManager()
        self.renderer = Renderer()

        self.state = GameState.READY

        self.snake: Snake
        self.food = Food()

        self.score = 0
        self.high_score = 0

        self.speed = self.config.initial_speed

        self.reset()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset(self) -> None:

        center = (
            self.config.width // 2,
            self.config.height // 2,
        )

        self.snake = Snake(
            start=center,
            length=self.config.starting_length,
            direction=Direction.RIGHT,
        )

        self.food = Food()

        self.food.spawn(
            self.config.width,
            self.config.height,
            self.snake.body,
        )

        self.score = 0
        self.speed = self.config.initial_speed

        self.state = GameState.READY

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    def handle_input(
        self,
        key: Optional[str],
    ) -> bool:

        if key is None:
            return True

        # Quit
        if key == "q":
            self.state = GameState.QUIT
            return False

        # Pause / resume
        if key == "p":

            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED

            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING

            return True

        # Restart
        if key == "r":

            if self.state in (
                GameState.GAME_OVER,
                GameState.WON,
            ):
                self.reset()

            return True

        direction = self.input.get_direction(key)

        if direction is None:
            return True

        # READY -> PLAYING
        if self.state == GameState.READY:
            self.snake.direction = direction
            self.snake.next_direction = direction
            self.state = GameState.PLAYING
            return True

        # Normal direction change
        if self.state == GameState.PLAYING:
            self.snake.change_direction(direction)

        return True

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self) -> None:

        if self.state != GameState.PLAYING:
            return

        # Predict next head
        head_x, head_y = self.snake.head

        new_head = (
            head_x + self.snake.next_direction.dx,
            head_y + self.snake.next_direction.dy,
        )

        # Wall collision
        if self.is_wall_collision(new_head):
            self.end_game()
            return

        # Food
        will_eat = self.food.is_eaten(new_head)

        # Self collision
        if will_eat:
            collision = self.snake.occupies(new_head)
        else:
            collision = self.snake.occupies_except_tail(new_head)

        if collision:
            self.end_game()
            return

        # Move
        self.snake.move(grow=will_eat)

        # Eat food
        if will_eat:
            self.score += self.config.food_score

            self.speed = max(
                self.config.minimum_speed,
                self.speed - self.config.speed_increment,
            )

            spawned = self.food.spawn(
                self.config.width,
                self.config.height,
                self.snake.body,
            )

            if not spawned:
                self.state = GameState.WON
                self.update_high_score()
                return

        self.update_high_score()

    # --------------------------------------------------------
    # COLLISION
    # --------------------------------------------------------

    def is_wall_collision(
        self,
        position: Position,
    ) -> bool:

        x, y = position

        return (
            x < 0
            or x >= self.config.width
            or y < 0
            or y >= self.config.height
        )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    def update_high_score(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    def end_game(self) -> None:

        self.update_high_score()

        self.state = GameState.GAME_OVER

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    def run(self) -> None:

        self.renderer.render(self)

        while self.state != GameState.QUIT:

            frame_start = time.monotonic()

            # Process all available input
            while True:

                key = self.input.read_key()

                if key is None:
                    break

                if not self.handle_input(key):
                    break

            if self.state == GameState.QUIT:
                break

            self.update()

            self.renderer.render(self)

            elapsed = time.monotonic() - frame_start

            sleep_time = max(
                0.01,
                self.speed - elapsed,
            )

            time.sleep(sleep_time)

        self.renderer.clear()


# ============================================================
# ENTRY POINT
# ============================================================

def main() -> None:

    game = SnakeGame()

    try:
        game.run()

    except KeyboardInterrupt:
        pass

    finally:
        game.renderer.clear()


if __name__ == "__main__":
    main()