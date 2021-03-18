#include <iostream>
#include <string>
#include <algorithm>
#include <map>
#include <vector>
using namespace std;

class Server
{
public:
    string name;
    int cores;
    int mems;
    int hc;
    int ec;
    double average_cores_hc, average_cores_ec, average_mems_hc, average_mems_ec;

public:
    Server(string name, int cores, int mems, int hc, int ec);
};

Server::Server(string name, int cores, int mems, int hc, int ec)
{
    this->name = name;
    this->cores = cores;
    this->mems = mems;
    this->hc = hc;
    this->ec = ec;
    this->average_cores_ec = ec * 1.0 / cores;
    this->average_cores_hc = hc * 1.0 / cores;
    this->average_mems_ec = ec * 1.0 / mems;
    this->average_mems_hc = hc * 1.0 / mems;
}

class VM
{

public:
    string name;
    int cores;
    int mems;
    int is_binode;
    VM(){}
    VM(string name, int cores, int mems, bool is_binode)
    {
        this->name = name;
        this->cores = cores;
        this->mems = mems;
        this->is_binode = is_binode;
    }
};

class RunningVM
{
public:
    string name;
    int cores;
    int mems;
    bool is_binode;
    int id;
    int running_server = -1;
    string running_node = "";

    RunningVM(){}
    RunningVM(VM vm, int id)
    {
        this->name = vm.name;
        this->cores = vm.cores;
        this->mems = vm.mems;
        this->is_binode = vm.is_binode;
        this->id = id;
    }

    void setrunningloc(int serverid, string node)
    {
        this->running_server = serverid;
        this->running_node = node;
    }
};

class RunningServer
{

public:
    string name;
    int cores;
    int mems;
    int id;
    int ec;
    int runningatA = -1;
    int runningatB = -1;
    RunningServer(Server server, int id)
    {
        this->name = server.name;
        this->cores = server.cores;
        this->mems = server.cores;
        this->ec = server.ec;
        this->id = id;
    }

    bool Ais_empty()
    {
        if (this->runningatA == -1)
            return true;
        else
            return false;
    }
    bool Bis_empty()
    {
        if (this->runningatB == -1)
            return true;
        else
            return false;
    }
    bool empty()
    {
        return this->Ais_empty() and this->Bis_empty();
    }

    void setrunningnode(int vmid, string node)
    {
        if (node == "A")
        {
            this->runningatA = vmid;
        }
        else if (node == "B")
        {
            this->runningatB = vmid;
        }
        else
        {
            this->runningatA = vmid;
            this->runningatB = vmid;
        }
    }

    void delrunningnode(string node)
    {
        if (node == "A")
        {
            this->runningatA = -1;
        }
        else if (node == "B")
        {
            this->runningatB = -1;
        }
        else
        {
            this->runningatA = -1;
            this->runningatB = -1;
        }
    }
};

class opt
{
public:
    string ope, vmname;
    int vmid;

    opt(string ope, string vmname, int vmid)
    {
        this->ope = ope;
        this->vmname = vmname;
        this->vmid = vmid;
    }
};

class Manager
{
public:
    map<string, VM> vm_list;
    vector<Server> server_list;
    vector<vector<opt>> allopts;
    int days;
    Manager()
    {
        std::ios::sync_with_stdio(false);
        int serverline;
        cin >> serverline;
        string server;
        int cores, mems, hc, ec;
        for (int i = 0; i < serverline; i++)
        {
            cin >> server;
            cin.get();
            cin >> cores;
            cin.get();
            cin >> mems;
            cin.get();
            cin >> hc;
            cin.get();
            cin >> ec;
            cin.get();
            server_list.push_back(Server(server.substr(1, server.length() - 2), cores, mems, hc, ec));
        }
        int vmlines;
        cin >> vmlines;
        string vm;
        bool isbinode;
        for (int i = 0; i < vmlines; i++)
        {
            cin >> vm;
            cin.get();
            cin >> cores;
            cin.get();
            cin >> mems;
            cin.get();
            cin >> isbinode;
            cin.get();
            vm_list[vm.substr(1, vm.length() - 2)] = VM(vm.substr(1, vm.length() - 2), cores, mems, isbinode);

        }
        cin >> days;
        for (int i = 0; i < days; i++)
        {
            int optnum;
            vector<opt> dailyopt;
            string op, vm;
            int id;
            cin >> optnum;
            cout << optnum<<endl;
            for (int j = 0; j < optnum; j++)
            {
                cin >> op;
                cin.get();
                string o = op.substr(1, op.length() - 2);
                if(o == "add"){
                    cin >> vm;
                    cin.get();
                    cin >> id;
                    cin.get();
                    dailyopt.push_back(opt(o, vm.substr(0,vm.length() - 1), id));
                }
                else{
                    cin >>id;
                    cin.get();
                    dailyopt.push_back(opt(o, "", id));
                }
                
            }
            allopts.push_back(dailyopt);
        }
    }

