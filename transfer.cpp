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
            for (int j = 0; j < optnum; j++)
            {
                cin >> op;
                cin.get();
                cin >> vm;
                cin.get();
                cin >> id;
                cin.get();
                dailyopt.push_back(opt(op.substr(1, op.length() - 2), vm.substr(0, vm.length() - 1), id));
            }
            allopts.push_back(dailyopt);
        }
    }

    VM find_vm_by_name(string vmname)
    {
        return vm_list[vmname];
    }

    static bool cmphc(Server a, Server b)
    {
        if (a.hc < b.hc)
            return true;
        if (a.ec < b.ec)
            return true;
        if (a.cores < b.cores)
            return true;
        if (a.mems < b.mems)
            return true;
        return false;
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
    }

    auto get_day_ops(int day)
    {
        return allopts[day];
    }

    int get_days()
    {
        return days;
    }
};

// class Schedule
// {
// public:
//     Manager manager;
//     map<int, RunningVM> runningVM;
//     vector<RunningServer> running_server;
//     vector<RunningServer> free_server;

//     Schedule(Manager manager)
//     {
//         this->manager = manager;
//     }

//     int server_cnt()
//     {
//         return running_server.size() + free_server.size();
//     }
// };

int main()
{
    auto s = Manager();
    return 0;
}