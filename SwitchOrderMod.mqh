//+------------------------------------------------------------------+
//|                                               SwitchOrderMod.mqh |
//|                                                         davdcsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include <AutomatedTradingMQL5/transaction/Transaction.mqh>


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class SwitchOrderMod
  {
private:
   ENUM_ORDER_PENDING_TYPE type;
public:
                     SwitchOrderMod(void) {}

   void              UpdateAtr(ENUM_ORDER_PENDING_TYPE restart_type) { type = restart_type; }

   ENUM_ORDER_PENDING_TYPE GetPrivateAtr(void) { return type; }

   void              Run(void) { type = type == ORDER_PENDING_TYPE_BUY ? ORDER_PENDING_TYPE_SELL : ORDER_PENDING_TYPE_BUY; }

  };
//+------------------------------------------------------------------+