    VM find_vm_by_name(string vmname)
    {
        return vm_list[vmname];
    }

    static bool cmphc(Server &a, Server &b)
    {
        return a.hc<b.hc;
    }

    void sort_server_by_hc()
    {
        sort(server_list.begin(), server_list.end(), cmphc);
    }

    Server find_server(int cores, int mems)
    {
        for (Server s : server_list)
        {
            if (s.cores >= cores and s.mems >= mems)
            {
                return s;
            }
        }
        return server_list[0];
    }

    vector<opt> get_day_ops(int day)
    {
        return allopts[day];
    }

    int get_days()
    {
        return days;
    }
};

class Schedule
{
public:
    Manager manager;
    map<int, RunningVM> runningVM;
    vector<RunningServer> running_server;
    vector<RunningServer> free_server;

    Schedule(Manager manager)
    {
        this->manager = manager;
    }

    int server_cnt()
    {
        return running_server.size() + free_server.size();
    }

    string add_server_to_free(RunningServer server){
        free_server.push_back(server);
        return server.name +" "+to_string(server.id);
    }

    string add_server_to_running(RunningServer server){
        running_server.push_back(server);
        return server.name +" "+to_string(server.id);
    }

    RunningVM add_vm(RunningVM vm){
        runningVM[vm.id] = vm;
        return vm;
    }

    static bool cmpec(RunningServer &a, RunningServer &b){
        return a.ec < b.ec;
    }

    static bool cmpempty(RunningServer &a ,RunningServer &b){
        if(a.cores <= b.cores and (a.Ais_empty() or a.Bis_empty())){
            return true;
        }
        else if(a.cores > b.cores and (b.Ais_empty() or b.Bis_empty())){
            return false;
        }
        else return a.cores <b.cores;
    }

    void sort_free_server_by_ec(){
        sort(free_server.begin(),free_server.end(),cmpec);
    }

    void sort_running_server(){
        sort(running_server.begin(),running_server.end(),cmpempty);
    }

    int find_server_from_running_server(int cores,int mems){
        for(int i=0;i<running_server.size();i++){
            if((running_server[i].Ais_empty() or running_server[i].Bis_empty()) and running_server[i].cores >= cores and running_server[i].mems >= mems){
                return i;
            }
        }
        return -1;
    }

    int find_server_from_free_server(int cores , int mems){
        for(int i=0;i<free_server.size();i++){
            if(free_server[i].cores >= cores and free_server[i].mems >= mems){
                return i;
            }
        }
        return -1;
    }

    int find_free_server_by_id(int id){
        for(int i=free_server.size()-1;i>=0;--i){
            if(free_server[i].id == id){
                return i;
            }
        }
    }

    int find_running_server_by_id(int id){
        for(int i=running_server.size()-1;i>=0;--i){
            if(running_server[i].id == id){
                return i;
            }
        }
        return -1;
    }

