import numpy as np
from GhostSimulation import spawn_ghosts
# a = np.array([[0, 1, 1, 1, 1],
#               [0, 0, 1, 0, 1],
#               [0, 0, 1, 1, 0],
#               [1, 0, 1, 1, 0],
#               [0, 0, 0, 0, 0],
#               ])


def flood_fill(maze, n_row, n_col, x, y):

    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]
    if maze[x][y] == 0:
        maze[x][y] = 55

        for i in range(4):
            next_r = x+walk[i][0]
            next_c = y+walk[i][1]
            if 0 <= next_r < n_row and 0 <= next_c < n_col and maze[next_r][next_c] != 1 and maze[next_r][next_c] != 55:
                flood_fill(maze, n_row, n_col, next_r, next_c)
    return maze


# print(flood_fill(a,6,5, 0, 0))

# # print(a)
# gh=list()
# print(spawn_ghosts(a, 15,5,5,gh))
# print(a)
