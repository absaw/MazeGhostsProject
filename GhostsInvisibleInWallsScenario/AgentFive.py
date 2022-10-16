 #=======Strategy of Agent 5========
 # INVISIBLE GHOSTS IN WALLS
 # ================================
# Calculate initial shortest path
# If path not valid i.e. there are ghosts in the path
#       If the nearest ghost is farther than a limit in the path
#           Start walking on the path
#       Else
#           Find run away cell for player
# For each step while walking in maze
# Check if died/survived
# Simulate ghosts
# Check if died/survived
# Strategize the following way:-
# Calculate nearest wall
# If it comes within our wall limit
#       Mark the surrounding 8 cells of ghost as blocked in maze_marked
#       Set wall condition to be true
# Calculate the nearest ghost to it
# If it comes within our run away limit, 
#       Mark the surrounding 8 cells of the ghost as blocked
#       Calculate a new latest path to the goal while keeping this new blocked maze in mind to avoid the ghost
#       If the path is valid
#           append the next cell to the path variable
#       Else
#           Calculate a running away cell from the ghost
#           Get a new latest path, while forgetting the ghosts, so that we can replan in the next step
# Else
#       If wall < wall limit--wallcondition
#       
#          Calculate a new latest path to the goal while keeping this new blocked maze in mind to avoid the ghost
#          If the path is valid
#              append the next cell to the path variable
#          Else
#              Calculate a running away cell from the ghost
#              Get a new latest path, while forgetting the ghosts, so that we can replan in the next step
#       Else
#          we stick to the current path
#       

import numpy as np
from CallableAgentTwo import *
from BFS import *
from Maze import *
# from GhostSimulation import *
from time import time
from datetime import datetime
import csv
import multiprocessing as mp

def intersection_list(l1,l2):
    return list(set(l1)&set(l2))

def get_wall_list(maze,n_row,n_col):
    wall_list=[]
    for row in range(0,n_row):
        for col in range(0,n_col):
            if maze[row][col]==1 or maze[row][col]>200:
                wall_list.append((row,col))
    
    return wall_list
    

