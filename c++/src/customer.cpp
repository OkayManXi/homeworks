#include "customer.h"

void Customer::buyDrink(CMachine &v)
{
    v.slot();      //投币
    v.buyDrink();  //选择饮料
}