import numpy as np
from GhostSimulation import spawn_ghosts
from Maze import *

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
            if 0 <= next_r < n_row and 0 <= next_c < n_col and maze[next_r][next_c]==0 and maze[next_r][next_c] != 1 and maze[next_r][next_c] != 55:
                flood_fill(maze, n_row, n_col, next_r, next_c)
    return maze

# a = np.array([[0, 1, 1, 1, 1],
#               [0, 0, 1, 0, 1],
#               [0, 0, 1, 1, 0],
#               [1, 0, 1, 1, 0],
#               [0, 0, 0, 0, 0],
#               ])

# print(flood_fill(a,6,5, 0, 0))

# # print(a)
gh=list()
a=generate_maze(51,51,True)[0]
spawn_ghosts(a,1000,51,51,gh)
print(a)
