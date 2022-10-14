import heapq as hq
from TraversalTable import *


class Node:

    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.actual_cost = self.heuristic_cost = self.total_cost = 0

    def __eq__(self, other):
        return self.pos == other.pos

    # def __repr__(self):
    #     return "{self.pos} - g:{self.g} h:{self.h} total_cost: {self.}

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost < other.total_cost


def return_path(curr):
    path = []
    c = curr

    while c is not None:
        path.append(c.pos)
        c = c.parent

    return path[::-1]  # reversing the list


def a_star(maze, lookup_table, n_row, n_col, start, end):

    st_n = Node(None, start)
    st_n.actual_cost = st_n.heuristic_cost = st_n.total_cost = 0

    end_n = Node(None, end)
    end_n.actual_cost = end_n.heuristic_cost = end_n.total_cost = 0

    fringe_heap = []
    visited_set = []

    hq.heapify(fringe_heap)
    hq.heappush(fringe_heap, st_n)

    walk = [[0, 1],
            [0, -1],
            [1, 0],
            [-1, 0]]

    while len(fringe_heap) > 0:

        c_n = hq.heappop(fringe_heap)
        visited_set.append(c_n)

        if c_n == end_n:
            return return_path(c_n)

        ch = []

        for i in range(4):
            next_n_r = c_n.pos[0]+walk[i][0]
            next_n_c = c_n.pos[1]+walk[i][1]

            if (0 <= next_n_r < n_row and 0 <= next_n_c < n_col and maze[next_n_r][next_n_c] != 1 and maze[next_n_r][next_n_c] < 100):
                ch_n = Node(c_n, (next_n_r, next_n_c))
                ch.append(ch_n)

        for successor in ch:

            if not len([k for k in visited_set if k == successor]) > 0:

                successor.actual_cost = c_n.actual_cost + 1
                # print(successor.pos[0],",",successor.pos[1])
                successor.heuristic_cost = lookup_table[successor.pos[0]][successor.pos[1]]
                successor.total_cost = successor.actual_cost + successor.heuristic_cost

                if not len([l for l in visited_set if successor.pos == l.pos and successor.actual_cost > l.actual_cost]) > 0:
                    hq.heappush(fringe_heap, successor)

    return None


a = np.array([[0, 1, 0, 1, 1],
              [0, 0, 1, 0, 1],
              [0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0]])

lookup_table = get_traversal_table(a,5,5,(4,4),True)[1]
path = a_star(a,lookup_table,5,5,(0,0),(4,4))
for i,j in path:
    a[i][j]=55
print(a)
print(path)