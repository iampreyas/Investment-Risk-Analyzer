#include<iostream>
#include<fstream>
using namespace std;
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
        cout<<"Enter Investment Name:";
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
    int getID()
    {
        return id;
    }
    float getAmount()
    {
        return amount;
    }
    void addAmount()
    {
        float money;
        cout<<"\nEnter Amount to Invest More : ";
        cin>>money;
        amount = amount+money;
        cout<<"\nInvestment Updated Successfully!";
    }
    void returnAmount()
    {
        float profit;
        profit = amount * rate/100;
        cout<<"\nExpected Return : Rs. "<<profit;
    }
    void save()
    {
        ofstream file("investment.txt",ios::app);
        file<<id<<" "<<name<<" "<<amount<<" "<<rate<<endl;
        file.close();
    }
};
class stock : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Stock";
    }
    void risk()
    {
        cout<<"\nRisk Level : High";
    }
};
class mutualfund : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Mutual Fund";
    }
    void risk()
    {
        cout<<"\nRisk Level : Medium";
    }
};
class fixeddeposit : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Fixed Deposit";
    }
    void risk()
    {
        cout<<"\nRisk Level : Low";
    }
};
class gold : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Gold";
    }
    void risk()
    {
        cout<<"\nRisk Level : Medium";
    }
};
class crypto : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Cryptocurrency";
    }
    void risk()
    {
        cout<<"\nRisk Level : Very High";
    }
};
class forex : public investment
{
    public:
    void type()
    {
        cout<<"\nInvestment Type : Forex";
    }
    void risk()
    {
        cout<<"\nRisk Level : High";
    }
};
void addInvestment(investment inv[],int &n)
{
    inv[n].input();
    inv[n].save();
    n++;
    cout<<"\nInvestment Added Successfully!";
}
void displayInvestment(investment inv[],int n)
{
    int i;
    if(n==0)
    {
        cout<<"\nNo Investment Found!";
        return;
    }
    for(i=0;i<n;i++)
    {
        cout<<"\n---INVESTMENT "<<i+1<<"---";
        inv[i].display();
    }
}
void investMore(investment inv[],int n)
{
    int id,i;
    cout<<"\nEnter Investment ID :";
    cin>>id;
    for(i=0;i<n;i++)
    {
        if(inv[i].getID()==id)
        {
            inv[i].addAmount();
            return;
        }
    }
    cout<<"\nInvestment Not Found!";
}
void calculateReturn(investment inv[],int n)
{
    int id;
    cout<<"\nEnter Investment ID:";
    cin>>id;
    for(int i=0;i<n;i++)
    {
        if(inv[i].getID()==id)
        {
            inv[i].returnAmount();
            return;
        }
    }
    cout<<"\nInvestment Not Found";
}
void analyzeRisk(investment inv[],int n)
{
    int id;
    cout<<"\nEnter Investment ID :";
    cin>>id;
    for(int i=0;i<n;i++)
    {
        if(inv[i].getID()==id)
        {
            cout<<"\n---RISK ANALYSIS---";
            if(inv[i].getAmount()>100000)
                cout<<"\nInvestment Amount: High";
            else
                cout<<"\nInvestment Amount : Normal";
            cout<<"\nExpected Return : "<<inv[i].getAmount() * 0.10;
            cout<<"\nRisk Level : Medium";
            return;
        }
    }
    cout<<"\nInvestment Not Found!";
}
int main()
{
    investment inv[20];
    int n=0,ch;
    while(ch!=6)
    {
        cout<<"\n---INVESTMENT RISK ANALYZER---";
        cout<<"\n1. Add Investment";
        cout<<"\n2. Display Investments";
        cout<<"\n3. Invest More";
        cout<<"\n4. Calculate Return";
        cout<<"\n5. Analyze Risk";
        cout<<"\n6. Exit";
        cout<<"\nEnter Choice :";
        cin>>ch;
        switch(ch)
        {
            case 1:
                addInvestment(inv,n);
                break;
            case 2:
                displayInvestment(inv,n);
                break;
            case 3:
                investMore(inv,n);
                break;
            case 4:
                calculateReturn(inv,n);
                break;
            case 5:
                analyzeRisk(inv,n);
                break;
            case 6:
                cout<<"\nThank You!";
                break;
            default:
                cout<<"\nInvalid Choice";
        }
    }
    return 0;
}