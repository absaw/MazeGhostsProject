from datetime import datetime
file=open("../Results/AgentOne.txt","a")

file.write("\nHello at  "+datetime.now().strftime("%m/%d/%y %H:%M:%S"))
file.write("hello %d at dfd"%4)
file.close()