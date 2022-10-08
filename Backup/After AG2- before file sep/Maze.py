# -*- coding: utf-8 -*-

from multiprocessing import current_process
from collections import deque

import numpy as np
import random
import matplotlib.pyplot as plt
from BFS import get_bfs_path

# 0 = Unblocked
# 1 = Blocked
# 100 = Ghost in Unblocked Cell
# 200 = Ghost in Blocked cell

def generate_maze(n_row,n_col,ghost_present):
    maze_generated=False
    while(not maze_generated):
        maze = np.zeros((n_row,n_col))

        for i in range(n_row):
            for j in range(n_col):
                if random.uniform(0,1)<0.28:
                    maze[i][j]=1
                
        maze[0][0]=maze[n_row-1][n_col-1]=0
        
        bfs_result=get_bfs_path(maze,n_row,n_col,(0,0),ghost_present)
        
        path_possible=bfs_result[0]
        
        if path_possible:
            maze_generated=True
            shortest_path=bfs_result[1]
        
        
        # if check_maze_validity(maze,n_row,n_col,(0,0)[0]):
        #     maze_generated=True
    return [maze,shortest_path]

def check_maze_validity(maze,n_row,n_col,start):
    # ismazevalid=get_bfs_path(maze,n_row,n_col,start)
    # print (ismazevalid)
    # return ismazevalid[0]
    return get_bfs_path(maze,n_row,n_col,start)

def plot_maze(maze):
    # print(maze)
    plt.imshow(maze,"Dark2")
    plt.show()


# plot_maze(generate_maze(5,5,True)[0])
