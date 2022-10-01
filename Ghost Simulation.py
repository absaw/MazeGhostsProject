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
		# print(maze)
	print("Initial Maze -> ")
	print(maze)
	n_simul = 10
	while(n_simul > 0):
		for x, y in ghost_position:
			cell_found=False
			while(not cell_found):
				random_direction = random.randint(0, 3)
				x_move = x+walk[random_direction][0]
				y_move = y+walk[random_direction][1]

				if (0 <= x_move <= n_row-1) and (0 <= y_move <= n_col-1):
					cell_found=True
			move=random.random()>=0.5

			#Empty Space
			if maze[x_move][y_move]==0:
				maze[x_move][y_move] = 100
			
			#Empty space with ghost
			elif 100<=maze[x_move][y_move]<200:
				maze[x_move][y_move] +=1 

			#Wall
			elif maze[x_move][y_move] == 1 and move:
				maze[x_move][y_move] = 200

			#Wall with Ghost
			elif maze[x_move][y_move] >= 200 and move:
				maze[x_move][y_move] += 1

			reset_prev_cell(maze,x,y)

		n_simul-=1
		print("Simulation -> ",n_simul)
		print(maze)
		# plt.imshow(maze,cmap="Dark2",alpha=0.9)
		# plt.show()
		print()

def reset_prev_cell(maze,x,y):
	if (100<maze[x][y]<200):
		maze[x][y]-=1
  
	elif(maze[x][y]>200):
		maze[x][y]-=1
  
	elif (maze[x][y]==100):
		maze[x][y]=0
  
	elif (maze[x][y]==200):
		maze[x][y]=1
	
ghost_simulation()

#     col = ListedColormap(["green","red","yellow","blue"])
#     col.set_bad("silver")
#     plt.imshow(maze,cmap=col,alpha=0.9)
#     plt.show()
