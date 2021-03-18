#include<iostream>
#include<string>
#include<map>
using namespace std;


int main(){
    // map<string,int> m;
    // m["123"] = 1;
    // m["111"] = 2;
    // cout << m["111"]<<endl;
    std::ios::sync_with_stdio(false);
    // int vmlines;
    // cin >> vmlines;
    // string vm;
    // int cores,mems;
    // bool isbinode;
    // cin>>vm;
    // cin.get();
    // cin >> cores;
    // cin.get();
    // cin >> mems;
    // cin.get();
    // cin >> isbinode;
    // cin.get();
    // cout << vm.substr(1,vm.length()-2) <<cores<<mems<<isbinode<<endl;
    // string opt,vm;
    // int id;
    // cin>>opt;
    // cin.get();
    // cin>>vm;
    // cin.get();
    // cin>>id;
    // cin.get();


    // cin>>opt;
    // cin.get();
    // cin>>vm;
    // cin.get();
    // cin>>id;
    // cin.get();
    // cout<<opt.substr(1,opt.length()-2) <<vm.substr(0,vm.length()-1)<<id<<endl;
    // int serverline;
    // cin >> serverline;
    // cout << serverline<<endl;
    // string s;
    // int cores,mems,hc,ec;
    // cin >> s;
    // cin.get();
    // cin>>cores;
    // cin.get();
    // cin>>mems;
    // cin.get();
    // cin>>hc;
    // cin.get();
    // cin>>ec;
    // cin.get();
    // cout << s.substr(1,s.length()-2) <<cores<<mems<<hc<<ec<<endl;
    string op, vm;
    int id;
    cin >> op;
    cin.get();
    string o = op.substr(1, op.length() - 2);
    if(o == "add"){
        cin >> vm;
        cin.get();
        cin >> id;
        cin.get();
        cout << o<<" "<<vm.substr(0,vm.length()-1) <<" "<< id;
    }
    else{
        cin >>id;
        cin.get();
        cout << o<<" "<< id;
    }

    cin >> op;
    cin.get();
    o = op.substr(1, op.length() - 2);
    if(o == "add"){
        cin >> vm;
        cin.get();
        cin >> id;
        cin.get();
        cout << o<<" "<<vm.substr(0,vm.length()-1) <<" "<< id;
    }
    else{
        cin >>id;
        cin.get();
        cout << o<<" "<< id;
    }
                
    return 0;
}