import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from GhostSimulation import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime

# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost


def agent_two():
    start=time()
    print("Started...")
    n_ghost=2
    n_row = 5
    n_col = 5
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]

    file=open("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentTwo.txt","a")
    text="\n\n\n======  Start Time  =========->  "+ datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Ghosts = %d"%n_ghost)
    file.write("\nNo. of mazes for each ghost = 100")
    # no of ghosts = 1
    # charter a path for agent 2

    # start walking
    # remember ghosts are present
    for i_ghost in range(2, n_ghost+1):
        n_maze=1
        n_alive_for_this_ghost = 0
        n_dead_for_this_ghost=0
        node_reached=[]
        print("Ghost Number ",i_ghost," Started")
        while (n_maze>0):
            n_maze-=1
            maze = generate_maze(n_row, n_col,True)[0]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col,ghost_position)
            run_away=False
            get_init_path=get_bfs_path(maze,n_row,n_col,(0,0),True)
            is_init_path_valid=get_init_path[0]
            path=list()
            if is_init_path_valid:
                # init_path=get_init_path[1]
                path.append(get_init_path[1].pop(1))
            else:
                run_away=True
                nearest_ghost=find_nearest_ghost(0,0,ghost_position)[1]
                max=0 #some low value
                play_next_r=-1
                play_next_c=-1
                for i in range(0,4):
                    next_pos_r=walk[i][0] #next possible row
                    next_pos_c=walk[i][1] #next possible column
                    if 0<=next_pos_r<n_row and 0<=next_pos_c<n_col and maze[next_pos_r][next_pos_c]!=1 and maze[next_pos_r][next_pos_c]<100: #must be inside grid
                        dist_frm_ghost=euclidean_distance(next_pos_r,next_pos_c,nearest_ghost[0],nearest_ghost[1])
                        if dist_frm_ghost>=max:
                            max=dist_frm_ghost
                            play_next_r=next_pos_r #player's next row
                            play_next_c=next_pos_c #player's next column
                if (play_next_r,play_next_c)==(-1,-1):
                    path.append((0,0))#ghosts at all neighboring positions. can't move
                else:
                    path.append((play_next_r,play_next_c))
            # n_alive=0
            # n_death=0
            # ghosts now present in maze. Now start walking
            # path_set=set(init_path)
            # current_planned_path=init_path.copy()
            # n_recalc=0
            
# ========================================================================================================================================
# ===============================       Player Starts Moving       =========================================================================
# ========================================================================================================================================
            for play_pos_r, play_pos_c in path:
                is_player_alive=True
                
                if maze[play_pos_r][play_pos_c]>=100:
                    is_player_alive=False
                    break
                if (play_pos_r,play_pos_c)==(n_row-1,n_col-1):
                    break
                # ===============================      Ghost Simulation       =========================================================================
                maze,ghost_position=ghost_simulation(walk,ghost_position,n_row,n_col,maze)
                # ===========================================================================
                
                #Now all ghosts are in their next position. So if player is on the same cell, they die
                if maze[play_pos_r][play_pos_c] >= 100:
                        # player dies
                    is_player_alive=False
                    node_reached.append((play_pos_r,play_pos_c))
                    break
                    
                if (play_pos_r,play_pos_c) == (n_row-1,n_col-1):
                        # player survives
                    break
                
                
                # ===================================================================================================
                # Now this code will execute only if player hasn't yet died. so player will have to replan the path
                # ===================================================================================================
                
                
                latest_path=get_bfs_path(maze,n_row,n_col,(play_pos_r,play_pos_c),True)
                
                if latest_path[0]:#contains True/False : if there exists a path from player to goal, 
                    path.append(latest_path[1].pop(1))#append the next cell in the path
                
                elif latest_path[0] == False:
                    #Path is blocked by ghost. Run away..We find the nearest ghost to current player position. 
                    #Then select the next direction which is the farthest from this particular ghost
                    
                    nearest_ghost=find_nearest_ghost(play_pos_r,play_pos_c,ghost_position)[1]
                    max=0 #some low value
                    # play_next_r=-1
                    # play_next_c=-1
                    for i in range(0,4):
                        next_pos_r=play_pos_r+walk[i][0] #next possible row
                        next_pos_c=play_pos_c+walk[i][1] #next possible column
                        if 0<=next_pos_r<n_row and 0<=next_pos_c<n_col and maze[next_pos_r][next_pos_c]!=1: #must be inside grid
                            dist_frm_ghost=euclidean_distance(next_pos_r,next_pos_c,nearest_ghost[0],nearest_ghost[1])
                            if dist_frm_ghost>=max:
                                max=dist_frm_ghost
                                play_next_r=next_pos_r #player's next row
                                play_next_c=next_pos_c #player's next column
                    if (play_next_r,play_next_c)==(-1,-1):
                        path.append((play_pos_r,play_pos_c))
                    else:
                        path.append((play_next_r,play_next_c))
                    
                    # print("\n\nRunning Away : ")
                    # print("Player Position >",play_pos_r,",",play_pos_c)
                    # print("Nearest Ghost -> ",nearest_ghost)
                    # print("Next Position -> ",play_next_r,",",play_next_c)
                    # print("Max Distance ->",max)
                    # print("Ghost Position List ->",ghost_position)
                    # print("Current Position : ",play_pos_r,play_pos_c)
                # print("\nCurrent maze - > \n",maze)
                print("\n\nPlayer Position >",play_pos_r,",",play_pos_c)
                print("Ghost Position ->",ghost_position)
                print("Curent maze  \n",maze)
                print("Path - > ",path)
                print("Latest Path ->",latest_path)
                # plt.imshow(maze,"Dark2")
                # plt.plot()
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
            #print("\nMaze number ",n_maze)
            if is_player_alive:
                print("Alive")
                n_alive_for_this_ghost+=1
            else:
                n_dead_for_this_ghost+=1
                print("Dead = ",n_dead_for_this_ghost)
                print("Dead at ",node_reached)
                print("Ghost Position : ",ghost_position)
                print("Player Position >",play_pos_r,",",play_pos_c)
                print("Death maze  \n",maze)

        file.write("\nReport for %d Number of Ghosts"%i_ghost)
        file.write("\nPlayer Survivability = %d"%n_alive_for_this_ghost+" %")
        file.write("\nDead Number-> %d"%n_dead_for_this_ghost)
        # print("Node Reached -> %d"%node_reached)

        # print("Dead = ",n_dead_for_this_ghost)
        # print("Dead at ",node_reached)
        
        print("Ghost Number ",i_ghost," Done\n")
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


agent_two()