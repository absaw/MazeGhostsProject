from lib2to3.pgen2.pgen import DFAState
import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
# from collections import deque

# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost

def ghost_simulation():
	original_maze = np.array([[0, 0, 1, 0, 0],
					 [0, 0, 1, 0, 0],
					 [0, 0, 1, 0, 0],
					 [1, 0, 1, 1, 0],
					 [0, 0, 0, 0, 0]])
	maze=original_maze
	n_ghosts = 5
	n_row = 5
	n_col = 5
	walk = [[0, 1],
			[0, -1],
			[1, 0],
			[-1, 0]]

	ghost_position = list()

	for i in range(n_ghosts):
		row = random.randint(1,n_row-1)
		col = random.randint(1,n_col-1)
		# print(row,col)
		# print(maze[row][col])
		ghost_position.append((row, col))
		if maze[row][col] == 0:
			maze[row][col] = 100
			# Ghost present at open space
		elif maze[row][col]==1:
			maze[row][col] = 200
      
		elif 100<=maze[row][col]<200:
			maze[row][col]+=1
   
		elif maze[row][col]>=200:
			maze[row][col]+=1
			# Ghost present in wall
		# print(maze)
	ghost_maze=maze
	print("Initial Maze -> ")
	print(maze)
	n_simul = 1
 
	while(n_simul > 0):
		maze=ghost_maze
		for row, col in ghost_position:
			
			cell_found=False
			while(not cell_found):
				random_direction = random.randint(0, 3)
				row_move = row+walk[random_direction][0]
				col_move = col+walk[random_direction][1]
    
				if (0 <= row_move < n_row) and (0 <= col_move < n_col):
					cell_found=True
     
			print("Ghost -> ",row,col," - > ",row_move,col_move)
			print(maze)
			print()
			move=random.random()>=0.5

			#Empty Space--0->100
			if maze[row_move][col_move]==0:
				maze[row_move][col_move] = 100
			#Wall--1->200
			elif maze[row_move][col_move] == 1 and move:
				maze[row_move][col_move] = 200
			
			#Empty space with ghost
			elif 100<=maze[row_move][col_move]<200:
				maze[row_move][col_move] +=1 

			#Wall with Ghost
			elif maze[row_move][col_move] >= 200 and move:
				maze[row_move][col_move] += 1

			reset_prev_cell(maze,row,col)
			print(maze)

		n_simul-=1
		print("Simulation -> ",n_simul)
		print(ghost_maze)
		print(maze)
		# plt.imshow(maze,cmap="Dark2",alpha=0.9)
		# plt.show()
		print()

def reset_prev_cell(maze,row,col):
	if (100<maze[row][col]<200):
		maze[row][col]-=1
  
	elif(maze[row][col]>200):
		maze[row][col]-=1
  
	elif (maze[row][col]==100):
		maze[row][col]=0
  
	elif (maze[row][col]==200):
		maze[row][col]=1
	
ghost_simulation()

#     col = ListedColormap(["green","red","yellow","blue"])
#     col.set_bad("silver")
#     plt.imshow(maze,cmap=col,alpha=0.9)
#     plt.show()
