import os
import random
from copy import deepcopy
from dataclasses import dataclass
from typing import List

BOARD_SIDE_LENGTH = 20
BOARD_SIDE_WITH_WALL = BOARD_SIDE_LENGTH + 2

SHAPES = {
    "I": [[1], [1], [1], [1]],
    "O": [[1, 1], [1, 1]],
    "L": [[1, 0], [1, 0], [1, 1]],
    "J": [[0, 1], [0, 1], [1, 1]],
    "S": [[0, 1], [1, 1], [1, 0]],
}

SHAPES_LIST = list(SHAPES.values())

SHAPES_COUNT = len(SHAPES_LIST)

clear = lambda: os.system("clear" if os.name == "posix" else "cls")

MOVE_LEFT = "a"
MOVE_RIGHT = "d"
ROTATE_CLOCKWISE = "w"
ROTATE_COUNTER_CLOCKWISE = "s"


@dataclass
class TetrisElement:
    shape: List[List[int]]
    position_x: int
    position_y: int

    @property
    def shape_size_x(self) -> int:
        return len(self.shape)

    @property
    def shape_size_y(self) -> int:
        return len(self.shape[0])

    def move_down(self) -> None:
        self.position_x += 1

    def move_left(self) -> None:
        self.position_y -= 1

    def move_right(self) -> None:
        self.position_y += 1

    def rotate_clockwise(self):
        shape = self.shape
        for item in range(0, 3):
            shape = self._rotate_counter_clockwise(shape)
        self.shape = shape

    def rotate_counter_clockwise(self):
        self.shape = self._rotate_counter_clockwise(self.shape)

    @staticmethod
    def _rotate_counter_clockwise(shape):
        return list(list(item) for item in zip(*deepcopy(shape)[::-1]))


class Tetris:
    def __init__(self) -> None:
        self.board = self._empty_board()
        self.tetris_element = self._get_random_shape_and_random_position()
        self.gamer_message = ""

    def play(self) -> None:
        while not self._game_over():
            self._render_board()
            player_move = input("Your move:").lower()
            move_shape_down = False
            if player_move == MOVE_LEFT:
                if self._can_move_left():
                    self.tetris_element.move_left()
                    move_shape_down = True
                else:
                    self.gamer_message = "Move left is not correct!"
            elif player_move == MOVE_RIGHT:
                if self._can_move_right():
                    self.tetris_element.move_right()
                    move_shape_down = True
                else:
                    self.gamer_message = "Move right is not correct!"
            elif player_move == ROTATE_CLOCKWISE:
                if self._can_rotate_clockwise():
                    self.tetris_element.rotate_clockwise()
                    move_shape_down = True
                else:
                    self.gamer_message = "Rotate clockwise is not correct!"
            elif player_move == ROTATE_COUNTER_CLOCKWISE:
                if self._can_rotate_counter_clockwise():
                    self.tetris_element.rotate_counter_clockwise()
                    move_shape_down = True
                else:
                    self.gamer_message = "Rotate counter clockwise is not correct!"
            else:
                self.gamer_message = "Your move is undefined"

            if move_shape_down and self._can_move_down():
                self.tetris_element.move_down()
            if not self._can_move_down():
                self._merge_shape_to_board()
                self.tetris_element = self._get_random_shape_and_random_position()

        print("GAME OVER!")

    def _can_move_down(self) -> bool:
        new_tetris_element = deepcopy(self.tetris_element)
        new_tetris_element.move_down()
        return self._is_overlap(new_tetris_element)

    def _can_move_left(self) -> bool:
        new_tetris_element = deepcopy(self.tetris_element)
        new_tetris_element.move_left()
        return self._is_overlap(new_tetris_element)

    def _can_move_right(self) -> bool:
        new_tetris_element = deepcopy(self.tetris_element)
        new_tetris_element.move_right()
        return self._is_overlap(new_tetris_element)

    def _can_rotate_clockwise(self) -> bool:
        new_tetris_element = deepcopy(self.tetris_element)
        new_tetris_element.rotate_clockwise()
        return self._is_overlap(new_tetris_element)

    def _can_rotate_counter_clockwise(self) -> bool:
        new_tetris_element = deepcopy(self.tetris_element)
        new_tetris_element.rotate_counter_clockwise()
        return self._is_overlap(new_tetris_element)

    @staticmethod
    def _empty_board() -> List[List[int]]:
        board = [
            ([1] + [0] * BOARD_SIDE_LENGTH + [1])
            for _ in range(BOARD_SIDE_WITH_WALL - 1)
        ]
        board.append([1] * BOARD_SIDE_WITH_WALL)
        return board

    def _game_over(self) -> bool:
        return not self._can_move_down() and self.tetris_element.position_x == 0

    @staticmethod
    def _get_random_shape_and_random_position() -> TetrisElement:
        shape = SHAPES_LIST[random.randrange(start=0, stop=SHAPES_COUNT)]
        position_y = random.randrange(1, BOARD_SIDE_WITH_WALL - len(shape))
        return TetrisElement(shape, 0, position_y)

    def _is_overlap(self, new_tetris_element: TetrisElement) -> bool:
        for x in range(new_tetris_element.shape_size_x):
            for y in range(new_tetris_element.shape_size_y):
                if (
                    self.board[new_tetris_element.position_x + x][
                        new_tetris_element.position_y + y
                    ]
                    == 1
                    and new_tetris_element.shape[x][y] == 1
                ):
                    return False
        return True

    def _merge_shape_to_board(self) -> None:
        for x in range(self.tetris_element.shape_size_x):
            for y in range(self.tetris_element.shape_size_y):
                self.board[self.tetris_element.position_x + x][
                    self.tetris_element.position_y + y
                ] = (
                    self.tetris_element.shape[x][y]
                    | self.board[self.tetris_element.position_x + x][
                        self.tetris_element.position_y + y
                    ]
                )

    def _render_board(self) -> None:
        clear()
        board_copy = deepcopy(self.board)
        for x in range(self.tetris_element.shape_size_x):
            for y in range(self.tetris_element.shape_size_y):
                board_copy[self.tetris_element.position_x + x][
                    self.tetris_element.position_y + y
                ] = (
                    self.tetris_element.shape[x][y]
                    | self.board[self.tetris_element.position_x + x][
                        self.tetris_element.position_y + y
                    ]
                )

        for x in range(BOARD_SIDE_WITH_WALL):
            for y in range(BOARD_SIDE_WITH_WALL):
                print("*" if board_copy[x][y] else " ", end="")
            print("")

        print(
            f"""Control:
        to move piece left - press button a 
        to move piece right - press button s 
        to rotate piece counter clockwise - press button w 
        to rotate piece clockwise - press button s
        \033[91m{self.gamer_message}\033[0m"""
        )
        self.gamer_message = ""


if __name__ == "__main__":
    Tetris().play()
