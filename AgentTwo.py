import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
import BFS
import GhostSimulation
import Maze
from BFS import get_bfs_path
from Maze import generate_maze
from time import time
from datetime import datetime
# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost


def agent_two():
    start=time()
    print("Started...")
    n_ghost=1
    n_row = 10
    n_col = 10
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]

    #file=open("Results/AgentTwo.txt","a")
    # text="\n\n\n======  Start Time  =========->  "+ datetime.now().strftime("%m/%d/%y %H:%M:%S")
    #file.write(text)
    #file.write("\nNo. of Ghosts = %d"%n_ghost)
    #file.write("\nNo. of mazes for each ghost = 100")
    # file.close()
    # no of ghosts = 1
    # charter a path for agent 2

    # start walking
    # remember ghosts are present
    for i_ghost in range(1, n_ghost+1):
        n_maze=1
        n_alive_for_this_ghost = 0
        while (n_maze>0):
            n_maze-=1
            maze_generator_result = generate_maze(n_row, n_col,True)
            maze = maze_generator_result[0]
            initial_path = maze_generator_result[1]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col,ghost_position)
            # n_alive=0
            # n_death=0
            # ghosts now present in maze. Now start walking
            # path_set=set(initial_path)
            path=list()
            path.append(initial_path.pop(1))
            # current_planned_path=initial_path.copy()
            # n_recalc=0
            for play_pos_r, play_pos_c in path:
                is_player_alive=True
                next_ghost_position=list()

                # Simulate movement for ghost
                # =========================================================================
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
                # ===========================================================================
                #Now all ghosts are in their next position. So if player is on the same cell, they die
                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive=False
                    break
                if (play_pos_r,play_pos_c) == (n_row-1,n_col-1):
                    # player survives
                    break
                # ===================================================================================================
                
                # Now this code will execute only if player hasn't yet died. so player will have to replan the path
                latest_path=get_bfs_path(maze,n_col,n_row,(play_pos_r,play_pos_c),True)
                print("Latest Path->",latest_path)
                
                if latest_path[0]:#contains True/False : if there exists a path from player to goal, without ghosts
                    # if (len(latest_path[1])==1):
                    #     path.append(latest_path[1].pop(0))
                    # else:
                    path.append(latest_path[1].pop(1))#append the next cell in the path
                    print("Moving : Current path ",path)
                    print("Current Position : ",play_pos_r,play_pos_c)
                # ===================================================================================================
                
                
                else:
                    
                    #Path is blocked by ghost. Run away..
                    #We find the nearest ghost to current player position. 
                    nearest_ghost=find_nearest_ghost(play_pos_r,play_pos_c,ghost_position)[1]
                    # Then select the next direction which is the farthest from this particular ghost
                    max=-1 #some low value
                    for i in range(0,4):
                        next_pos_r=play_pos_r+walk[i][0] #next possible row
                        next_pos_c=play_pos_c+walk[i][1] #next possible column
                        if 0<=next_pos_r<n_row and 0<=next_pos_c<n_col and maze[next_pos_r][next_pos_c]!=1: #must be inside grid
                            dist_frm_ghost=euclidean_distance(next_pos_r,next_pos_c,nearest_ghost[0],nearest_ghost[1])
                            if dist_frm_ghost<max:
                                min=dist_frm_ghost
                                play_next_r=next_pos_r #player's next row
                                play_next_c=next_pos_c #player's next column

                    
                    path.append((play_next_r,play_next_c))
                    print("Running Away : ",path)
                    print("Current Position : ",play_pos_r,play_pos_c)

                # ===================================================================================================
                #First checking if we can stick to current path
                # ghost_set=set(ghost_position)
                # # path_set=set(latest_path)
                
                # if(len(ghost_set&path_set)!=0):
                #     latest_path=get_bfs_path(maze,n_col,n_row,(play_pos_r,play_pos_c),True)
                #     n_recalc+=1
                # else:
                #     path.append(latest_path.pop(0))


            # print("Simulation for %d ghosts done"%(i_ghost))
            if is_player_alive:
                # print("Alive")
                n_alive_for_this_ghost+=1
            # else:
                # print("Dead at ",node_reached)
        #file.write("\nReport for %d Number of Ghosts"%i_ghost)
        #file.write("\nPlayer Survivability = %d"%n_alive_for_this_ghost+" %")
        print(i_ghost," ")
        # print(maze)
    end = time()
    #file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    #file.close()
    print("Done!")
    # n_simul-=1
    # print("Simulation -> ",n_simul)
    # print(ghost_maze)
    # print(maze)
    # plt.imshow(maze,cmap="Dark2",alpha=0.9)
    # plt.show()
    # print()

def find_nearest_ghost(play_pos_r,play_pos_c,ghost_position):
    min_dist = 1000 #Some initial high value
    # play_pos_r=play_pos_c=0
    # ghost_position=[(3,4),(2,3),(6,8),(1,1)]
    min_gh_r=ghost_position[0][0]
    min_gh_c=ghost_position[0][1]
    for gh_r, gh_c in ghost_position:
        curr_dist = euclidean_distance(play_pos_r,play_pos_c,gh_r,gh_c)
        # curr_dist = np.sqrt((gh_r-play_pos_r)**2+(gh_c-play_pos_c)**2)
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_gh_r = gh_r
            min_gh_c = gh_c
    # print("Min Dist = ",min_dist)
    # print("Co-Ordinates = ",min_gh_r,", ", min_gh_c)
    return min_dist,(min_gh_r,min_gh_c)

def euclidean_distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2+(y1-y2)**2)

def manhattan_distance(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y2-y1)

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

agent_two()