# -*- coding: utf-8 -*-

from multiprocessing import current_process
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque
n_row=5
n_col=5
maze = np.zeros((n_row,n_col))

# 0 = Unblocked
# 1 = Blocked
# 10 = Ghost in Unblocked Cell
# 11 = Ghost in Blocked cell

for i in range(n_row):
    for j in range(n_col):
        # random.seed(j)
        if random.uniform(0,1)<0.28:
            maze[i][j]=1
            # if random.uniform(0,1)>0.5:
            #     maze[i][j]=10
        # else:
        #     if random.uniform(0,1)>0.5:
        #         maze[i][j]=
maze[0][0]=maze[n_row-1][n_col-1]=0

print(maze)
plt.imshow(maze,"Dark2")
plt.show()


