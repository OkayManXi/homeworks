#ifndef DRINK_H
#define DRINK_H

#include <iostream>

using namespace std;

class Drink
{
  private:
    string name;
    float price;
    int num;

  public:
    Drink(string name, float price, int num);
    Drink();
    string getName();
    float getPrice();
    int getNum();
    void setAllinfo(string name, float price, int num);
    void setName(string name);
    void setPrice(int price);
    void setNum(int num);
    void display();
};

#endif