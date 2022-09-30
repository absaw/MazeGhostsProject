# Python3 program for the above approach
from collections import deque as queue
 
# Direction vectors
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]
 
# Function to check if a cell
# is be visited or not
def isValid(vis, row, col):
   
    # If cell lies out of bounds
    if (row < 0 or col < 0 or row >= 4 or col >= 4):
        return False
 
    # If cell is already visited
    if (vis[row][col]):
        return False
 
    # Otherwise
    return True
 
# Function to perform the BFS traversal
def BFS(grid, vis, row, col):
   
    # Stores indices of the matrix cells
    q = queue()
 
    # Mark the starting cell as visited
    # and push it into the queue
    q.append(( row, col ))
    vis[row][col] = True
 
    # Iterate while the queue
    # is not empty
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        print(grid[x][y], end = " ")
 
        #q.pop()
 
        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (isValid(vis, adjx, adjy)):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True
 
# Driver Code
if __name__ == '__main__':
   
    # Given input matrix
    grid= [ [ 1, 2, 3, 4 ],
           [ 5, 6, 7, 8 ],
           [ 9, 10, 11, 12 ],
           [ 13, 14, 15, 16 ] ]
 
    # Declare the visited array
    vis = [[ False for i in range(4)] for i in range(4)]
    # vis, False, sizeof vis)
 
    BFS(grid, vis, 0, 0)