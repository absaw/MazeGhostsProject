from datetime import datetime
import numpy as np
def file():
    file = open("../Results/AgentOne.txt", "a")

    file.write("\nHello at  "+datetime.now().strftime("%m/%d/%y %H:%M:%S"))
    file.write("hello %d at dfd" % 4)
    file.close()


def min_dist():
    min_dist = 10000
    play_pos_r=play_pos_c=0
    ghost_position=[(3,4),(2,3),(6,8),(1,1)]
    min_gh_r=ghost_position[0][0]
    min_gh_c=ghost_position[0][1]
    for gh_r, gh_c in ghost_position:
        curr_dist = np.sqrt((gh_r-play_pos_r)**2+(gh_c-play_pos_c)**2)
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_gh_r = gh_r
            min_gh_c = gh_c
    print("Min Dist = ",min_dist)
    print("Co-Ordinates = ",min_gh_r,", ", min_gh_c)

# min_dist()

def brkTwo():

    for i in range(0,5):
        for j in range(0,5):
            print(i,j)
            if j==2:
               break
         
brkTwo()