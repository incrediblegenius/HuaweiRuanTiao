from Server import Server,VM
from operator import attrgetter
import sys
class Manager():
    def __init__(self) -> None:
        self.server_list = []
        self.server_count = 0
        self.sortflag = ''
        self.vm_list = []
        self.vm_count = 0
        
        lines = sys.stdin.readline()
        # print(lines,type(lines))
        serverline = int(lines)
        # vmlines = int(lines[serverline+1])
        for i in range(serverline):
            a = sys.stdin.readline()
            server = a[1:-2].split(', ')    
            self.server_list.append(Server(server[0],int(server[1]),int(server[2]),int(server[3]),int(server[4])))
            self.server_count += 1
            self.sortflag = ''
        vmlines = int(sys.stdin.readline())
        for i in range(vmlines):
            a = sys.stdin.readline()
            vm = a[1:-2].split(', ')
            self.vm_list.append(VM(vm[0],int(vm[1]),int(vm[2]),int(vm[3])))
            self.vm_count += 1
        self.days = int(sys.stdin.readline())
        self.ops =[]

        for i in range(self.days):
            day =[]
            ops_num = int(sys.stdin.readline())
            for j in range(ops_num):
                a = sys.stdin.readline()
                day.append(a[1:-2].split(', '))
            self.ops.append(day)
        # print(self.days)
        # print(self.ops[0])

    # def addServer(self,server:Server):
    #     self.server_list.append(server)
    #     self.server_count += 1
    #     self.sortflag = ''
        
    # def addVM(self,vm:VM):
    #     self.vm_list.append(vm)
    #     self.vm_count += 1
    
    def find_vm_by_name(self,name)->VM:
        for i in self.vm_list:
            if i.name == name:
                return i
        
    def find_server_by_hc(self,cores:int,mems:int)->Server:
        if self.sortflag != 'hc':
            self.server_list.sort(key=attrgetter('hard_cost','energy_cost','cores','mems'))
            self.sortflag ='hc'
        for i in self.server_list:
            if i.cores >=cores and i.mems >=mems :
                return i
    
    def find_server_by_ec(self,cores:int,mems:int)->Server:
        if self.sortflag != 'ec':
            self.server_list.sort(key=attrgetter('energy_cost','hard_cost','cores','mems'))
            self.sortflag ='ec'
        for i in self.server_list:
            if i.cores >=cores and i.mems >=mems :
                return i


    def find_server_by_hc_list(self,cores:int,mems:int,length:int) :
        if self.sortflag != 'hc':
            self.server_list.sort(key=attrgetter('hard_cost','energy_cost','cores','mems'))
            self.sortflag ='hc'
        ret = []
        cnt = 0
        for i in self.server_list:
            if i.cores >= cores and i.mems >= mems:
                ret.append(i)
                cnt += 1
                if cnt == length:
                    break
        return ret
    
    def get_day_ops(self,day:int): ######start with 0
        return self.ops[day]

    def get_all_ops(self):
        return self.ops

    def get_days(self)->int:
        return self.days

    def find_server_by_ec_list(self,cores:int,mems:int,length:int) :
        if self.sortflag != 'ec':
            self.server_list.sort(key=attrgetter('energy_cost','hard_cost','cores','mems'))
            self.sortflag ='ec'
        ret = []
        cnt = 0
        for i in self.server_list:
            if i.cores >= cores and i.mems >= mems:
                ret.append(i)
                cnt += 1
                if cnt == length:
                    break
        return ret

    def __str__(self) -> str:
        return 'There are {} servers, and {} virtual machines'.format(self.server_count,self.vm_count)

if __name__ =='__main__':
    manager = Manager()
    a = manager.find_vm_by_name('vmSQCQ3')
    b = manager.find_server_by_hc_list(200,200,5)
    print(a)
    for i in b:
        print(i)
    print(manager)
