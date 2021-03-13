from operator import attrgetter

class Server():
    def __init__(self,name ,cores ,mems, hard_cost, energy_cost):
        self.name =name 
        self.cores = cores 
        self.mems = mems
        self.hard_cost = hard_cost
        self.energy_cost = energy_cost
        self.average_core_hc =  hard_cost/cores
        self.average_mem_hc = hard_cost/mems
        self.average_core_ec = energy_cost/cores
        self.average_mem_ec = energy_cost/mems
        self.nodeA_busy = 0
        self.nodeB_busy = 0

    def setAstate(self,state:bool):
        self.nodeA_busy = state
    
    def setBstate(self,state:bool):
        self.nodeB_busy = state

    def __str__(self) -> str:
        return "SeverName:{}, cores:{}, mems:{}, hc:{}, ec:{}".format(self.name,self.cores,self.mems,self.hard_cost,self.energy_cost)

class VM():
    def __init__(self,name,cores,mems,binode) -> None:
        self.name = name
        self.cores = cores
        self.mems = mems
        self.is_binode = binode
        
    def __str__(self) -> str:
        return "VMname: {}, cores: {}, mems:{}, is_binode:{}".format(self.name,self.cores,self.mems,self.is_binode)
    

if __name__ =='__main__':
    A = []
    with open('./training-1.txt','r') as f:
        lines = f.readline()
        print(lines)
        severs = f.readlines()
        for i in range(int(lines)):
            server = severs[i][1:-2].split(', ')
            print(server)
            A.append(Server(server[0],int(server[1]),int(server[2]),int(server[3]),int(server[4])))

    A.sort(key=attrgetter('cores','mems','hard_cost','energy_cost'))

    for i in A:
        print('name:{}, cores:{}, mems:{}'.format(i.name,i.cores,i.mems))
