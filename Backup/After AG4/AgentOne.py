import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import collections
from GhostSimulation import *
from BFS import *
from Maze import *
# from BFS import get_bfs_path
from Maze import generate_maze
from time import time
from datetime import datetime
import csv
# 0   = Empty Space
# 1   = Blocked Wall
# 100 = Empty Space with ghost
# 200 = Blocked Wall with ghost


def agent_one():
    start = time()
    print("Started...")

    n_ghost = 200
    n_row = 51
    n_col = 51
    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]
    filename_txt="Results/AgentOne/Run 1.txt"
    filename_csv="Results/AgentOne/Run 1.csv"
    file=open(filename_txt,"a")
    csvfile = open(filename_csv, "a")
    csv_writer=csv.writer(csvfile)
    fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
    csv_writer.writerow(fields)

    file = open("Results/AgentOne.txt", "a")
    text = "\n\n\n======  Start Time  =========->  " + \
        datetime.now().strftime("%m/%d/%y %H:%M:%S")
    csv_writer.writerow(["Execution Started Run 1"])
    
    file.write(text)
    file.write("\nNo. of Ghosts = %d" % n_ghost)
    file.write("\nNo. of mazes for each ghost = 100")

    for i_ghost in range(1, n_ghost+1, 5):
        gh_st_time = time()
        n_maze = 100
        n_alive_for_this_ghost = 0
        print("Ghost Number ", i_ghost, " Started")
        while (n_maze > 0):
            n_maze -= 1
            maze_generator_result = generate_maze(n_row, n_col, False)
            maze = maze_generator_result[0]
            path = maze_generator_result[1]
            ghost_position = list()
            # Spawning Ghosts at random location
            spawn_ghosts(maze, i_ghost, n_row, n_col, ghost_position)
            # ghosts now present in maze. Now start walking

            for play_pos_r, play_pos_c in path:
                # Simulate movement for ghost
                is_player_alive = True
                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    break
                # ===============================Ghost Simulation=========================================================================
                maze, ghost_position = ghost_simulation(
                    walk, ghost_position, n_row, n_col, maze)
                # ===========================================================================

                if maze[play_pos_r][play_pos_c] >= 100:
                    # player dies
                    is_player_alive = False
                    break
                if (play_pos_r, play_pos_c) == (n_row-1, n_col-1):
                    # player survives
                    break

            if is_player_alive:
                # Alive
                n_alive_for_this_ghost += 1

        file.write("\nReport for %d Number of Ghosts" % i_ghost)
        file.write("\nPlayer Survivability = %d" % n_alive_for_this_ghost+" %")
        time_now=datetime.now().strftime("%m/%d/%y %H:%M:%S")
    #  fields=['Date Time','Ghost Number','Maze Number','Time Taken','Survived','Hanged','Died','Comments']
        gh_end_time=time()
        
        csv_writer.writerow([time_now,i_ghost,100,str(gh_end_time-gh_st_time),str(n_alive_for_this_ghost),0,str(100-n_alive_for_this_ghost)])
        
    end = time()
    file.write("\n\nExecution Time = "+str(end-start)+" s")
    print("Execution time : "+str(end-start)+" s")
    file.close()
    print("Done!")


agent_one()