    string add_svm_to_running_server(int vmid,int runningloc){
        int serverid = running_server[runningloc].id;
        string node ="";
        if(running_server[runningloc].Ais_empty()){
            node = "A";
        }
        else if(running_server[runningloc].Bis_empty()){
            node = "B";
        }
        else return "";
        runningVM[vmid].setrunningloc(serverid,node);
        running_server[runningloc].setrunningnode(vmid,node);
        return to_string(serverid)+":"+node;
    }

    string add_svm_from_free_server(int vmid,int serverid,int freeloc){
        string node ="";
        if(free_server[freeloc].Ais_empty())
            node = "A";
        else node = "B";

        runningVM[vmid].setrunningloc(serverid,node);
        free_server[freeloc].setrunningnode(vmid,node);
        running_server.push_back(free_server[freeloc]);
        free_server.erase(free_server.begin()+freeloc);
        return to_string(serverid)+":"+node;
    }

    string add_bsv_to_running_server(int vmid,int serverid,int serverloc){
        string node ="AB";
        runningVM[vmid].setrunningloc(serverid,node);
        free_server[serverloc].setrunningnode(vmid,node);
        running_server.push_back(free_server[serverloc]);
        free_server.erase(free_server.begin()+serverloc);
        return to_string(serverid);
    }

    void delvm(RunningVM vm){
        int serverid = vm.running_server;
        string node = vm.running_node;

        int serverloc =find_running_server_by_id(serverid);

        running_server[serverloc].delrunningnode(node);

        if(running_server[serverloc].empty()){
            free_server.push_back(running_server[serverloc]);
            running_server.erase(begin(running_server)+serverloc);
        }
    }

    vector<vector<string>> daily_report(int day){
        vector<opt> ops = manager.allopts[day];
        vector<vector<string>> ret;
        vector<string> bushu;
        vector<string> purchase;
        sort_free_server_by_ec();
        sort_running_server();
        for(int i=0;i<ops.size();i++){
            if(ops[i].ope=="add"){
                RunningVM vm = add_vm(RunningVM(manager.find_vm_by_name(ops[i].vmname),ops[i].vmid));
                if(vm.is_binode){
                    int loc = find_server_from_free_server(vm.cores,vm.mems);
                    if(loc>=0){
                        int serverid = free_server[loc].id;
                        bushu.push_back(add_bsv_to_running_server(vm.id,serverid,loc));
                    }
                    else{
                        RunningServer s =RunningServer(manager.find_server(vm.cores,vm.mems),server_cnt());
                        purchase.push_back(add_server_to_running(s));
                        runningVM[vm.id].setrunningloc(s.id,"AB");
                        bushu.push_back(to_string(s.id));
                    }
                }
                else{
                    int loc =find_server_from_running_server(vm.cores*2,vm.mems*2);
                    if(loc >=0){
                        bushu.push_back(add_svm_to_running_server(vm.id,running_server[loc].id));
                        continue;
                    }
                    int freeloc = find_server_from_free_server(vm.cores*2,vm.mems*2);
                    if(freeloc>=0){
                        bushu.push_back(add_svm_from_free_server(vm.id,free_server[freeloc].id,freeloc));
                    }
                    else{
                        RunningServer s = RunningServer(manager.find_server(vm.cores*2,vm.mems*2),server_cnt());
                        purchase.push_back(add_server_to_running(s));
                        runningVM[vm.id].setrunningloc(s.id,"A");
                        bushu.push_back(to_string(s.id)+":"+"A");
                    }

                    
                }
            }
            else{
                int sid = runningVM[ops[i].vmid].id;
                string node = runningVM[ops[i].vmid].running_node;
                int serverloc = find_running_server_by_id(sid);
                running_server[serverloc].delrunningnode(node);
                runningVM.erase(ops[i].vmid);
                if(running_server[serverloc].empty()){
                    free_server.push_back(running_server[serverloc]);
                    running_server.erase(begin(running_server)+serverloc);
                }
            }
        }
        ret.push_back(purchase);
        ret.push_back(bushu);
        
        return ret;
    }


};

int main()
{
    auto s = Schedule(Manager());
    int days = s.manager.get_days();
    for(int i=0;i<days;i++){
        s.daily_report(i);
    }
    return 0;
}