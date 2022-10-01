from lib2to3.pgen2.pgen import DFAState
import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
# from collections import deque


def ghost_simulation():
	maze = np.array([[0, 0, 1, 0, 0],
					 [0, 0, 1, 0, 0],
					 [0, 0, 1, 0, 0],
					 [1, 0, 1, 1, 0],
					 [0, 0, 0, 0, 0]])
	n_ghosts = 5
	n_row = 5
	n_col = 5
	walk = [[0, 1],
			[0, -1],
			[1, 0],
			[-1, 0]]

	ghost_position = list()

	for i in range(n_ghosts):
		x = int(random.uniform(1, n_row-1))
		y = int(random.uniform(1, n_col-1))
		# print(x,y)
		# print(maze[x][y])
		ghost_position.append((x, y))
		if maze[x][y] == 0:
			maze[x][y] = 100
			# Ghost present at open space
		else:
			maze[x][y] = 200
			# Ghost present in wall
		print(maze)
	n_simul = 10
	while(n_simul > 0):
		for x, y in ghost_position:
					# random_direction=int(random.uniform(0,4))
			random_direction = random.randint(0, 3)
					# for i in range(4):
			x_move = x+walk[random_direction][0]
			y_move = y+walk[random_direction][1]

			if (0 <= x_move <= n_row-1) and (0 <= y_move <= n_col-1):
				move=random.random()>=0.5
    
				if maze[x_move][y_move] == 1 and move:
					maze[x_move][y_move] = 200
     
				elif maze[x_move][y_move] >= 200 and move:
					maze[x_move][y_move] += 1
     
				elif maze[x_move][y_move]==0 and move:
					maze[x_move][y_move] = 100
     
				elif 100<=maze[x_move][y_move]<200 and move:
					maze[x_move][y_move] +=1 
     
		n_simul-=1
		print(maze)

ghost_simulation()

#     col = ListedColormap(["green","red","yellow","blue"])
#     col.set_bad("silver")
#     plt.imshow(maze,cmap=col,alpha=0.9)
#     plt.show()
