from Server import VM,Server

class RunningVM():
    def __init__(self,vm:VM,id) -> None:
        self.name = vm.name
        self.cores = vm.cores
        self.mems = vm.mems
        self.id = id
        self.running_server = 0   ##server id
        self.running_node = 0    ##node 1:singleA  2:singleB  3:binoode

    def setrunningloc(self,serverid,node):
        self.running_server = serverid
        self.running_node = node

class RunningServer():
    def __init__(self,server:Server,id) -> None:
        self.cores  = server.cores
        self.name = server.name
        self.mems = server.mems
        self.id = id
        self.ec = server.energy_cost
        self.runningatA = 0
        self.runningatB = 0
    @property
    def Ais_empty(self):
        return ~self.runningatA

    @property
    def Bis_empty(self):
        return ~self.runningatB
    
    
    def setrunningnode(self,nodeid,vmid):
        if nodeid ==1:
            self.runningatA = vmid
        elif nodeid ==2:
            self.runningatB = vmid
        else:
            self.runningatA =vmid
            self.runningatB =vmid
    
    def delrunningnode(self,nodeid):
        if nodeid ==1:
            self.runningatA = 0
        elif nodeid ==2:
            self.runningatB = 0
        else:
            self.runningatA =0
            self.runningatB =0
    
