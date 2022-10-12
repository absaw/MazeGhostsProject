from lib2to3.pgen2.tokenize import generate_tokens
import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from GhostSimulation import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime

# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost


def callable_agent_two(maze,n_row,n_col,n_ghost,ghost_position,play_pos):
    start=time()
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]
    play_pos_r=play_pos[0]
    play_pos_c=play_pos[1]
    n_alive_simulation=0
    n_simulations=2
    sum_path_length=0
    
    for i_sim in range(1, n_simulations+1):
    
        # print("Sim Number ", i_sim, " Started")
        
        get_init_path = get_bfs_path(maze, n_row, n_col, play_pos, True)
        is_init_path_valid = get_init_path[0]
        path = list()
        if is_init_path_valid and len(get_init_path[1])>1:
            path.append(get_init_path[1].pop(1))
        elif is_init_path_valid and len(get_init_path[1])==1:
            path.append(get_init_path[1].pop(0))
        else:
            ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
            path.append((play_next_r, play_next_c))

        # ========================================================================================================================================
        # ===============================Player Starts Moving=====================================================================================
        # ========================================================================================================================================
        for play_pos_r, play_pos_c in path:
            is_player_alive = True

            if maze[play_pos_r][play_pos_c] >= 100:
                is_player_alive = False
                break
            if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                break
            # ===============================Ghost Simulation=====================================================================================
            maze, ghost_position = ghost_simulation(walk, ghost_position, n_row, n_col, maze)
            # ====================================================================================================================================

            # Now all ghosts are in their next position. So if player is on the same cell, they die
            if maze[play_pos_r][play_pos_c] >= 100:
                # player dies
                is_player_alive = False
                break

            if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                # player survives
                break

            # ===================================================================================================
            # Now this code will execute only if player hasn't yet died. so player will have to replan the path
            # ===================================================================================================
            latest_path = get_bfs_path(
                maze, n_row, n_col, (play_pos_r, play_pos_c), True)
            # contains True/False : if there exists a path from player to goal,
            if latest_path[0]:
                # append the next cell in the path
                path.append(latest_path[1].pop(1))
            elif latest_path[0] == False:
                # Path is blocked by ghost. Run away..We find the nearest ghost to current player position.
                # Then select the next direction which is the farthest from this particular ghost
                ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                    walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                path.append((play_next_r, play_next_c))
            # print("\n\nPlayer Position >",play_pos_r,",",play_pos_c)
            # print("Ghost Position ->",ghost_position)
            # print("Curent maze  \n",maze)
            # print("Path - > ",path)
            # print("Latest Path ->",latest_path)
        if is_player_alive:
            n_alive_simulation += 1
            # if len(path)==1:
            #     sum_path_length=0
            if len(path)>=2:
                sum_path_length+=len(path)-1
            # print("Alive -- path Length = ",sum_path_length)
            
        # else:
        #     n_dead_simulation += 1

        # print("Alive = ",n_alive_simulation)
        # print("Sim Number ", i_sim, " Done\n")
    survivability=n_alive_simulation/n_simulations * 100
    if n_alive_simulation !=0:
        avg_path_length=sum_path_length/n_alive_simulation
    else:
        avg_path_length=10000 #some high value so that it is not picked while calculating the shortest path
    # print("Survivability = ",survivability)
    # print("Avg path length = ",avg_path_length)
    end = time()
    # print("Execution time : "+str(end-start)+" s")
    # print("Done!")
    return survivability, avg_path_length
# a=np.array([[0,1,0,1,1],
#             [0,0,100,0,1],
#             [0,0,0,0,0],
#             [1,0,1,0,0],
#             [0,100,0,0,0]])
# a=generate_maze(51,51,True)[0]
# ghost_position=list()
# # print(a)
# spawn_ghosts(a,10,51,51,ghost_position)
# # ghost_position=[(1,2),(4,1)]
# print("Ghost Position List ->",ghost_position)
# print("No. of ghosts -> ",len(ghost_position))
# print(a)
# print(callable_agent_two(a,51,51,10,ghost_position,(0,0)))
