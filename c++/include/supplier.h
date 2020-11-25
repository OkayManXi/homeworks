#ifndef SUPPLIER_H
#define SUPPLIER_H

#include <iostream>
#include "drink.h"
#include "cmachine.h"

using namespace std;

class Supplier
{
  public:
    void addDrink(CMachine &v);
    void drawMoney();
};

#endif