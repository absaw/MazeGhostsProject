import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
import collections
# from collections import deque

def get_bfs_path(maze,n_row,n_col,start):
    # maze=[  [0,0,1,0,0],
    #         [0,0,1,0,0],
    #         [0,0,1,0,0],
    #         [1,0,1,1,0],
    #         [0,0,0,0,0]]
    # n_row=5
    # n_col=5
    walk = [[0, 1],
            [0,-1],
            [1, 0],
            [-1,0]]
    # maze_visited=np.zeros((n_row,n_col))

    # visited_set=set([(0,0)])
    visited_set=set([start])
    
    # visited_set.add((0,0))
    fringe_q=collections.deque([[start]])
    # fringe_q=collections.deque([[(0,0)]])
    # fringe_q.append([(0,0)])
    # path=[]
    path_found=False
    while(len(fringe_q)>0):
        path=fringe_q.popleft()
        # print("Type path ->",type(path))
        curr_x,curr_y=path[-1]
        # maze_visited[curr[0]][curr[1]]=1
        # maze[curr[0]][curr[1]]=-1
        if ((curr_x,curr_y)==(n_row-1,n_col-1)):
            # print("Path found")
            path_found=True
            break

        for i in range(4):
            # x=curr[0]+walk[i][0]  #traversing x column
            # y=curr[1]+walk[i][1]  #traversing y column
            x=curr_x+walk[i][0]
            y=curr_y+walk[i][1]
            if (x>=0 and x<n_row) and (y>=0 and y<n_col) and (maze[x][y]!=1) and (x,y) not in visited_set:
                # if (x>=0 and x<n_row) and (y>=0 and y<n_col) and (maze_visited[x,y]!=1):
                fringe_q.append(path+[(x,y)])
                # fringe_q.append((x,y))
                visited_set.add((x,y))
                # path.append((x,y))

        # print("Fringe - >",fringe_q)

    # print("Exited the While loop")

    if path_found:
        # print("Path found")
        # print("\n Path ->",path)
        return [path_found,path]
    else:
        # print("Path not found")
        return [path_found,None]

    # plt.imshow(maze,"Dark2")
    # plt.show()
# a=[ [0,0,1,0,0],
#     [0,0,0,0,0],
#     [0,1,1,1,0],
#     [1,1,1,1,0],
#     [0,0,0,0,0]]
# result=get_bfs_path(a,5,5,(2,0))
# print(result)
        


        