import BFS,Maze
from AgentOne import agent_one
def main():
    print("Welcome!")
    print("\nEnter 1 for Agent 1 , 2 for Agent 2 and so on")
    inp=input("Enter an input ")

    if inp==1:
        agent_one()
    # elif inp==2:
        # agent_two()
    
    
if __name__=="__main__":
    main()
    
    



