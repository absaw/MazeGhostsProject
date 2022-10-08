import random
def ghost_simulation():
    for row, col in ghost_position:
        
        cell_found = False
        while(not cell_found):
            random_direction = random.randint(0, 3)
            row_move = row+walk[random_direction][0]
            col_move = col+walk[random_direction][1]

            if (0 <= row_move < n_row) and (0 <= col_move < n_col):
                cell_found = True

        # print("\n\nGhost -> ", row, col, " - > ", row_move, col_move)
        # print(maze, "\n")
        
        did_ghost_move=move_to_next_cell(maze, row_move, col_move)
        #if it moved, update ghost_list, reset prev cell
        if did_ghost_move:
            reset_prev_cell(maze, row, col)
            next_ghost_position.append((row_move,col_move))
        else:
            next_ghost_position.append((row,col))

def spawn_ghosts(maze, n_ghost, n_row, n_col,ghost_position):
    # ghost_position = list()
    # Spawning Ghosts at random location
    for i in range(n_ghost):
        row = random.randint(1, n_row-1)
        col = random.randint(1, n_col-1)
        ghost_position.append((row, col))

        # Ghost present at open space
        if maze[row][col] == 0:
            maze[row][col] = 100

        # Ghost present in wall
        elif maze[row][col] == 1:
            maze[row][col] = 200

        # More than one ghost present at open space
        elif 100 <= maze[row][col] < 200:
            maze[row][col] += 1

        # More than one ghost present in wall
        elif maze[row][col] >= 200:
            maze[row][col] += 1


def move_to_next_cell(maze, row_move, col_move):
    move = random.random() >= 0.5
    did_ghost_move=False
    # Empty Space--0->100
    if maze[row_move][col_move] == 0:
        maze[row_move][col_move] = 100
        did_ghost_move=True
    # Wall--1->200
    elif maze[row_move][col_move] == 1 and move:
        maze[row_move][col_move] = 200
        did_ghost_move=True
    # Empty space with ghost
    elif 100 <= maze[row_move][col_move] < 200:
        maze[row_move][col_move] += 1
        did_ghost_move=True
    # Wall with Ghost
    elif maze[row_move][col_move] >= 200 and move:
        maze[row_move][col_move] += 1
        did_ghost_move=True

    return did_ghost_move

def reset_prev_cell(maze, row, col):
    if (100 < maze[row][col] < 200):
        maze[row][col] -= 1

    elif(maze[row][col] > 200):
        maze[row][col] -= 1

    elif (maze[row][col] == 100):
        maze[row][col] = 0

    elif (maze[row][col] == 200):
        maze[row][col] = 1
