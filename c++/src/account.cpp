#include "account.h"

void Account::updateAcc(float exchange)
{
    allMoney += exchange;
}
float Account::getAllMoney()
{
    return allMoney;
}