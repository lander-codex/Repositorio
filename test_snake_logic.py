import unittest

from Pruebas import SnakeGameState


class SnakeGameStateTests(unittest.TestCase):
    def test_step_moves_head_in_current_direction(self) -> None:
        state = SnakeGameState(width=8, height=8, seed=1)
        start = state.snake[0]

        state.step()

        self.assertEqual(state.snake[0], (start[0] + 1, start[1]))

    def test_snake_grows_and_scores_when_eating_food(self) -> None:
        state = SnakeGameState(width=8, height=8, seed=1)
        head_x, head_y = state.snake[0]
        state.food = (head_x + 1, head_y)
        start_len = len(state.snake)

        state.step()

        self.assertEqual(len(state.snake), start_len + 1)
        self.assertEqual(state.score, 1)
        self.assertNotIn(state.food, state.snake)

    def test_wall_collision_sets_game_over(self) -> None:
        state = SnakeGameState(width=4, height=4, seed=1)
        state.snake = [(3, 1), (2, 1), (1, 1)]
        state.direction = (1, 0)
        state.next_direction = (1, 0)

        state.step()

        self.assertTrue(state.game_over)

    def test_self_collision_sets_game_over(self) -> None:
        state = SnakeGameState(width=6, height=6, seed=1)
        state.snake = [(2, 2), (2, 1), (3, 1), (3, 2)]
        state.direction = (0, -1)
        state.next_direction = (1, 0)

        state.step()

        self.assertTrue(state.game_over)

    def test_food_never_spawns_on_snake(self) -> None:
        state = SnakeGameState(width=3, height=3, seed=7)
        state.snake = [(0, 0), (1, 0), (2, 0), (0, 1)]

        for _ in range(20):
            food = state.place_food()
            self.assertNotIn(food, state.snake)


if __name__ == "__main__":
    unittest.main()
