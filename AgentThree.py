import numpy as np
from CallableAgentTwo import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime


def agent_three():
    start = time()
    print("Started...")
    n_ghost = 1
    n_row = 51
    n_col = 51
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
            [0,0]]

    file = open("/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentThree.txt", "a")
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = 1")

    for i_ghost in range(1, n_ghost+1):
        n_maze = 1
        n_alive_for_this_ghost = 0
        n_dead_for_this_ghost = 0
        node_reached = []
        print("Ghost Number ", i_ghost, " Started")
        
        while (n_maze > 0):

            n_maze -= 1
            maze = generate_maze(n_row, n_col, True)[0]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col, ghost_position)
            path = []
            path.append((0,0))
            surv_dict={}
            is_player_alive=True
            #now short list all the options for agent 3 and move to the best one
            for play_pos_r,play_pos_c in path:
                
                if maze[play_pos_r][play_pos_c] >= 100:
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    break
                
                # Player has not moved into a ghost's position. So now we are at same level with ghosts. Now simulating ghosts

                # ===============================      Ghost Simulation       =========================================================================
                maze, ghost_position = ghost_simulation(walk, ghost_position, n_row, n_col, maze)
                # ===========================================================================
                #Checking if ghost has moved into player's position
                if maze[play_pos_r][play_pos_c] >= 100:
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    break
                
                #Player hasn't died yet. now decide next step to be taken..
                
                for i in range(5):

                    poss_r = play_pos_r+walk[i][0]  #possible rows
                    poss_c = play_pos_c+walk[i][1]  #possible columns
                    if 0<=poss_r<n_row and 0<=poss_c<n_col and maze[poss_r][poss_c]!=1: 
                        surv_dict[(poss_r,poss_c)]=callable_agent_two(maze,n_row,n_col,i_ghost,ghost_position,(poss_r,poss_c))
                
                print("Surv Dict->",surv_dict)
                max_surv=max(surv_dict)
                print("Max Surv",max_surv)
                max_surv_list = [m for m in surv_dict if surv_dict[m]==surv_dict[max_surv]] # all positions with survivability = max survivability are inserted in this list
                print("Max surv list ", max_surv_list)

                if len(max_surv_list)>0:
                    #tie
                    print()
                
                next_pos = max_surv_list[0]
                path.append(next_pos)
                print("Player Pos ->",next_pos)
                print("Path -> ",path)
                # print("\n\nRunning Away : ")
                # print("Player Position >",play_pos_r,",",play_pos_c)
                # print("Nearest Ghost -> ",nearest_ghost)
                # print("Next Position -> ",play_next_r,",",play_next_c)
                # print("Ghost Position List ->",ghost_position)

                # print("\n\nPlayer Position >",play_pos_r,",",play_pos_c)
                # print("Ghost Position ->",ghost_position)
                # print("Curent maze  \n",maze)
                # print("Path - > ",path)
                # print("Latest Path ->",latest_path)

            if is_player_alive:
                n_alive_for_this_ghost += 1
                print("Alive")
            else:
                n_dead_for_this_ghost += 1
                print("Dead = ",n_dead_for_this_ghost)
                # print("Dead at ",node_reached)
                # print("Ghost Position : ",ghost_position)
                # print("Player Position >",play_pos_r,",",play_pos_c)
                # print("Death maze  \n",maze)

        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" %")
        # file.write("\nDead Number-> %d"%n_dead_for_this_ghost)
        # print("Node Reached -> %d"%node_reached)
        # print("Dead = ",n_dead_for_this_ghost)
        # print("Dead at ",node_reached)

        print("Ghost Number ", i_ghost, " Done\n")
    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")

agent_three()
# agent_two()
