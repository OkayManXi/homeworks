#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <iostream>

using namespace std;

class Account
{
  private:
    float allMoney;

  public:
    Account() : allMoney(0.0){};
    void updateAcc(float exchange);
    float getAllMoney();
};

#endif