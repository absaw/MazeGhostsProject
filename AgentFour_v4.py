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



def agent_four(n_gh_lb, n_gh_ub, ProcessName):
    start = time()
    # print("Started...")
    # n_ghost = 50
    n_row = 51
    n_col = 51
    no_of_mazes=100
    # walk = [[0, 1],
    #         [0, -1],
    #         [1, 0],
    #         [-1, 0],
    #         [0, 0]]
    walk = [[0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [0, 0]]
    ghost_surrounding = [[0, 1],
            [1, 0],
            [0, -1],
            [-1, 0],
            [0, 0],
            [1,1],
            [-1,-1],
            [1,-1],
            [-1,1]]
    # filename_txt="Results/AgentFour/Test.txt"
    filename_txt="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentFour/Testv2.txt"
    filename_csv="/Users/abhishek.sawalkar/Library/Mobile Documents/com~apple~CloudDocs/AI Project/MazeGhostsProject/Results/AgentFour/Testv2.csv"
    # filename_csv="Results/AgentFour/Test.csv"
    # filename_csv="Results/AgentFour/Multiprocessed/"+ProcessName+".csv"
    # filename_csv="Results/AgentFour/Multiprocessed/"+ProcessName+".csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
    # csv_writer.writerow(fields)
    time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
    text = "\n\n\n======  Start Time for "+ProcessName+"  =========->  " +time_now
    csv_writer.writerow(["Execution Started "+ProcessName])
    file.write(text)
    # file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = "+str(no_of_mazes))
    # file.write("\nNo. of simulations of agent 2 at each step = 5")
    for i_ghost in range(n_gh_lb, n_gh_ub+1,5):
        try:
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

                get_init_path = get_bfs_path(maze, n_row, n_col, (0, 0), False)
                is_init_path_valid = get_init_path[0]
                path = list()
                init_path=get_init_path[1][1:] #excluding the first element i.e. 0,0 from the list
                if is_init_path_valid:
                    path.append(init_path.pop(0))
                else:

                    #find nearest ghost and run away
                    ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost_in_maze(
                            walk, ghost_position, n_row, n_col, maze, 0, 0)
                    path.append((play_next_r, play_next_c))

                    ##calculate ghost on path distance
                    # We have the ghost_position and path. This condition entails that path has some ghost
                    # We calc the distance of the nearest ghost on the path. See if this exceeds the run away limit

                    #def calc ghostinpath():
                    #finding intersection between ghost position and path
                    # ghosts_in_path_list=intersection_list(init_path,ghost_position)

                    # nearest_gh_in_path=find_nearest_ghost_in_maze(0,0,ghosts_in_path_list)[0] #Distance to the nearest ghost(even in wall) returned

                    # if nearest_gh_in_path>5:
                    #     path.append(init_path.pop(0))
                    # else:
                    #     ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost_in_maze(
                    #         walk, ghost_position, n_row, n_col, maze, 0, 0)
                    #     path.append((play_next_r, play_next_c))


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

                    #=======Strategy of Agent 4========
                    # ghost in path runaway limit = 5
                    # ghost in maze runaway limit = 2
                    ## TODO think abt the case when both are same!

                    # Calculate the nearest ghost to it
                    # If it comes within our run away limit, 
                    #       we calc a new latest_path
                    #       append latest cell to path
                    #       If there is no path
                    #           we start running 
                    # Else
                    #       we stick to the current path
                    #       Calc nearest ghost in path
                    #       If nearest ghost in path < run away limit
                    #              we calc a new latest_path
                    #              append latest cell to path
                    #              If there is no path
                    #                   we start running 
                    # we start running away from this ghost(TBD---towards a nearer path?)
                    
                    # gh_path_limit=2
                    gh_maze_limit=2
                    nearest_gh_maze_result=find_nearest_ghost_in_maze(play_pos_r,play_pos_c,ghost_position)
                    nearest_gh_maze_dist=nearest_gh_maze_result[0]
                    nearest_gh=nearest_gh_maze_result[1]
                    maze_gh_copy=maze.copy()

                    # mark_nearest_gh_vicinity()

                    if nearest_gh_maze_dist<=gh_maze_limit:
                        # Recalculate the new path
                        maze_duplicate = maze.copy()
                        # for i in range(9):
                        #     # ghost_position_duplicate = ghost_position.copy()
                        #     mark_r = nearest_gh[0]+ghost_surrounding[i][0]  # possible rows
                        #     mark_c = nearest_gh[1]+ghost_surrounding[i][1]  # possible columns
                        #     if 0 <= mark_r < n_row and 0 <= mark_c < n_col:
                        #         maze_duplicate[mark_r][mark_c]=1
                        
                        latest_path_result=get_bfs_path(maze,n_row,n_col,(play_pos_r,play_pos_c),True)
                        # latest_path_result=get_bfs_path(maze_duplicate,n_row,n_col,(play_pos_r,play_pos_c),True)
                        
                        if latest_path_result[0]:
                            latest_path=latest_path_result[1][1:]
                            path.append(latest_path.pop(0))
                        else:
                            # start running away
                            ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost_in_maze(
                                    walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                            path.append((play_next_r, play_next_c))
                            latest_path_result=get_bfs_path(maze,n_row,n_col,(play_next_r,play_next_c),False)
                        # if latest_path_result[0]:
                            latest_path=latest_path_result[1][1:]
                        # else:
                            # latest_path=get_bfs_path(maze,n_row,n_col,(play_next_r,play_next_c),False)[1][1:]
                    else:
                        path.append(latest_path.pop(0))

                        # ghosts_in_path_list=intersection_list(latest_path,ghost_position)
                        # nearest_gh_in_path=find_nearest_ghost_in_maze(play_pos_r,play_pos_c,ghosts_in_path_list)[0]

                        # if nearest_gh_in_path>gh_path_limit:
                        #     path.append(latest_path.pop(0))
                        # else:
                        #     #Recalculate the new path
                        #     latest_path_result=get_bfs_path(maze,n_row,n_col,(play_pos_r,play_pos_c),True)
                        #     if latest_path_result[0]:
                        #         latest_path=latest_path_result[1][1:]
                        #         path.append(latest_path.pop(0))
                        #     else:
                        #         #start running away
                        #         ghost_position, maze, play_next_r, play_next_c, nearest_ghost = run_away_from_ghost_in_maze(
                        #                 walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c)
                        #         path.append((play_next_r, play_next_c))

                if is_player_alive and not is_player_hanged:
                    n_alive_for_this_ghost += 1
                    
                    # print("Alive=",n_alive_for_this_ghost)
                if is_player_alive and is_player_hanged:
                    n_hanged_for_this_ghost+=1
                    # print("Hanged=", n_hanged_for_this_ghost)
                if not is_player_alive:
                    n_dead_for_this_ghost += 1
                    # print("Dead = ", n_dead_for_this_ghost)
                maze_end_time=time()
                file.write("\n\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
                # print("\nMaze "+str(n_maze+1)+" Execution Time = "+str(maze_end_time-maze_st_time)+" s")
                    
            gh_end_time=time()
            file.write("\nReport for %d Number of Ghosts" % i_ghost)
            file.write("\nPlayer Survived = %d" % n_alive_for_this_ghost+" ")
            file.write("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
            file.write("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")
            file.write("\nGhost "+str(i_ghost+1)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")

            # print("\n\nReport for %d Number of Ghosts" % i_ghost)
            print("\nGhost "+str(i_ghost)+" Execution Time = "+str(gh_end_time-gh_st_time)+" s")
            print("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" ")
            # print("\nPlayer Hanged = %d" % n_hanged_for_this_ghost+" ")
            # print("\nPlayer Dead = %d" % n_dead_for_this_ghost+" ")

            #  fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
            time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
            csv_writer.writerow([time_now,i_ghost,1,str(gh_end_time-gh_st_time),str(n_alive_for_this_ghost),str(n_hanged_for_this_ghost),str(n_dead_for_this_ghost)])
            # file.write("\nDead Number-> %d"%n_dead_for_this_ghost)
            # print("Node Reached -> %d"%node_reached)
            # print("Dead = ",n_dead_for_this_ghost)
            # print("Dead at ",node_reached)

            print("Number of Ghosts = ", i_ghost, " Done\n")
        except:
            # print("Error = ",err)
            print("Error in gh no. = ",i_ghost)
            continue

    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")

agent_four(1,100,"Run")

if __name__=="mai_":
    
    p_1_11 = mp.Process(target=agent_four,args=(1,11,"Process 1 to 11"))
    p_21_31 = mp.Process(target=agent_four,args=(21,31,"Process 21 to 31"))
    p_41_51 = mp.Process(target=agent_four,args=(41,51,"Process 41 to 51"))
    p_61_71 = mp.Process(target=agent_four,args=(61,71,"Process 61 to 71"))
    p_81_91 = mp.Process(target=agent_four,args=(81,91,"Process 81 to 91"))
    p_101_111 = mp.Process(target=agent_four,args=(101,111,"Process 101 to 111"))
    
    # p_1_21 = mp.Process(target=agent_four,args=(1,21,"Process 1 to 21"))
    # p_31_51 = mp.Process(target=agent_four,args=(31,51,"Process 31 to 51"))
    # p_61_81 = mp.Process(target=agent_four,args=(61,81,"Process 61 to 81"))
    # p_91_111 = mp.Process(target=agent_four,args=(91,111,"Process 91 to 111"))
    
    p_1_11.start()
    p_21_31.start()
    p_41_51.start()
    p_61_71.start()
    p_81_91.start()
    p_101_111.start()
    
    
    p_1_11.join()
    print("Process 1 to 11 Joined")

    p_21_31.join()
    print("Process 21 to 31 Joined")

    p_41_51.join()
    print("Process 41 to 51 Joined")

    p_61_71.join()
    print("Process 61 to 71 Joined")

    p_81_91.join()
    print("Process 81 to 91 Joined")
    
    p_101_111.join()
    print("Process 101 to 111 Joined")

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
    

