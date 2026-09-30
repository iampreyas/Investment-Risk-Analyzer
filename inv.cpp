#include<iostream.h>
class investment
{
    int id;
    float amount;
    void input()
    {
        cout<<"Enter Investment ID:";
        cin>>id;
        cout<<"Enter Amount:";
        cin>>amount;
    }
    void display()
    {
        cout<<"\Investment ID:"<<id;
        cout<<"\nAmount: Rs."<<amount;
    }
};
int main()
{
    clrscr();
    investment inv;
    inv.input();
    inv.display();
    return 0;
}