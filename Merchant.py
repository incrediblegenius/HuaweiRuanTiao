from Sever import Sever
from operator import attrgetter
class Merchant():

    def __init__(self) -> None:
        self.server_list = []
        self.server_count = 0
        self.sortflag = ''
    def add(self,server:Sever):
        self.server_list.append(server)
        self.server_count += 1
        self.sortflag = ''
        

    def find_by_hc(self,cores:int,mems:int)->Sever:
        if self.sortflag != 'hc':
            self.server_list.sort(key=attrgetter('hard_cost','energy_cost','cores','mems'))
            self.sortflag ='hc'
        for i in self.server_list:
            if i.cores >cores and i.mems >mems :
                return i
    
    def find_by_ec(self,cores:int,mems:int)->Sever:
        if self.sortflag != 'ec':
            self.server_list.sort(key=attrgetter('energy_cost','hard_cost','cores','mems'))
            self.sortflag ='ec'
        for i in self.server_list:
            if i.cores >cores and i.mems >mems :
                return i


    def find_by_hc_list(self,cores:int,mems:int,length:int) :
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
        

    def find_by_ec_list(self,cores:int,mems:int,length:int) :
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

if __name__ =='__main__':
    merchant = Merchant()
    with open('./training-1.txt','r') as f:
        lines = f.readline()
        severs = f.readlines()
        for i in range(int(lines)):
            sever = severs[i][1:-2].split(', ')
            
            merchant.add(Sever(sever[0],int(sever[1]),int(sever[2]),int(sever[3]),int(sever[4])))
            hcf = merchant.find_by_hc_list(300,300,10)
            ecf = merchant.find_by_ec_list(300,300,10)

        for i in hcf:
            print(i)
        for i in ecf:
            print(i)
    