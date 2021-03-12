from operator import attrgetter

class Sever():
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


if __name__ =='__main__':
    A = []
    with open('./training-1.txt','r') as f:
        lines = f.readline()
        print(lines)
        severs = f.readlines()
        for i in range(int(lines)):
            sever = severs[i][1:-2].split(', ')
            print(sever)
            A.append(Sever(sever[0],int(sever[1]),int(sever[2]),int(sever[3]),int(sever[4])))

    A.sort(key=attrgetter('cores','mems','hard_cost','energy_cost'))

    for i in A:
        print('name:{}, cores:{}, mems:{}'.format(i.name,i.cores,i.mems))
