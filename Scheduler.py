from Server import Server
from RuningVM import RunningServer,RunningVM
from Manager import Manager
from operator import attrgetter

class Scheduler():
    def __init__(self,manager:Manager) -> None:
        self.running_server = []
        self.running_vm =[]
        self.free_server = []
        self.manager = manager
        self.serverid = 0
    @property
    def server_cnt(self):
        return len(self.free_server)+len(self.running_server)

    @property
    def running_server_cnt(self):
        return len(self.running_server)
    
    @property
    def running_vm_cnt(self):
        return len(self.running_vm)

    @property
    def free_server_cnt(self):
        return len(self.free_server)

    def add_server_to_free(self,server:RunningServer):
        self.free_server.append(server)
    
    def add_server_to_running(self,server:RunningServer):
        self.running_server.append(server)
    
    def add_vm(self,vm:RunningVM):
        self.running_vm.append(vm)
        return vm

    def sort_free_server_by_ec(self):
        self.free_server.sort(key=attrgetter('ec','cores','mems'))

    def sort_running_server_by_ec(self):
        self.running_server.sort(key=attrgetter('ec','cores','mems'))

    def find_server_from_running_server(self,cores,mems) -> int:
        for i in range(self.running_server_cnt):
            if self.running_server[i].cores >= cores and self.running_server[i].mems >= mems and (self.running_server[i].Ais_empty or self.running_server[i].Bis_empty):
                return i 
        return -1

    def find_server_from_free_server(self,cores,mems) -> int:
        for i in range(self.free_server_cnt):
            if self.free_server[i].cores >= cores and self.free_server[i].mems >= mems :
                return i 
        return -1
    
    def find_vm_by_id(self,id:str) -> int:
        for i in range(self.running_vm_cnt):
            if self.running_vm[i].id == id :
                return i
    
    def find_running_server_by_id(self,serverid):
        for i in range(self.running_server_cnt):
            if self.running_server[i].id == serverid :
                return i

    def find_free_server_by_id(self,serverid):
        for i in range(self.free_server_cnt):
            if self.free_server[i].id == serverid :
                return i

    def add_svm_to_running_server(self,vmid,serverid):
        i = self.find_vm_by_id(vmid)
        j = self.find_running_server_by_id(serverid)
        if self.running_server[j].Ais_empty :
            node = 'A'
        elif self.running_server[j].Bis_empty :
            node = 'B' 
        else:
            return False
        self.running_vm[i].setrunningloc(serverid,node)
        self.running_server[j].setrunningnode(vmid,node)
        return True

    def add_svm_from_free_server(self,vmid,serverid,freeloc):
        i = self.find_vm_by_id(vmid)
        if self.free_server[freeloc].Ais_empty :
            node = 'A'
        elif self.free_server[freeloc].Bis_empty :
            node = 'B' 
        else:
            return False
        self.running_vm[i].setrunningloc(serverid,node)
        self.free_server[freeloc].setrunningnode(vmid,node)
        server = self.free_server.pop(freeloc)
        self.running_server.append(server)
        return True

    def add_bsv_to_running_server(self,vmid,serverid,serverloc):
        i = self.find_vm_by_id(vmid)
        # j = self.find_free_server_by_id(serverid)
        node = 'AB'
        self.running_vm[i].setrunningloc(serverid,node)
        self.free_server[serverloc].setrunningnode(vmid,node)
        server = self.free_server.pop(serverloc)
        self.running_server.append(server)

    def addopt(self,vmname,vmid):
        vm = self.add_vm(RunningVM(self.manager.find_vm_by_name(vmname),vmid))
        if vm.isbinode:
            self.addbinode(vm)
        else:
            self.addsnode(vm)

    def delopt(self,vmid):
        vmloc = self.find_vm_by_id(vmid)
        vm = self.running_vm.pop(vmloc)
        self.delvm(vm)

    def delvm(self,vm:RunningVM):
        serverid  = vm.running_server
        node = vm.running_node


    def addbinode(self,vm:RunningVM):
        loc = self.find_server_from_free_server(vm.cores,vm.mems)
        if loc >0 :
            serverid = self.free_server[loc].id
            self.add_bsv_to_running_server(vm.id,serverid,loc)
        else:
            self.add_server_to_free(RunningServer(self.manager.find_server_by_hc(vm.cores,vm.mems),self.server_cnt))
            self.addbinode(vm)

    def addsnode(self,vm:RunningVM):
        runningloc = self.find_server_from_running_server(vm.cores,vm.mems)
        if runningloc>0:
            serverid = self.running_server[runningloc].id
            self.add_svm_to_running_server(vm.id,serverid)
            return 
        freeloc = self.find_server_from_free_server(vm.cores,vm.mems)
        if freeloc>0:
            serverid = self.free_server[freeloc].id
            self.add_svm_from_free_server(vm.id,serverid,freeloc)
        else:
            self.add_server_to_free(RunningServer(self.manager.find_server_by_hc(vm.cores,vm.mems),self.server_cnt))
            self.addsnode(vm)
