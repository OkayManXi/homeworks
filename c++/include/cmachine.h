#ifndef CMACHINE_H
#define CMACHINE_H

#include <iostream>
#include <iomanip>
#include "sleep.h"
#include "global.h"
#include "drink.h"
#include "account.h"

using namespace std;

class CMachine
{
  private:
    int currentNum;
    bool buttonLighten[6];
    Drink drk[6];
    float moneyCounter;
    Account acc;

  public:
    int capacity;
    int maxType;
    CMachine();
    void display();
    void gotoXY(int x, int y);
    void sendDrink(Drink drk, int i);
    void slot();
    int pressButton(int button);  //购买
    void refreshLight();
    void refresh(int state, char *str, int place);
    int buyDrink();
};

#endif