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
        purchase.append("{}:{}".format(server.name,server.id))
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
        self.sort_free_server_by_ec()
        for i in range(self.free_server_cnt):
            if self.free_server[i].cores >= cores and self.free_server[i].mems >= mems :
                return i 
        return -1
    
    def find_vm_by_id(self,id:str) -> int:
        for i in range(self.running_vm_cnt-1,-1,-1):
            if self.running_vm[i].id == id :
                return i
    
    def find_running_server_by_id(self,serverid):
        for i in range(self.running_server_cnt-1,-1,-1):
            if self.running_server[i].id == serverid :
                return i
 
    def find_free_server_by_id(self,serverid):
        for i in range(self.free_server_cnt-1,-1,-1):
            if self.free_server[i].id == serverid :
                return i

    def add_svm_to_running_server(self,vmid,ruuningloc):
        i = self.find_vm_by_id(vmid)
        serverid = self.running_server[ruuningloc].id
        # j = self.find_running_server_by_id(serverid)
        if self.running_server[ruuningloc].Ais_empty :
            node = 'A'
        elif self.running_server[ruuningloc].Bis_empty :
            node = 'B' 
        else:
            return False
        self.running_vm[i].setrunningloc(serverid,node)
        self.running_server[ruuningloc].setrunningnode(vmid,node)
        bushu.append("{}:{}".format(serverid,node))
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
        bushu.append("{}:{}".format(serverid,node))
        return True

    def add_bsv_to_running_server(self,vmid,serverid,serverloc):
        i = self.find_vm_by_id(vmid)
        # j = self.find_free_server_by_id(serverid)
        node = 'AB'
        self.running_vm[i].setrunningloc(serverid,node)
        self.free_server[serverloc].setrunningnode(vmid,node)
        server = self.free_server.pop(serverloc)
        self.running_server.append(server)
        bushu.append("{}".format(serverid))
        

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
        serverloc = self.find_running_server_by_id(serverid)
        
        self.running_server[serverloc].delrunningnode(node)
        
        if self.running_server[serverloc].Ais_empty and self.running_server[serverloc].Bis_empty :
            server = self.running_server.pop(serverloc)
            self.free_server.append(server)

    def addbinode(self,vm:RunningVM):
        loc = self.find_server_from_free_server(vm.cores,vm.mems)
        if loc >=0 :
            serverid = self.free_server[loc].id
            self.add_bsv_to_running_server(vm.id,serverid,loc)
        else:
            self.add_server_to_free(RunningServer(self.manager.find_server_by_hc(vm.cores,vm.mems),self.server_cnt))
            self.addbinode(vm)

    def addsnode(self,vm:RunningVM):
        runningloc = self.find_server_from_running_server(vm.cores,vm.mems)
        if runningloc>=0:
            serverid = self.running_server[runningloc].id
            self.add_svm_to_running_server(vm.id,runningloc)
            return 
        freeloc = self.find_server_from_free_server(vm.cores,vm.mems)
        if freeloc>=0:
            serverid = self.free_server[freeloc].id
            self.add_svm_from_free_server(vm.id,serverid,freeloc)
        else:
            self.add_server_to_free(RunningServer(self.manager.find_server_by_hc(vm.cores*2,vm.mems*2),self.server_cnt))
            self.addsnode(vm)

    # def daily_opt(self,day:int):
    #     purchase = []
    #     bushu = []
    #     opt = self.manager.get_day_ops(day)
    #     for i in range(len(opt)):
    #         if i[0] == 'add':
    #             self.addopt(i[i],i[2])
    #         elif i[0] == 'del':
    #             self.delopt(i[1])
        
if __name__ =='__main__':

    manager = Manager()
    scheduler = Scheduler(manager)
    days = scheduler.manager.get_days()
    ids = 0
    dic ={}
    for i in range(days):
        purchase = []
        bushu = []
        opt = manager.get_day_ops(i)
        for j in opt:
            if j[0] == 'add':
                scheduler.addopt(j[1],j[2])
            elif j[0] =='del':
                scheduler.delopt(j[1])
        name = []
        purchase.sort()
        for i in purchase:
            a = i.split(':')
            name.append(a[0])
            dic[a[1]] = ids
            ids += 1
        print("(purchase, {})".format(len(set(name))))
        for i in set(name):
            print("({}, {})".format(i,name.count(i)))
        
        print("(migratiion, 0)")
        for i in bushu:
            if ':' not in i:
                print("({})".format(dic[i]))
            else:
                a = i.split(':')
                print("({}, {})".format(dic[a[0]],a[1]))

    # print(scheduler.running_server[0].runningatA,scheduler.running_server[0].runningatB)
