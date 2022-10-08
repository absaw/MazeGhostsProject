import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
import BFS
import GhostSimulation
import Maze
# from BFS import get_bfs_path
from Maze import generate_maze
from time import time
from datetime import datetime
# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost


def agent_one():
    start=time()
    print("Started...")
    
    n_ghost=200
    n_row = 51
    n_col = 51
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]
    file=open("Results/AgentOne.txt","a")
    text="\n\n\n======  Start Time  =========->  "+ datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Ghosts = %d"%n_ghost)
    file.write("\nNo. of mazes for each ghost = 100")
    # charter a path for agent 1

    # start walking
    # remember ghosts are present
    for i_ghost in range(1, n_ghost+1,5):
        n_maze=100
        n_alive_for_this_ghost = 0
        while (n_maze>0):
            n_maze-=1
            maze_generator_result = generate_maze(n_row, n_col,True)
            maze = maze_generator_result[0]
            path = maze_generator_result[1]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col,ghost_position)
            # n_alive=0
            # n_death=0
            # ghosts now present in maze. Now start walking

            for play_pos_r, play_pos_c in path:
                # Simulate movement for ghost
                is_player_alive=True
                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive=False
                    break

                next_ghost_position=list()
                for row, col in ghost_position:

                    cell_found = False
                    while(not cell_found):
                        random_direction = random.randint(0, 3)
                        row_move = row+walk[random_direction][0]
                        col_move = col+walk[random_direction][1]

                        if (0 <= row_move < n_row) and (0 <= col_move < n_col):
                            cell_found = True

                    # print("\n\nGhost -> ", row, col, " - > ", row_move, col_move)
                    # print(maze, "\n")
                    next_ghost_position.append((row_move,col_move))
                    move_to_next_cell(maze, row_move, col_move)
                    reset_prev_cell(maze, row, col)
                ghost_position=next_ghost_position
                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive=False
                    # node_reached = (play_pos_r,play_pos_c)
                    break
                # if (play_pos_r,play_pos_c) == (n_row,n_col):
                    # node_reached=(n_row,n_col)

            # print("Simulation for %d ghosts done"%(i_ghost))
            if is_player_alive:
                # print("Alive")
                n_alive_for_this_ghost+=1
            # else:
                # print("Dead at ",node_reached)
        file.write("\nReport for %d Number of Ghosts"%i_ghost)
        file.write("\nPlayer Survivability = %d"%n_alive_for_this_ghost+" %")
        print(i_ghost," ")
        # print(maze)
    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")
    # n_simul-=1
    # print("Simulation -> ",n_simul)
    # print(ghost_maze)
    # print(maze)
    # plt.imshow(maze,cmap="Dark2",alpha=0.9)
    # plt.show()
    # print()


def spawn_ghosts(maze, n_ghost, n_row, n_col,ghost_position):
    # ghost_position = list()
    # Spawning Ghosts at random location
    for i in range(n_ghost):
        row = random.randint(1, n_row-1)
        col = random.randint(1, n_col-1)
        ghost_position.append((row, col))

        # Ghost present at open space
        if maze[row][col] == 0:
            maze[row][col] = 100

        # Ghost present in wall
        elif maze[row][col] == 1:
            maze[row][col] = 200

        # More than one ghost present at open space
        elif 100 <= maze[row][col] < 200:
            maze[row][col] += 1

        # More than one ghost present in wall
        elif maze[row][col] >= 200:
            maze[row][col] += 1


def move_to_next_cell(maze, row_move, col_move):
    move = random.random() >= 0.5

    # Empty Space--0->100
    if maze[row_move][col_move] == 0:
        maze[row_move][col_move] = 100
    # Wall--1->200
    elif maze[row_move][col_move] == 1 and move:
        maze[row_move][col_move] = 200

    # Empty space with ghost
    elif 100 <= maze[row_move][col_move] < 200:
        maze[row_move][col_move] += 1

    # Wall with Ghost
    elif maze[row_move][col_move] >= 200 and move:
        maze[row_move][col_move] += 1


def reset_prev_cell(maze, row, col):
    if (100 < maze[row][col] < 200):
        maze[row][col] -= 1

    elif(maze[row][col] > 200):
        maze[row][col] -= 1

    elif (maze[row][col] == 100):
        maze[row][col] = 0

    elif (maze[row][col] == 200):
        maze[row][col] = 1

agent_one()