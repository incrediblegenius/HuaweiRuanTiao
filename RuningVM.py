from Server import VM,Server

class RunningVM():
    def __init__(self,vm:VM,id) -> None:
        self.name = vm.name
        self.cores = vm.cores
        self.mems = vm.mems
        self.isbinode = vm.is_binode
        self.id = id
        self.running_server = ''  ##server id
        self.running_node = ''    ##node 'A':singleA  'B':singleB  'AB':binoode

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
        self.runningatA = ''
        self.runningatB = ''
    @property
    def Ais_empty(self):
        if self.runningatA == '':
            return 1
        else:
            return 0

    @property
    def Bis_empty(self):
        if self.runningatB == '':
            return 1
        else:
            return 0
    
    
    def setrunningnode(self,vmid,nodeid):
        if nodeid =='A':
            self.runningatA = vmid
        elif nodeid =='B':
            self.runningatB = vmid
        else:
            self.runningatA =vmid
            self.runningatB =vmid
    
    def delrunningnode(self,nodeid):
        if nodeid =='A':
            self.runningatA = ''
        elif nodeid =='B':
            self.runningatB = ''
        else:
            self.runningatA =''
            self.runningatB =''
    