def agent_four(n_gh_lb, n_gh_ub, ProcessName):
    start = time()
    n_row = 51
    n_col = 51
    no_of_mazes=1

    walk = [[0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [0, 0]]
    surrounding = [[0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [0, 0],
            [1,1],
            [-1,-1],
            [1,-1],
            [-1,1]]
            
    filename_txt="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentFive/Test.txt"
    filename_csv="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentFive/Test.csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    # fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
    # csv_writer.writerow(fields)
    time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
    text = "\n\n\n======  Start Time for "+ProcessName+"  =========->  " +time_now
    csv_writer.writerow(["Execution Started "+ProcessName])
    file.write(text)
    file.write("\nNo. of mazes for each ghost = "+str(no_of_mazes))
    for i_ghost in range(n_gh_lb, n_gh_ub+1,5):
        # try:
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
            wall_position=get_wall_list(maze,n_row,n_col)

            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col, ghost_position)

            get_init_path = get_bfs_path(maze, n_row, n_col, (0, 0), False)
            is_init_path_valid = get_init_path[0]
            path = list()
            init_path=get_init_path[1][1:] #excluding the first element i.e. 0,0 from the list
            if is_init_path_valid:
                path.append(init_path.pop(0))
            else:
                #find nearest ghost and run away
                ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                        walk, ghost_position, n_row, n_col, maze, 0, 0)
                path.append((play_next_r, play_next_c))

            latest_path=init_path.copy()
            goal_reached=False
            for play_pos_r, play_pos_c in path:
                
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

                # ===================================================================================================
                # This code will execute only if player hasn't yet died.
                # Now decide next step to be taken..This is where player strategizes
                # ===================================================================================================
                wall_limit=1
                nearest_wall_result=find_nearest_wall(maze,play_pos_r,play_pos_c,wall_position)
                nearest_wall_dist=nearest_wall_result[0]
                nearest_wall=nearest_wall_result[1]
                maze_marked = maze.copy()
                
                wall_condition=False
                
                if nearest_wall_dist<=wall_limit:
                    wall_condition=True
                    for i in range(9):
                        mark_r = nearest_wall[0]+surrounding[i][0]  # possible rows
                        mark_c = nearest_wall[1]+surrounding[i][1]  # possible columns
                        if 0 <= mark_r < n_row and 0 <= mark_c < n_col and (mark_r,mark_c)!=(play_pos_r,play_pos_c):
                            maze_marked[mark_r][mark_c]=1
                
                gh_maze_limit=2
                nearest_gh_maze_result=find_nearest_ghost(maze,play_pos_r,play_pos_c,ghost_position)
                nearest_gh_maze_dist=nearest_gh_maze_result[0]
                nearest_gh=nearest_gh_maze_result[1]

                if nearest_gh_maze_dist<=gh_maze_limit:
                    # maze_marked = maze.copy()
                    for i in range(9):
                        mark_r = nearest_gh[0]+surrounding[i][0]  # possible rows
                        mark_c = nearest_gh[1]+surrounding[i][1]  # possible columns
                        if 0 <= mark_r < n_row and 0 <= mark_c < n_col and (mark_r,mark_c)!=(play_pos_r,play_pos_c):
                            maze_marked[mark_r][mark_c]=1
                    
                    # Recalculate the new path
                    latest_path_result=get_bfs_path(maze_marked,n_row,n_col,(play_pos_r,play_pos_c),True)
                    
                    if latest_path_result[0]:
                        latest_path=latest_path_result[1][1:]
                        path.append(latest_path.pop(0))
                    else:
                        # start running away
                        ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                                walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                        path.append((play_next_r, play_next_c))
                        latest_path_result=get_bfs_path(maze,n_row,n_col,(play_next_r,play_next_c),False)
                        latest_path=latest_path_result[1][1:]
                else:
                    if wall_condition:
                        # Recalculate the new path
                        latest_path_result=get_bfs_path(maze_marked,n_row,n_col,(play_pos_r,play_pos_c),True)
                        
                        if latest_path_result[0]:
                            latest_path=latest_path_result[1][1:]
                            path.append(latest_path.pop(0))
                        else:
                            # start running away
                            ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                                    walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                            path.append((play_next_r, play_next_c))
                            latest_path_result=get_bfs_path(maze,n_row,n_col,(play_next_r,play_next_c),False)
                            latest_path=latest_path_result[1][1:]
                    else:
                        path.append(latest_path.pop(0))
                print("\n\nPast Player Pos",play_pos_r,play_pos_c)
                print("Current Path ->",path)
                # print("Marked Maze ->\n",maze_marked)
                # print("Normal Maze ->\n",maze)
                # print("Ghost ->",ghost_position)


            if is_player_alive and not is_player_hanged:
                n_alive_for_this_ghost += 1
            if is_player_alive and is_player_hanged:
                n_hanged_for_this_ghost+=1
            if not is_player_alive:
                n_dead_for_this_ghost += 1
            maze_end_time=time()
            file.write("\n\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
                
        gh_end_time=time()
        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survived = %d" % n_alive_for_this_ghost+" ")
        file.write("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
        file.write("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
        file.write("\nGhost "+str(i_ghost+1)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")

        print("\nGhost "+str(i_ghost)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
        print("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" ")
        

        #  fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
        csv_writer.writerow([time_now,i_ghost,1,str(gh_end_time-gh_st_time),str(n_alive_for_this_ghost),str(n_hanged_for_this_ghost),str(n_dead_for_this_ghost)])
        

        print("Number of Ghosts = ", i_ghost, " Done\n")
        # except:
        #     print("Error in gh no. = ",i_ghost)
        #     continue

    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")

agent_four(2,2,"Run")

def recalculate_path(maze,n_row,n_col,play_pos_r,play_pos_c,path,walk):
# Recalculate the new path
    latest_path_result=get_bfs_path(maze,n_row,n_col,(play_pos_r,play_pos_c),True)
    
    if latest_path_result[0]:
        latest_path=latest_path_result[1][1:]
        path.append(latest_path.pop(0))
    else:
        # start running away
        ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost(
                walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
        path.append((play_next_r, play_next_c))
        latest_path_result=get_bfs_path(maze,n_row,n_col,(play_next_r,play_next_c),False)
        latest_path=latest_path_result[1][1:]
    
    return latest_path




