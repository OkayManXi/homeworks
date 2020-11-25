#include "supplier.h"

void Supplier::addDrink(CMachine &v)
{
    int continueSend = 1;
    int shelvesId;
    char name[20];
    float price;
    int num;
    Drink tempDrink;
    while (continueSend)
    {
        v.refresh(SEND_DRINK, "【送货模式】请输入货架位置（0-5）:", 0);
        cin >> shelvesId;
        v.refresh(SEND_DRINK, "请输入对应饮料名称:", 0);
        cin >> name;
        v.refresh(SEND_DRINK, "请输入对应饮料价格:", 0);
        cin >> price;
        v.refresh(SEND_DRINK, "请输入对应饮料数量:", 0);
        cin >> num;
        tempDrink.setAllinfo(name, price, num);
        v.sendDrink(tempDrink, shelvesId);
        v.refresh(SEND_DRINK, "继续送货？ yes-1 or no-0: ", 0);
        cin >> continueSend;
    }
}
void Supplier::drawMoney()
{
}
