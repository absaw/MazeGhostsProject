import numpy as np
from CallableAgentTwo import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime
import csv

def agent_three():
    start = time()
    print("Started...")
    n_ghost = 10
    n_row = 51
    n_col = 51
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
            [0, 0]]
    filename="Results/AgentThree.txt"
    csvfile = open(filename, "a")
    csv_writer=csv.writer(csvfile)

    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    file.write(text)
    file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = 5")
    file.write("\nNo. of simulations of agent 2 at each step = 5")

    for i_ghost in range(1, n_ghost+2,2):
        n_maze = 5
        n_alive_for_this_ghost = 0
        n_dead_for_this_ghost = 0
        n_hanged_for_this_ghost = 0
        node_reached = []
        print("Ghost Number ", i_ghost, " Started")
        gh_st_time = time()

        while (n_maze > 0):
            maze_st_time=time()
            n_maze -= 1
            maze = generate_maze(n_row, n_col, True)[0]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col, ghost_position)

            get_init_path = get_bfs_path(maze, n_row, n_col, (0, 0), True)
            is_init_path_valid = get_init_path[0]
            path = list()
            if is_init_path_valid:
                path.append(get_init_path[1].pop(1))
            else:
                ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                    walk, ghost_position, n_row, n_col, maze, 0, 0)
                path.append((play_next_r, play_next_c))

            # now short list all the options for agent 3 and move to the best one
            surv_dict = {}
            path_length_dict={}
            goal_reached=False
            for play_pos_r, play_pos_c in path:
                # if (play_pos_r,play_pos_r) == (8,9) or (play_pos_r,play_pos_c)==(9,8):
                #     print("Wait")
                surv_dict.clear()
                path_length_dict.clear()
                is_player_alive = True
                is_player_hanged=False
                
                if maze[play_pos_r][play_pos_c] >= 100:
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    goal_reached=True
                    break
                curr_pos_count=path.count((play_pos_r,play_pos_c))
                # print("Current player count -> ",curr_pos_count)
                if curr_pos_count>10:
                    is_player_hanged=True
                    break

                # Player has not moved into a ghost's position. So now we are at same level with ghosts. Now simulating ghosts

                # ===============================      Ghost Simulation       =========================================================================
                maze, ghost_position = ghost_simulation(
                    walk, ghost_position, n_row, n_col, maze)
                # ===========================================================================
                # Checking if ghost has moved into player's position
                if maze[play_pos_r][play_pos_c] >= 100:
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    break

                # Player hasn't died yet. now decide next step to be taken..
                # ===================================================================================================
                # Now this code will execute only if player hasn't yet died. so player will have to replan the path
                # ===================================================================================================

                latest_path = get_bfs_path(
                    maze, n_row, n_col, (play_pos_r, play_pos_c), True)
                
                if latest_path[0]:      # contains True/False : if there exists a path from player to goal,
                    # append the next cell in the path
                    for i in range(5):
                        maze_duplicate=maze.copy()
                        poss_r = play_pos_r+walk[i][0]  # possible rows
                        poss_c = play_pos_c+walk[i][1]  # possible columns
                        if 0 <= poss_r < n_row and 0 <= poss_c < n_col and maze[poss_r][poss_c] != 1 and maze[poss_r][poss_c]<100:
                            if (poss_r,poss_c) == (n_row-1,n_col-1):
                                #goal state reached. no need to call agent_two
                                goal_reached=True
                                next_pos=(poss_r,poss_c)
                                path.append(next_pos)
                                break
                            
                            agent_two_result=callable_agent_two(
                                maze_duplicate, n_row, n_col, i_ghost, ghost_position, (poss_r, poss_c))

                            surv_dict[(poss_r, poss_c)] = agent_two_result[0]
                            path_length_dict[(poss_r, poss_c)]=agent_two_result[1]
                    if goal_reached:
                        print("goal reached. Path -> ",path)
                        print("Length = ", len(path)-1)
                        continue
                    # print("\n\nSurv Dict->", surv_dict)
                    # print("Player Position ->",play_pos_r,", ",play_pos_c)
                    # print("Path Length Dict ->",path_length_dict)
                    max_surv = max(surv_dict)
                    # print("Max Surv key->", max_surv)
                    # print("Max Surv value->", surv_dict[max_surv])
                    
                    # all positions with survivability = max survivability are inserted in this list
                    max_surv_list = [       
                        m for m in surv_dict if surv_dict[m] == surv_dict[max_surv]]    #making list of keys with max survivability
                    # print("Max surv list ->", max_surv_list)

                    if len(max_surv_list) > 0:
                        # tie
                        min_length=100000                #some high value
                        for key in max_surv_list:       #finding the key with the least average length from the path_length_dictionary
                            if path_length_dict[key]<=min_length:
                                min_length = path_length_dict[key]
                                min_path_key=key
                        next_pos=min_path_key
                    else:
                        next_pos = max_surv_list[0]
                        
                    path.append(next_pos)
                    
                # Defaulting to Agent 2's behaviour when there is no path from current position to goal
                elif latest_path[0] == False:
                    # Path is blocked by ghost. Run away..We find the nearest ghost to current player position.
                    # Then select the next direction which is the farthest from this particular ghost
                    ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                        walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                    path.append((play_next_r, play_next_c))

                print("Next Player Pos ->", next_pos)
                print("Path -> ", path)


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

            if is_player_alive and not is_player_hanged:
                n_alive_for_this_ghost += 1
                
                print("Alive")
            if is_player_alive and is_player_hanged:
                n_hanged_for_this_ghost+=1
                print("Hanged")
            if not is_player_alive:
                n_dead_for_this_ghost += 1
                print("Dead = ", n_dead_for_this_ghost)
            maze_end_time=time()
            file.write("\n\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
            print("\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
                # print("Dead at ",node_reached)
                # print("Ghost Position : ",ghost_position)
                # print("Player Position >",play_pos_r,",",play_pos_c)
                # print("Death maze  \n",maze)
        gh_end_time=time()
        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" ")
        file.write("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
        file.write("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
        file.write("\nGhost "+str(i_ghost+1)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
        print("\n\nReport for %d Number of Ghosts" % i_ghost)
        print("\nGhost "+str(i_ghost+1)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
        print("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" ")
        print("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
        print("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
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
