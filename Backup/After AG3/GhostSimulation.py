import random
import numpy as np
from Maze import flood_fill


def ghost_simulation(walk, ghost_position, n_row, n_col, maze):

    next_ghost_position = list()

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

        did_ghost_move = move_to_next_cell(maze, row_move, col_move)
        # if it moved, update ghost_list, reset prev cell
        if did_ghost_move:
            reset_prev_cell(maze, row, col)
            next_ghost_position.append((row_move, col_move))
        else:
            next_ghost_position.append((row, col))

    ghost_position = next_ghost_position.copy()
    return maze, ghost_position


def spawn_ghosts(maze, n_ghost, n_row, n_col, ghost_position):
    # ghost_position = list()
    # Spawning Ghosts at random location
    filled_maze=maze.copy()
    filled_maze=flood_fill(filled_maze,n_row,n_col,0,0)

    for i in range(n_ghost):

        cellFound=False
        while not cellFound:
            row = random.randint(1, n_row-1)
            col = random.randint(1, n_col-1)
            if filled_maze[row][col]==55:
                cellFound=True

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
    did_ghost_move = False
    # Empty Space--0->100
    if maze[row_move][col_move] == 0:
        maze[row_move][col_move] = 100
        did_ghost_move = True
    # Wall--1->200
    elif maze[row_move][col_move] == 1 and move:
        maze[row_move][col_move] = 200
        did_ghost_move = True
    # Empty space with ghost
    elif 100 <= maze[row_move][col_move] < 200:
        maze[row_move][col_move] += 1
        did_ghost_move = True
    # Wall with Ghost
    elif maze[row_move][col_move] >= 200 and move:
        maze[row_move][col_move] += 1
        did_ghost_move = True

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


def find_nearest_ghost(play_pos_r, play_pos_c, ghost_position):
    min_dist = 1000  # Some initial high value
    # play_pos_r=play_pos_c=0
    # ghost_position=[(3,4),(2,3),(6,8),(1,1)]
    min_gh_r = ghost_position[0][0]
    min_gh_c = ghost_position[0][1]
    for gh_r, gh_c in ghost_position:
        curr_dist = euclidean_distance(play_pos_r, play_pos_c, gh_r, gh_c)
        # curr_dist = np.sqrt((gh_r-play_pos_r)**2+(gh_c-play_pos_c)**2)
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_gh_r = gh_r
            min_gh_c = gh_c
    # print("Min Dist = ",min_dist)
    # print("Co-Ordinates = ",min_gh_r,", ", min_gh_c)
    return min_dist, (min_gh_r, min_gh_c)


def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2+(y1-y2)**2)


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1-x2)+abs(y2-y1)


def count_ghosts(maze, n_row, n_col):
    k = 0
    for i in range(0, n_row):
        for j in range(0, n_col):
            if maze[i][j] >= 100:
                k += 1
                print("\n Ghost value--", maze[i][j])
    print("                             No. of ghosts currently = ", k)
    return k


def run_away_from_ghost(walk, ghost_position, n_row, n_col, maze, play_pos_r, play_pos_c):
    nearest_ghost = find_nearest_ghost(play_pos_r, play_pos_c, ghost_position)[1]
    max = 0  # some low value
    # play_next_r=-1
    # play_next_c=-1
    for i in range(0, 4):
        next_pos_r = play_pos_r+walk[i][0]  # next possible row
        next_pos_c = play_pos_c+walk[i][1]  # next possible column
        # must be inside grid
        if 0 <= next_pos_r < n_row and 0 <= next_pos_c < n_col and maze[next_pos_r][next_pos_c] != 1:
            dist_frm_ghost = euclidean_distance(
                next_pos_r, next_pos_c, nearest_ghost[0], nearest_ghost[1])
            if dist_frm_ghost >= max:
                max = dist_frm_ghost
                play_next_r = next_pos_r  # player's next row
                play_next_c = next_pos_c  # player's next column

    return ghost_position, maze, play_next_r, play_next_c, nearest_ghost
