#include "drink.h"

Drink::Drink(string name, float price, int num)
{
    this->name = name;
    this->price = price;
    this->num = num;
}

Drink::Drink()
{
    num = 0;
}

void Drink::setAllinfo(string name, float price, int num)
{
    this->name = name;
    this->price = price;
    this->num = num;
}

string Drink::getName()
{
    return name;
}

float Drink::getPrice()
{
    return price;
}

int Drink::getNum()
{
    return num;
}

void Drink::setName(string name)
{
    this->name = name;
}

void Drink::setPrice(int price)
{
    this->price = price;
}
void Drink::setNum(int num)
{
    this->num = num;
}

void Drink::display()
{
    if (num == 0)
    {
        cout << "已售罄" << endl;
    }
    else
    {
        cout << "名称：" << getName() << "  价格：" << getPrice() << "  数量" << getNum() << endl;
    }
}