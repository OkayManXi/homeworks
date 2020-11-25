#include "cmachine.h"

void CMachine::slot()
{
    float input = 0.0;
    while (true)
    {
        refresh(0, "请输入投入面值，输入-1结束输入:", 0);
        cin >> input;
        if ((int)input == -1)
        {
            refresh(0, NULL, 0);
            break;
        }
        moneyCounter += input;
        refreshLight();
    }
}

int CMachine::buyDrink()
{
    int button;
    int buyState;
    int continueBuy = 1;
    float input;

    while (continueBuy)
    {
        refresh(0, "购买饮料请输入对应编号（0-5）；结束购买并退币请输入-1：", 0);
        cin >> button;
        buyState = pressButton(button);  //选择饮料
        //询问是否继续购买
        refresh(buyState, "继续购买(1), 投币并继续购买(2), 结算(-1)：", 0);
        cin >> continueBuy;
        if (continueBuy == 2)
        {  //投币
            slot();
        }
        if (continueBuy == -1)
        {  //结算并退币

            refresh(SETTLEMENT, NULL, 0);
            break;
        }
    }
}

void CMachine::refresh(int state, char *str, int place)
{
    refreshLight();
    system("cls");
    gotoXY(3, 1);
    cout << "-------------------------------------------------------------" << endl;
    gotoXY(3, 25);
    cout << "-------------------------------------------------------------" << endl;
    gotoXY(3, 20);
    cout << "-------------------------------------------------------------" << endl;
    for (int i = 2; i <= 24; i++)
    {
        gotoXY(3, i);
        cout << "!";
        gotoXY(63, i);
        cout << "!";
    }
    for (int i = 1; i <= 6; i++)
    {  //饮料
        if (drk[i - 1].getNum())
        {
        }
        if (i <= 3)
        {
            gotoXY(15 * i, 4);
            cout << i - 1 << " 号";
            if (drk[i - 1].getNum())
            {  //饮料数量不为零
                gotoXY(15 * i, 5);
                cout << drk[i - 1].getName();
                gotoXY(15 * i - 1, 6);
                cout << "价格：" << drk[i - 1].getPrice();
                gotoXY(15 * i - 1, 7);
                cout << "库存：" << drk[i - 1].getNum();
            }
            else
            {
                gotoXY(15 * i - 1, 6);
                cout << "已售罄";
            }
            gotoXY(15 * i - 1, 8);
            cout << "灯：";
            if (buttonLighten[i - 1])
                cout << "亮";
            else
                cout << "灭";
        }
        else
        {
            gotoXY(15 * (i - 3), 11);
            cout << i - 1 << " 号";
            if (drk[i - 1].getNum())
            {  //饮料数量不为零
                gotoXY(15 * (i - 3), 12);
                cout << drk[i - 1].getName();
                gotoXY(15 * (i - 3) - 1, 13);
                cout << "价格：" << drk[i - 1].getPrice();
                gotoXY(15 * (i - 3) - 1, 14);
                cout << "库存：" << drk[i - 1].getNum();
            }
            else
            {
                gotoXY(15 * (i - 3) - 1, 13);
                cout << "已售罄";
            }

            gotoXY(15 * (i - 3) - 1, 14);
            cout << "灯：";
            if (buttonLighten[i - 1])
                cout << "亮";
            else
                cout << "灭";
        }
    }
    if (state == SEND_DRINK)
    {  //送货模式
        gotoXY(10, 18);
        cout << "当前饮料共" << currentNum << "瓶；还可以放" << capacity - currentNum << "瓶！" << endl;
    }
    else
    {  //顾客模式
        gotoXY(18, 23);
        if (state == BUY_SUCCESS)
        {
            cout << "购买成功，请取走饮料" << endl;
        }
        else if (state == SELLOUT)
        {  //想要买的饮料卖完
            cout << "抱歉！您要买的饮料卖光了" << endl;
        }
        else if (state == SHORTAGE_MONEY)
        {  //钱不够买要买的饮料
            cout << "请继续投币" << endl;
        }
        else if (state == SETTLEMENT)
        {  //退币
            cout << "退币成功！退币金额为: " << fixed << setprecision(1) << moneyCounter << endl;
            moneyCounter = 0;
        }
        else if (state == INVALID_INPUT)
        {  //非法输入
            cout << "非法输入！" << endl;
        }
        gotoXY(18, 18);
        cout << "当前投币数量：" << setiosflags(ios::fixed) << setprecision(1) << moneyCounter;
    }

    if (str)
    {  //提词板
        gotoXY(4, 21);
        if (place == 1)
        {
            gotoXY(4, 22);
        }
        cout << str;
    }
}

void CMachine::gotoXY(int x, int y)
{
    // // Initialize the coordinates
    // COORD coord = {x, y};
    // // Set the position
    // SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
    // return;
}

void CMachine::refreshLight()
{
    for (int i = 0; i <= 5; i++)
    {
        if (moneyCounter >= drk[i].getPrice() && drk[i].getNum())
        {  //投币大于价格 并且 有货
            buttonLighten[i] = true;
        }
        else
            buttonLighten[i] = false;
    }
}

CMachine::CMachine()
{
    capacity = 40;
    maxType = 6;
    currentNum = 0;
    moneyCounter = 0;
    for (int i = 0; i <= maxType; i++)
    {
        buttonLighten[i] = false;
    }
}

int CMachine::pressButton(int button)
{  //购买
    if (button == -1)
    {  //退币
        return SETTLEMENT;
    }
    if (button <= 5 && button >= 0)
    {
        if (this->buttonLighten[button])
        {                                            //对应灯点亮，可以购买
            moneyCounter -= drk[button].getPrice();  //更新投币计数器
            if (drk[button].getNum() - 1 <= 0)
            {  //更新饮料数量
                drk[button].setNum(0);
            }
            else
                drk[button].setNum(drk[button].getNum() - 1);

            acc.updateAcc(drk[button].getPrice());
            return BUY_SUCCESS;
        }
        else
        {  //灯不亮
            if (drk[button].getNum())
            {  //有货
                return SHORTAGE_MONEY;
            }
            else
            {
                return SELLOUT;
            }
        }
    }
    else
    {
        return INVALID_INPUT;
    }
}

void CMachine::sendDrink(Drink drk, int i)
{
    int resent;
    if (i >= 0 && i <= 5)
    {

        if ((this->drk[i].getNum()) != 0)
        {  //当前货架有货物
            refresh(SEND_DRINK, "当前货架有货物!是否清空后再添加？（y-1/n-0）: ", 1);
            cin >> resent;
            if (resent)
            {  //清空重新添加
                currentNum -= this->drk[i].getNum();
                this->drk[i].setNum(0);
            }
            else
            {
                refresh(SEND_DRINK, NULL, 1);
                return;
            }
        }
        if (currentNum + drk.getNum() > capacity)
        {
            refresh(SEND_DRINK, "送货失败！超出售货机最大容量！", 1);
            Sleep(1000);
        }
        else
        {
            currentNum += drk.getNum();
            this->drk[i] = drk;
        }
    }
    else
    {
        refresh(SEND_DRINK, "送货失败！货架号不存在！", 1);
        Sleep(1000);
    }
}