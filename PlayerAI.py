from random import randint
from BaseAI import BaseAI
from math import log
import time


def utility(grid):
    empty_cells = len(grid.getAvailableCells())

    max_tile = grid.getMaxTile()

    score = 0
    smoothness = 0
    monotonicity = 0
    weights = [
        [6, 5, 4, 3],
        [5, 4, 3, 2],
        [4, 3, 2, 1],
        [3, 2, 1, 0]
    ]

    for i in range(4):
        for j in range(4):
            score += grid.map[i][j] * weights[i][j]

    for i in range(4):
        for j in range(3):
            if grid.map[i][j] >= grid.map[i][j + 1] and grid.map[i][j] != 0:
                monotonicity += log(grid.map[i][j], 2)
            if grid.map[j][i] >= grid.map[j + 1][i] and grid.map[j][i] != 0:
                monotonicity += log(grid.map[j][i], 2)
            if grid.map[i][j] == grid.map[i][j + 1] and grid.map[i][j] != 0:
                smoothness += log(grid.map[i][j], 2)
            if grid.map[j][i] == grid.map[j + 1][i] and grid.map[j][i] != 0:
                smoothness += log(grid.map[j][i], 2)

    return 0.5 * empty_cells + 10 * log(max_tile, 2) + 0.2 * monotonicity + 2 * smoothness + score


class PlayerAI(BaseAI):

    def __init__(self):
        self.time_limit = 0

    def maximize(self, grid, depth, alpha, beta):
        moves = grid.getAvailableMoves()
        if depth > 5 or not grid.canMove() or time.clock() > self.time_limit:
            return None, utility(grid)

        max_state = None, -float('inf')

        for move in moves:
            new_grid = grid.clone()
            new_grid.move(move)
            result = self.minimize(new_grid, depth + 1, alpha, beta)
            if result[1] > max_state[1]:
                max_state = move, result[1]
            if max_state[1] >= beta:
                break
            if max_state[1] > alpha:
                alpha = max_state[1]
        return max_state

    def minimize(self, grid, depth, alpha, beta):
        cells = grid.getAvailableCells()
        if depth > 5 or not grid.canMove() or time.clock() > self.time_limit:
            return None, utility(grid)

        min_state = None, float('inf')

        for cell in cells:
            new_grid = grid.clone()
            new_grid.insertTile(cell, 4 if randint(0, 99) % 9 == 0 else 2)
            result = self.maximize(new_grid, depth + 1, alpha, beta)
            if result[1] < min_state[1]:
                min_state = -1, result[1]
            if min_state[1] <= alpha:
                break
            if min_state[1] < beta:
                beta = min_state[1]
        return -1, min_state[1]

    def getMove(self, grid):
        self.time_limit = time.clock() + 0.2
        result = self.maximize(grid, 1, -float('inf'), float('inf'))
        return result[0]
