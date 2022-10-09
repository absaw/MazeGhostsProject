import collections
import numpy as np

def get_traversal_table(maze,n_row,n_col,start,ghost_present):
       
    walk = [[0, 1],
            [0,-1],
            [1, 0],
            [-1,0]]

    visited_set=set([start])
    
    fringe_q=collections.deque([[start]])
    path_found=False

    visited_maze=np.zeros((n_row,n_col))
    # for i,j in visited_set:
    #     zero_maze[i][j]=1

    while(len(fringe_q)>0):
        path=fringe_q.popleft()
        curr_row,curr_col=path[-1]
        if ((curr_row,curr_col)==(0,0)):
            # Path found
            path_found=True
            break
        # print(type(path))
        for i in range(4):
            
            row=curr_row+walk[i][0]#traversing row column
            col=curr_col+walk[i][1]#traversing col column

            if (row>=0 and row<n_row) and (col>=0 and col<n_col) and (maze[row][col]!=1) and (row,col) not in visited_set:
                if not ghost_present:#for agent 1; when path without ghosts is calculated
                    fringe_q.append(path+[(row,col)])
                    visited_set.add((row,col))
                elif ghost_present and maze[row][col]<100:#ghost present and we need to avoid ghosts
                    fringe_q.append(path+[(row,col)])
                    visited_set.add((row,col))
                    visited_maze[row][col]=len(path)

        # print("Fringe - >",fringe_q)

    # print("Exited the While loop")
    # print(maze)
    # zero_maze=np.zeros((n_row,n_col))
    # for i,j in visited_set:
    #     zero_maze[i][j]=1
    
    # print(visited_maze)

    if path_found:
        return [path_found,visited_maze]
    else:
        return [path_found,None]

# a=np.array([[0,1,0,1,1],
#             [0,0,0,0,1],
#             [0,0,0,0,0],
#             [1,0,1,0,0],
#             [0,0,0,0,0]])

# a2=[[0,0,1,0,0],
#     [102,0,200,0,0],
#     [0,0,1,0,0],
#     [100,100,1,1,0],
#     [0,0,0,0,0]]

# result=get_traversal_table(a,5,5,(4,4),True)
# print(result)
        