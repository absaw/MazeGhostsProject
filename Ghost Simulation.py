import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
import collections
# from collections import deque

def ghost_simulation():
    maze=[  [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [1,0,1,1,0],
            [0,0,0,0,0]]
    n_row=5
    n_col=5
    walk = [[0, 1],
            [0,-1],
            [1, 0],
            [-1,0]]