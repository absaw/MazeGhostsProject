import numpy as np
from CallableAgentTwo import *
from BFS import *
from Maze import *
from time import time
from datetime import datetime
import csv
import multiprocessing as mp

def agent_three(n_gh_lb, n_gh_ub, ProcessName):
    start = time()
    print("Started...")
    # n_ghost = 50
    n_row = 51
    n_col = 51
    no_of_mazes=10
    walk = [[0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [0, 0]]

    # walk = [[0, 1],
    #         [0, -1],
    #         [1, 0],
    #         [-1, 0],
    #         [0, 0]]
    filename_txt="Results/MultiprocessedAgentThree/"+ProcessName+".txt"
    filename_csv="Results/MultiprocessedAgentThree/"+ProcessName+".csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    # fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
    # csv_writer.writerow(fields)
    time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
    text = "\n\n\n======  Start Time for "+ProcessName+"  =========->  " +time_now
    csv_writer.writerow(["Execution Started "+ProcessName])
    file.write(text)
    # file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = "+str(no_of_mazes))
    # file.write("\nNo. of simulations of agent 2 at each step = 5")

    for i_ghost in range(n_gh_lb, n_gh_ub+1):
        n_maze = no_of_mazes
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
                if curr_pos_count>50:
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
                        ghost_position_duplicate=ghost_position.copy()
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
                                maze_duplicate, n_row, n_col, i_ghost, ghost_position_duplicate, (poss_r, poss_c))
                            # agent_two_result=callable_agent_two(
                            #     maze_duplicate, n_row, n_col, i_ghost, ghost_position, (poss_r, poss_c))

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
                            if path_length_dict[key]<min_length:
                                min_length = path_length_dict[key]
                                min_path_key=key
                        next_pos=min_path_key
                    else:
                        next_pos = max_surv_list[0]
                        
                    # print("Next Player Pos ->", next_pos)
                    path.append(next_pos)
                    
                # Defaulting to Agent 2's behaviour when there is no path from current position to goal
                elif latest_path[0] == False:
                    # Path is blocked by ghost. Run away..We find the nearest ghost to current player position.
                    # Then select the next direction which is the farthest from this particular ghost
                    ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                        walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                    path.append((play_next_r, play_next_c))
                    # print("Next Player Pos ->", (play_next_r, play_next_c))
                
            # print("Path -> ",path)
                # print("Past player position ->",play_pos_r,play_pos_c)
                # print("ghost position ->",ghost_position)
                # print("maze -> \n",maze)

            if is_player_alive and not is_player_hanged:
                n_alive_for_this_ghost += 1
                
                print("Alive=",n_alive_for_this_ghost)
                # print("Maze - \n",maze)
                # print("path -> ",path)
            if is_player_alive and is_player_hanged:
                n_hanged_for_this_ghost+=1
                print("Hanged=", n_hanged_for_this_ghost)
                # print("Maze - \n",maze)
                # print("path -> ",path)
            if not is_player_alive:
                n_dead_for_this_ghost += 1
                print("Dead = ", n_dead_for_this_ghost)
                # print("Maze - \n",maze)
                # print("path -> ",path)
            maze_end_time=time()
            file.write("\n\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
            # print("\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
                
        gh_end_time=time()
        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survived = %d" % n_alive_for_this_ghost+" ")
        file.write("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
        file.write("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
        file.write("\nGhost "+str(i_ghost+1)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
        print("\n\nReport for %d Number of Ghosts" % i_ghost)
        print("\nGhost "+str(i_ghost)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
        print("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" ")
        print("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
        print("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
    
    #  fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        csv_writer.writerow([time_now,i_ghost,10,str(gh_end_time-gh_st_time),str(n_alive_for_this_ghost),str(n_hanged_for_this_ghost),str(n_dead_for_this_ghost)])
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

# agent_three()

if __name__=="__main__":
    
    p_1_11 = mp.Process(target=agent_three,args=(11,11,"Process Test"))
    # p_21_31 = mp.Process(target=agent_three,args=(21,31,"Process 21 to 31"))
    # p_41_51 = mp.Process(target=agent_three,args=(41,51,"Process 41 to 51"))
    # p_61_71 = mp.Process(target=agent_three,args=(61,71,"Process 61 to 71"))
    
    # p_1_21 = mp.Process(target=agent_three,args=(1,21,"Process 1 to 21"))
    # p_31_51 = mp.Process(target=agent_three,args=(31,51,"Process 31 to 51"))
    # p_61_81 = mp.Process(target=agent_three,args=(61,81,"Process 61 to 81"))
    # p_91_111 = mp.Process(target=agent_three,args=(91,111,"Process 91 to 111"))
    
    p_1_11.start()
    # p_21_31.start()
    # p_41_51.start()
    # p_61_71.start()
    
    
    p_1_11.join()
    # p_21_31.join()
    # p_41_51.join()
    # p_61_71.join()
    # p_1_21.start()
    # p_31_51.start()
    # p_61_81.start()
    # p_91_111.start()

    # p_1_21.join()
    # print("Process 1 to 21 Joined")
    # p_31_51.join()
    # print("Process 31 to 51 Joined")
    # p_61_81.join()
    # print("Process 61 to 81 Joined")
    # p_91_111.join()
    # print("Process 91 to 111 Joined")
    

