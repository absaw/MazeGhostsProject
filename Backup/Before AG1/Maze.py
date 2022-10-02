# -*- coding: utf-8 -*-

from multiprocessing import current_process
from collections import deque

import numpy as np
import random
import matplotlib.pyplot as plt

def maze_generator(n_row,n_col):
    
    n_row=5
    n_col=5
    maze = np.zeros((n_row,n_col))

    # 0 = Unblocked
    # 1 = Blocked
    # 100 = Ghost in Unblocked Cell
    # 200 = Ghost in Blocked cell

    for i in range(n_row):
        for j in range(n_col):
            if random.uniform(0,1)<0.28:
                maze[i][j]=1
               
    maze[0][0]=maze[n_row-1][n_col-1]=0

    print(maze)
    plt.imshow(maze,"Dark2")
    plt.show()


