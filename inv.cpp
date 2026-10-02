#include<iostream.h>
class investment
{
    protected:
        int id;
        char name[10];
        float amount,rate;
    public:
    void input()
    {
        cout<<"Enter Investment ID:";
        cin>>id;
        cout<<"Enter Investment Name:"
        cin>>name;
        cout<<"Enter Amount:";
        cin>>amount;
        cout<<"Enter Expected Return Rate (%):";
        cin>>rate;
    }
    void display()
    {
        cout<<"\nInvestment ID:"<<id;
        cout<<"\nName:"<<name;
        cout<<"\nAmount: Rs."<<amount;
        cout<<"\nRate:"<<rate<<"%";
    }
    int display()
    {
        cout<<"\nID :"<<id;
        cout<<"\nName :"<<name;
        cout<<"\nAmount :Rs. "<<amount;
        cout<<"\nRate :"<<rate<<" %";
    }
    int getID()
    {
        return id;
    }
    float getAmount()
    {
        return amount;
    }
};
int main()
{
    clrscr();
    investment inv;
    inv.input();
    inv.display();
    inv.calculateReturn();
    return 0;
}